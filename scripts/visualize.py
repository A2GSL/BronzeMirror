import rdflib
import networkx as nx
import matplotlib.pyplot as plt
from pathlib import Path

# 路径配置
ttl_path = Path(__file__).parent.parent / 'ontologies/xuanwumen/entities.ttl'

# 读取RDF并转为NetworkX图
def rdf_to_nx_graph():
    g = rdflib.Graph()
    g.parse(str(ttl_path), format='turtle')
    G = nx.MultiDiGraph()
    for s, p, o in g:
        G.add_edge(str(s), str(o), label=str(p))
    return G

def visualize_graph(G, focus_entity=None):
    plt.figure(figsize=(16, 10))
    pos = nx.spring_layout(G, k=0.5)
    # 只高亮focus_entity及其一阶关联
    node_colors = []
    for node in G.nodes():
        if focus_entity and focus_entity in node:
            node_colors.append('red')
        else:
            node_colors.append('skyblue')
    nx.draw(G, pos, with_labels=True, node_color=node_colors, edge_color='gray', font_size=10, node_size=1200)
    edge_labels = {(u, v): d['label'].split('#')[-1] for u, v, d in G.edges(data=True)}
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color='green')
    plt.title('宣武门之变本体知识图谱')
    plt.show()

if __name__ == '__main__':
    G = rdf_to_nx_graph()
    print("可视化节点示例：如xuan:LiShiMin, xuan:XuanwumenIncident")
    focus = input('请输入要高亮的实体（如LiShiMin，可留空）：').strip()
    focus_entity = focus if focus else None
    visualize_graph(G, focus_entity)