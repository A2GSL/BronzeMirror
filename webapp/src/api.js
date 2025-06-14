import axios from 'axios';

const API_BASE = 'http://localhost:8000'; // 后端FastAPI服务地址

export async function modelOntology(description) {
  const res = await axios.post(`${API_BASE}/model_ontology`, {
    description
  });
  return res.data;
}

export async function feedbackAndRemodel(feedback, lastOntology) {
  const res = await axios.post(`${API_BASE}/feedback_and_remodel`, {
    feedback,
    last_ontology: lastOntology
  });
  return res.data;
}

export async function getAdvice(ontology) {
  const res = await axios.post(`${API_BASE}/get_advice`, {
    ontology
  });
  return res.data;
}
