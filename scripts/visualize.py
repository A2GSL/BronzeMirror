from pyvis.network import Network

net = Network(height="600px")
net.add_node("李世民", title="权力值: 0.75", group="person")
net.add_node("玄武门", title="控制值: 0.92", group="place")
net.add_edge("李世民", "玄武门", title="收买控制")
net.show("xuanwumen.html")