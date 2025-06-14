import streamlit as st
from ..core.auto_labeler import AutoLabeler

class CorrectionUI:
    @staticmethod
    def launch_web_ui():
        st.set_page_config(page_title="本体标注校正平台", layout="wide")
        st.title("本体标注校正平台（Beta）")
        st.write("上传史料文本，自动抽取实体/关系/事件链，并支持人工校正、争议处理和权力量化。")

        uploaded_file = st.file_uploader("上传史料文本（txt/utf-8）", type=["txt"])
        if uploaded_file:
            text = uploaded_file.read().decode("utf-8")
            st.subheader("原始文本")
            st.text_area("史料内容", text, height=200)
            if st.button("自动抽取实体/关系/事件链"):
                with st.spinner("LLM抽取中..."):
                    entities = AutoLabeler.extract_entities(text)
                    relations = AutoLabeler.extract_relations(text)
                    event_chain = AutoLabeler.generate_event_chain(entities, relations)
                st.success("抽取完成！")
                st.subheader("实体标注校正与权力量化")
                entity_edits = []
                for i, ent in enumerate(entities):
                    col1, col2, col3, col4 = st.columns([3,2,3,2])
                    with col1:
                        name = st.text_input(f"实体名_{i}", ent.get('name', ''))
                    with col2:
                        typ = st.text_input(f"类型_{i}", ent.get('type', ''))
                    with col3:
                        evidence = st.text_area(f"证据_{i}", ent.get('evidence', ''))
                    with col4:
                        power = st.slider(f"权力值_{i}", 0.0, 1.0, float(ent.get('power', 0.5)), 0.01)
                    entity_edits.append({'name': name, 'type': typ, 'evidence': evidence, 'power': power})
                st.subheader("关系标注校正与争议处理")
                relation_edits = []
                for i, rel in enumerate(relations):
                    col1, col2, col3, col4, col5 = st.columns([2,2,2,4,2])
                    with col1:
                        subj = st.text_input(f"主体_{i}", rel.get('subject', ''))
                    with col2:
                        pred = st.text_input(f"关系_{i}", rel.get('predicate', ''))
                    with col3:
                        obj = st.text_input(f"客体_{i}", rel.get('object', ''))
                    with col4:
                        evidence = st.text_area(f"依据_{i}", rel.get('evidence', ''))
                    with col5:
                        # 争议标记
                        conflict = st.checkbox(f"争议_{i}", value=rel.get('conflict', False))
                    relation_edits.append({'subject': subj, 'predicate': pred, 'object': obj, 'evidence': evidence, 'conflict': conflict})
                st.subheader("事件链校正")
                st.json(event_chain)
                if st.button("导出标注结果（JSON）"):
                    import json
                    st.download_button(
                        label="下载JSON",
                        data=json.dumps({
                            'entities': entity_edits,
                            'relations': relation_edits,
                            'event_chain': event_chain
                        }, ensure_ascii=False, indent=2),
                        file_name="labeled_result.json",
                        mime="application/json"
                    )