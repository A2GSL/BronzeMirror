from ..utils.llm_intergrator import LLMIntegrator

class AutoLabeler:
    @staticmethod
    def extract_entities(text: str) -> list:
        """实体识别：返回[(实体名, 类型, 初始标签, 证据)]"""
        return LLMIntegrator.extract(text, task="entity_extraction")

    @staticmethod
    def extract_relations(text: str) -> list:
        """关系抽取：返回[(主体, 关系, 客体, 依据)]"""
        return LLMIntegrator.extract(text, task="relation_extraction")

    @staticmethod
    def generate_event_chain(entities, relations) -> dict:
        """事件链生成：返回时序化事件图谱（可直接用LLM抽取）"""
        # 可选：直接用LLM抽取，也可基于entities/relations拼接
        return LLMIntegrator.extract('\n'.join([str(entities), str(relations)]), task="event_chain")

    @staticmethod
    def resolve_conflicts(text: str) -> dict:
        """史料矛盾处理：返回多版本概率权重（可用LLM或规则融合）"""
        # 这里可扩展为多模型/多版本融合
        return {"conflicts": "TODO: 多版本融合实现"}

    @staticmethod
    def batch_label(texts: list, task="entity_extraction", api_key=None) -> list:
        """批量文本自动标注，返回结构化结果列表"""
        results = []
        for idx, text in enumerate(texts):
            print(f"[INFO] 正在处理第{idx+1}段文本...")
            try:
                result = LLMIntegrator.extract(text, task=task, api_key=api_key)
                results.append(result)
            except Exception as e:
                print(f"[ERROR] 第{idx+1}段处理失败: {e}")
                results.append(None)
        return results