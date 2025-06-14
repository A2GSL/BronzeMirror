# BronzeMirror 用户文档

## 1. 项目简介
BronzeMirror（铜镜）是一个基于历史事件本体建模与AI推理的决策辅助系统。用户可上传组织变量，查询历史知识图谱，并获得智能化的历史借鉴建议。

---

## 2. 数据上传

### 2.1 上传本体与三元组
- 将自定义的本体（Turtle格式）放入 `ontologies/xuanwumen/entities.ttl`
- 将三元组关系（N-Triples格式）放入 `ontologies/xuanwumen/relations.nt`
- 事件元数据（JSON-LD格式）放入 `ontologies/xuanwumen/metadata.jsonld`

### 2.2 变量与规则
- 在 `metadata.jsonld` 中补充/修改变量（如 coreTeamLoss, powerRatio）及其阈值、危险区间
- 可扩展规则，后续脚本会自动解析

---

## 3. 知识查询与可视化

### 3.1 命令行查询
- 运行 `python scripts/validate_ontology.py` 检查本体、三元组、变量一致性
- 运行 `python scripts/infer_risk.py` 输入变量，推理风险等级与建议

### 3.2 可视化知识图谱
- 运行 `python scripts/visualize.py`，可视化本体结构，支持高亮任意实体及其关联

---

## 4. 获得历史智能建议

### 4.1 命令行智能建议
- 运行 `python scripts/historical_advice.py`
- 输入你的决策问题（如“高管流失，权力分配失衡，如何应对？”）及变量，系统自动结合历史案例与规则输出建议

### 4.2 Web交互原型
- 运行 `python scripts/web_demo.py`
- 在浏览器访问 http://127.0.0.1:5000/
- 填写变量，实时获得风险推理与历史建议

---

## 5. 扩展与定制
- 可自定义本体、三元组、变量、规则，支持多历史事件、多组织场景
- 可集成更强大的自然语言模型（如transformers）实现更丰富的智能问答
- 支持导出Neo4j等格式，便于大规模知识图谱分析

---

## 6. 常见问题
- 依赖库安装：`pip install rdflib flask networkx matplotlib transformers`
- 如遇脚本报错，请检查文件路径、格式及依赖库
- 如需批量导入、API接口、Web美化等高级功能，请联系开发者

---

## 7. 联系与反馈
如有问题、建议或定制需求，请联系项目维护者。
