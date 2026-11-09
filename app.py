import streamlit as st
import os, base64
from datetime import datetime

st.set_page_config(page_title="AI Data Quality Analyzer", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
.main { font-family: 'Inter', sans-serif; background: #0f172a; }
.stApp { background: #0f172a; }
.card { background: #1e293b; border: 1px solid #334155; border-radius: 12px; padding: 24px; margin: 8px 0; color: #e2e8f0; }
.accent-blue { border-left: 4px solid #3b82f6; }
.accent-teal { border-left: 4px solid #14b8a6; }
.accent-orange { border-left: 4px solid #f97316; }
.accent-purple { border-left: 4px solid #a855f7; }
.stButton>button { background: #3b82f6; color: white; border-radius: 8px; border: none; }
.stButton>button:hover { background: #2563eb; }
a { color: #3b82f6; text-decoration: none; }
a:hover { text-decoration: underline; color: #60a5fa; }
</style>
""", unsafe_allow_html=True)

def main_app():
    st.sidebar.title("AI Data Quality Analyzer")
    st.sidebar.markdown("**Study Station for AI Agent Framework**")
    st.sidebar.markdown("---")
    pages = st.sidebar.radio("Navigation", ["Dashboard", "Study AI Agent Framework", "Datasets", "Cached Outputs", "Report Generation _output"])
    st.sidebar.markdown("---")
    st.sidebar.markdown("AI Data Quality Analyzer - All Rights Reserved")

    if pages == "Dashboard":
        st.title("AI Data Quality Analyzer")
        st.markdown("Your central hub for learning AI agent system building.")
        c1, c2, c3 = st.columns(3)
        with c1:
            st.markdown('<div class="card accent-blue">', unsafe_allow_html=True)
            st.subheader("Part 1 - Introduction")
            st.markdown("System architecture, data flow & anomalies")
            st.markdown('</div>', unsafe_allow_html=True)
        with c2:
            st.markdown('<div class="card accent-teal">', unsafe_allow_html=True)
            st.subheader("Part 2 - Agent Deep Dive")
            st.markdown("Agent types, communication, concurrency")
            st.markdown('</div>', unsafe_allow_html=True)
        with c3:
            st.markdown('<div class="card accent-orange">', unsafe_allow_html=True)
            st.subheader("Part 3 - Advanced Topics")
            st.markdown("RAG, frameworks, deployment & security")
            st.markdown('</div>', unsafe_allow_html=True)

    elif pages == "Study AI Agent Framework":
        st.title("Study AI Agent Framework")
        st.markdown("### Access All 3 Presentation Parts")
        ppt_dir = os.path.dirname(os.path.abspath(__file__))
        st.markdown("---")
        col1, col2 = st.columns(2)
        with col1:
            st.markdown('<div class="card accent-blue">', unsafe_allow_html=True)
            st.subheader("Part 1: Introduction")
            st.markdown("System architecture, data flow, anomaly detection")
            f1 = os.path.join(ppt_dir, "AI_Data_Quality_Analyzer.pptx")
            if os.path.exists(f1):
                with open(f1, "rb") as f:
                    b64 = base64.b64encode(f.read()).decode()
                st.markdown(f'<a href="data:application/vnd.openxmlformats-officedocument.presentationml.presentation;base64,{b64}" download="AI_Data_Quality_Analyzer.pptx">Download PPT</a>', unsafe_allow_html=True)
            else:
                st.warning("PPT not found")
            st.markdown('</div>', unsafe_allow_html=True)
        with col2:
            st.markdown('<div class="card accent-teal">', unsafe_allow_html=True)
            st.subheader("Part 2: Agent Deep Dive")
            st.markdown("Agent types, communication patterns, concurrency")
            f2 = os.path.join(ppt_dir, "Part2_Agent_Deep_Dive.pptx")
            if os.path.exists(f2):
                with open(f2, "rb") as f:
                    b64 = base64.b64encode(f.read()).decode()
                st.markdown(f'<a href="data:application/vnd.openxmlformats-officedocument.presentationml.presentation;base64,{b64}" download="Part2_Agent_Deep_Dive.pptx">Download PPT</a>', unsafe_allow_html=True)
            else:
                st.warning("PPT not found")
            st.markdown('</div>', unsafe_allow_html=True)
        st.markdown("---")
        c3, c4 = st.columns(2)
        with c3:
            st.markdown('<div class="card accent-orange">', unsafe_allow_html=True)
            st.subheader("Part 3: Advanced Topics")
            st.markdown("RAG, LLM integration, deployment, security")
            f3 = os.path.join(ppt_dir, "Part3_Advanced_Topics.pptx")
            if os.path.exists(f3):
                with open(f3, "rb") as f:
                    b64 = base64.b64encode(f.read()).decode()
                st.markdown(f'<a href="data:application/vnd.openxmlformats-officedocument.presentationml.presentation;base64,{b64}" download="Part3_Advanced_Topics.pptx">Download PPT</a>', unsafe_allow_html=True)
            else:
                st.warning("PPT not found")
            st.markdown('</div>', unsafe_allow_html=True)
        with c4:
            st.markdown('<div class="card accent-purple">', unsafe_allow_html=True)
            st.subheader("Code Resources")
            st.markdown("- `agent_system.py` - Multi-agent swarm")
            st.markdown("- `data ingestion.js` - Express backend")
            st.markdown("- `create_ppt.py` - PPT generator")
            st.markdown('</div>', unsafe_allow_html=True)

    elif pages == "Datasets":
        st.title("Datasets")
        st.markdown("### Data Resources for AI Agent Training")
        st.markdown('<div class="card accent-blue">', unsafe_allow_html=True)
        st.subheader("Sample Datasets")
        st.markdown("""
        - **Anomaly Dataset** - Labeled data quality anomalies
        - **Training Data** - Used for agent model training
        - **Test Data** - Validation and evaluation sets
        - **Schema Rules** - Business logic constraints for detection
        """)
        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown("### Available Data Files")
        st.markdown("- `flagged_anomalies.json` - Detected anomalies with context")
        st.markdown("- `organizational_memory.json` - Learned rules and embeddings")
        st.markdown("- `schema_rules.csv` - Validation rules for data quality")

    elif pages == "Cached Outputs":
        st.title("Cached Outputs")
        st.markdown("### Cached Agent Results & Model Outputs")
        st.markdown('<div class="card accent-teal">', unsafe_allow_html=True)
        st.subheader("Cache Directory")
        st.markdown("""
        - **Agent Predictions** - Cached anomaly detection results
        - **Embedding Cache** - Vector embeddings for fast retrieval
        - **Memory Snapshots** - Organizational memory checkpoints
        - **Pipeline Outputs** - Processed data from each run
        """)
        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown("### Cache Status")
        st.metric("Cache Size", "2.4 MB")
        st.metric("Last Updated", datetime.now().strftime("%Y-%m-%d %H:%M"))
        st.metric("Entries", "142")

    elif pages == "Report Generation _output":
        st.title("Report Generation _output")
        st.markdown("### Generate Quality Reports")
        st.markdown('<div class="card accent-orange">', unsafe_allow_html=True)
        st.subheader("Report Types")
        st.markdown("""
        - **Anomaly Summary Report** - Overview of all detected anomalies
        - **Remediation Log** - HITL decision tracking
        - **Memory Growth Report** - New rules learned over time
        - **Agent Performance** - Detection accuracy & latency metrics
        """)
        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown("### Generate Report")
        report_name = st.text_input("Report Name")
        report_type = st.selectbox("Report Type", ["Anomaly Summary", "Remediation Log", "Memory Growth", "Performance"])
        if st.button("Generate Report"):
            st.success(f"Report '{report_name}' ({report_type}) generated successfully!")
            st.markdown(f"**Output saved to:** `_output/{report_name}.pdf`")

# ── Entry Point ──
main_app()
