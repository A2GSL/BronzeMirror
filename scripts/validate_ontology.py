from rdflib import Graph

def validate_ttl(file_path):
    g = Graph()
    try:
        g.parse(file_path, format="turtle")
        print(f"✅ 本体文件验证通过: {len(g)} 条三元组")
    except Exception as e:
        print(f"❌ 错误: {str(e)}")

validate_ttl("ontologies/xuanwumen/entities.ttl")