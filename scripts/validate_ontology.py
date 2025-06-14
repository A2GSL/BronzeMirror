import rdflib
import json
from pathlib import Path

ttl_path = Path(__file__).parent.parent / 'ontologies/xuanwumen/entities.ttl'
nt_path = Path(__file__).parent.parent / 'ontologies/xuanwumen/relations.nt'
jsonld_path = Path(__file__).parent.parent / 'ontologies/xuanwumen/metadata.jsonld'

def validate_entities_and_relations():
    g = rdflib.Graph()
    g.parse(str(ttl_path), format='turtle')
    g.parse(str(nt_path), format='nt')
    print(f"[INFO] 加载三元组数量: {len(g)}")

    # 检查所有nt中的实体和属性是否在ttl中有定义
    missing_entities = set()
    missing_predicates = set()
    for s, p, o in g:
        for node in [s, o]:
            if isinstance(node, rdflib.URIRef):
                if (node, None, None) not in g and (None, None, node) not in g:
                    missing_entities.add(str(node))
        if (p, None, None) not in g:
            missing_predicates.add(str(p))
    if missing_entities:
        print("[WARN] 以下实体未在本体中声明:")
        for e in missing_entities:
            print("  ", e)
    if missing_predicates:
        print("[WARN] 以下属性未在本体中声明:")
        for p in missing_predicates:
            print("  ", p)
    if not missing_entities and not missing_predicates:
        print("[OK] 所有实体和属性均已声明")

    # 检查变量和规则
    with open(jsonld_path, encoding='utf-8') as f:
        meta = json.load(f)
    variables = {v['name'] for v in meta.get('variables', [])}
    for var in variables:
        found = False
        for s, p, o in g.triples((None, None, None)):
            if var in str(p) or var in str(o):
                found = True
                break
        if not found:
            print(f"[WARN] 变量 {var} 未在本体或三元组中出现")
    print("[INFO] 校验完成")

if __name__ == '__main__':
    validate_entities_and_relations()