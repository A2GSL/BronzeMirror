import rdflib
import json
from pathlib import Path
try:
    from transformers import pipeline
    has_transformers = True
except ImportError:
    has_transformers = False

# 配置文件路径
ttl_path = Path(__file__).parent.parent / 'ontologies/xuanwumen/entities.ttl'
jsonld_path = Path(__file__).parent.parent / 'ontologies/xuanwumen/metadata.jsonld'

# 历史推理与建议

def get_historical_advice(user_question, core_team_loss=None, power_ratio=None):
    # 1. 结构化变量推理
    advice = ""
    if core_team_loss is not None and power_ratio is not None:
        # 简单规则同infer_risk.py
        with open(jsonld_path, encoding='utf-8') as f:
            meta = json.load(f)
        threshold = None
        danger_zone = None
        for v in meta.get('variables', []):
            if v['name'] == 'coreTeamLoss':
                threshold = v.get('threshold', 0.6)
            if v['name'] == 'powerRatio':
                danger_zone = v.get('dangerZone', [1.5, 2.0])
        if threshold is not None and danger_zone is not None:
            if core_team_loss > threshold and danger_zone[0] <= power_ratio <= danger_zone[1]:
                advice = '历史经验：核心团队流失率高且权力分配失衡，极易引发权力危机。建议：立即干预关键岗位、优化权力结构、加强信任建设。参考宣武门之变。'
            else:
                advice = '历史经验：当前风险可控，但需持续关注团队稳定和权力平衡。'
    # 2. 如有transformers，支持自然语言问答
    if has_transformers:
        nlp = pipeline('text-generation', model='gpt2')
        prompt = f"客户问题：{user_question}\n请结合中国历史重大权力交接事件（如宣武门之变），给出决策建议："
        ai_reply = nlp(prompt, max_length=128, do_sample=True)[0]['generated_text']
        return advice + '\n' + ai_reply
    else:
        return advice + '\n(如需自然语言AI建议，请安装transformers和相关大模型)'

if __name__ == '__main__':
    print("=== 历史决策智能建议接口 ===")
    user_question = input("请输入你的决策问题（如：高管流失，权力分配失衡，如何应对？）：")
    try:
        core_team_loss = float(input("请输入核心团队流失率（如0.7，可留空）：") or 0)
        power_ratio = float(input("请输入权力比值（如1.8，可留空）：") or 0)
    except Exception:
        core_team_loss = None
        power_ratio = None
    print("\n[历史智能建议]")
    print(get_historical_advice(user_question, core_team_loss, power_ratio))
