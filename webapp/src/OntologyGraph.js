import React from 'react';
import CytoscapeComponent from 'react-cytoscapejs';

export default function OntologyGraph({ graphData }) {
  if (!graphData || !graphData.nodes || !graphData.edges) return null;

  // 转换为cytoscape格式
  const elements = [
    ...graphData.nodes.map(n => ({ data: { id: n.id, label: n.label } })),
    ...graphData.edges.map(e => ({ data: { source: e.source, target: e.target, label: e.label } }))
  ];

  return (
    <div style={{ height: 400, marginTop: 16 }}>
      <CytoscapeComponent
        elements={elements}
        style={{ width: '100%', height: '100%' }}
        layout={{ name: 'cose' }}
        cy={cy => cy.fit()}
      />
    </div>
  );
}
