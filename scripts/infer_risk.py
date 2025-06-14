import rdflib
import json
from pathlib import Path

ttl_path = Path(__file__).parent.parent / 'ontologies/xuanwumen/entities.ttl'
jsonld_path = Path(__file__).parent.parent / 'ontologies/xuanwumen/metadata.jsonld'

# 简单推理规则：
# 如果 coreTeamLoss > 阈值 且 powerRatio 在危险区间，则风险等级为 CRITICAL，否则为 NORMAL

def infer_risk(core_team_loss, power_ratio):
    g = rdflib.Graph()
    g.parse(str(ttl_path), format='turtle')
    with open(jsonld_path, encoding='utf-8') as f:
        meta = json.load(f)
    # 获取阈值和危险区间
    threshold = None
    danger_zone = None
    for v in meta.get('variables', []):
        if v['name'] == 'coreTeamLoss':
            threshold = v.get('threshold', 0.6)
        if v['name'] == 'powerRatio':
            danger_zone = v.get('dangerZone', [1.5, 2.0])
    # 推理
    risk = 'NORMAL'
    advice = '暂无风险，注意团队稳定和权力平衡。'
    if threshold is not None and danger_zone is not None:
        if core_team_loss > threshold and danger_zone[0] <= power_ratio <= danger_zone[1]:
            risk = 'CRITICAL'
            advice = '核心团队流失率高且权力分配失衡，建议立即干预关键岗位和权力结构。'
    print(f"[推理结果] 风险等级: {risk}")
    print(f"[建议] {advice}")
    return risk, advice

if __name__ == '__main__':
    # 示例：可替换为命令行参数或交互输入
    core_team_loss = float(input('请输入核心团队流失率（如0.7）: '))
    power_ratio = float(input('请输入权力比值（如1.8）: '))
    infer_risk(core_team_loss, power_ratio)
