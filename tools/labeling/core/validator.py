import json
from typing import List, Dict

class OntologyValidator:
    @staticmethod
    def check_consistency(ontology: Dict) -> List[str]:
        """
        本体一致性检查：
        1. 同一实体不能有矛盾属性（如同名不同类型）
        2. 关系必须连接已定义实体
        3. 权力量化值应在[0,1]区间
        4. 争议关系应有证据
        返回所有发现的问题列表
        """
        issues = []
        entity_names = set()
        entity_types = dict()
        for ent in ontology.get('entities', []):
            name = ent.get('name')
            typ = ent.get('type')
            if name in entity_names:
                if entity_types.get(name) != typ:
                    issues.append(f"实体 {name} 类型不一致: {entity_types.get(name)} vs {typ}")
            else:
                entity_names.add(name)
                entity_types[name] = typ
            # 权力量化校验
            power = ent.get('power')
            if power is not None and not (0.0 <= float(power) <= 1.0):
                issues.append(f"实体 {name} 权力值超出[0,1]区间: {power}")
        # 关系校验
        for rel in ontology.get('relations', []):
            subj = rel.get('subject')
            obj = rel.get('object')
            if subj not in entity_names:
                issues.append(f"关系主体 {subj} 未定义为实体")
            if obj not in entity_names:
                issues.append(f"关系客体 {obj} 未定义为实体")
            # 争议校验
            if rel.get('conflict') and not rel.get('evidence'):
                issues.append(f"争议关系 {subj}-{rel.get('predicate')}-{obj} 缺少证据")
        return issues

    @staticmethod
    def cross_event_validation(event1: Dict, event2: Dict) -> List[str]:
        """
        跨事件逻辑验证：如人物时间线连续性、事件因果链闭环等
        """
        issues = []
        # 示例：检查同一人物在不同事件中的类型/权力值是否突变
        e1_entities = {e['name']: e for e in event1.get('entities', [])}
        e2_entities = {e['name']: e for e in event2.get('entities', [])}
        for name in set(e1_entities) & set(e2_entities):
            p1 = e1_entities[name].get('power')
            p2 = e2_entities[name].get('power')
            if p1 is not None and p2 is not None and abs(float(p1)-float(p2)) > 0.7:
                issues.append(f"实体 {name} 在事件间权力值突变: {p1} -> {p2}")
        return issues

    @staticmethod
    def export_validation_report(issues: List[str], file_path="validation_report.txt"):
        with open(file_path, 'w', encoding='utf-8') as f:
            for issue in issues:
                f.write(issue + '\n')
        print(f"[INFO] 验证报告已导出: {file_path}")