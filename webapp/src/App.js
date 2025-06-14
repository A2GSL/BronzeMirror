import OntologyGraph from './OntologyGraph';
import React, { useState } from 'react';
import { Layout, Menu, Button, Input, Tabs, Spin, Alert } from 'antd';
import { modelOntology } from './api';

const { Header, Content, Footer, Sider } = Layout;
const { TextArea } = Input;

function App() {
  const [desc, setDesc] = useState('');
  const [loading, setLoading] = useState(false);
  const [ontology, setOntology] = useState(null);
  const [error, setError] = useState(null);

  const handleSubmit = async () => {
    setLoading(true);
    setError(null);
    try {
      const res = await modelOntology(desc);
      setOntology(res);
    } catch (e) {
      setError('建模失败，请检查后端服务或网络连接。');
    }
    setLoading(false);
  };

  return (
    <Layout style={{ minHeight: '100vh' }}>
      <Header style={{ color: '#fff', fontSize: 22 }}>BronzeMirror 历史决策智能系统</Header>
      <Layout>
        <Sider width={220} style={{ background: '#fff' }}>
          <Menu mode="inline" defaultSelectedKeys={['dialogue']}
            items={[
              { key: 'dialogue', label: '对话决策' },
              { key: 'annotation', label: '本体标注' }
            ]}
          />
        </Sider>
        <Content style={{ padding: 24 }}>
          <Tabs defaultActiveKey="dialogue">
            <Tabs.TabPane tab="对话决策" key="dialogue">
              <TextArea
                rows={4}
                placeholder="请描述您想要咨询的历史事件或决策情景..."
                value={desc}
                onChange={e => setDesc(e.target.value)}
                disabled={loading}
              />
              <Button type="primary" style={{ marginTop: 12 }} onClick={handleSubmit} loading={loading}>
                提交
              </Button>
              {error && <Alert type="error" message={error} style={{ marginTop: 16 }} />}
              {loading && <Spin style={{ marginTop: 16 }} />}
              {/* 对话流展示区 */}
              {ontology && (
                <div style={{ marginTop: 24 }}>
                  <h3>本体建模结果</h3>
                  <pre>{JSON.stringify(ontology.triples, null, 2)}</pre>
                  <div>文字说明：{ontology.text_summary}</div>
                  <OntologyGraph graphData={ontology.graph_json} />
                </div>
              )}
              {/* 用户确认/反馈区 */}
              {/* 历史推理与建议区 */}
            </Tabs.TabPane>
            <Tabs.TabPane tab="本体标注" key="annotation">
              {/* 标注者入口与标注界面 */}
            </Tabs.TabPane>
          </Tabs>
        </Content>
      </Layout>
      <Footer style={{ textAlign: 'center' }}>© 2025 BronzeMirror</Footer>
    </Layout>
  );
}

export default App;