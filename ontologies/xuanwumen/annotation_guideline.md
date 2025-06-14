# 宣武门之变本体标注规范（V1.0）

## 1. 标注目标
以RDF/OWL本体为基础，规范性标注《资治通鉴·宣武门之变》相关历史文本中的实体、关系和事件，便于后续知识抽取、推理和AI辅助决策。

## 2. 标注对象
- 人物（Person）：历史人物、主要参与者
- 组织（Organization）：政权、军队、宫廷等
- 地点（Place）：事件发生的具体地点
- 事件（Event）：历史事件、关键行为
- 权力流转（PowerTransfer）：权力继承、政变结果
- 关系（ObjectProperty）：如参与、杀害、支持、反对、指挥、因果等

## 3. 标注格式
采用Turtle语法，实体、事件、关系均以三元组形式表达。

### 3.1 实体标注
- 人物示例：
  xuan:LiShiMin a hist:Person ; hist:name "李世民" .
- 地点示例：
  xuan:Xuanwumen a hist:Place ; rdfs:label "宣武门" .

### 3.2 事件标注
- 事件示例：
  xuan:XuanwumenIncident a hist:Event ;
    rdfs:label "宣武门之变" ;
    hist:occursAt xuan:Xuanwumen ;
    hist:time "626-07-02" ;
    hist:hasParticipant xuan:LiShiMin, xuan:LiJianCheng, xuan:LiYuanJi ;
    hist:hasOutcome xuan:LiShiMinSuccess .

### 3.3 关系标注
- 参与关系：hist:hasParticipant
- 杀害关系：hist:killed
- 权力继承：hist:succeededBy
- 支持/反对：hist:supports / hist:opposes
- 指挥：hist:commands
- 隶属：hist:belongsTo
- 因果：hist:causedBy

#### 关系三元组示例：
- xuan:LiShiMin hist:killed xuan:LiJianCheng .
- xuan:LiShiMin hist:supports xuan:LiYuan .
- xuan:XuanwumenIncident hist:causedBy xuan:PowerStruggle .

## 4. 标注原则
1. 以史实为准，优先还原事件真实脉络。
2. 事件、关系应尽量细化，便于后续推理。
3. 复杂事件可拆分为多个子事件，建立因果链。
4. 标注时注意区分实体类型，避免混淆。
5. 所有URI命名统一用英文拼音或规范缩写。

## 5. 标注流程建议
1. 逐段阅读史料，识别并标注实体。
2. 梳理事件链，标注事件及其参与者、时间、地点、结果。
3. 明确事件间因果、权力流转等关系。
4. 复查三元组，确保语义清晰、无歧义。

---
如需扩展属性、关系或遇到歧义，请在文档中补充说明并与团队讨论。
