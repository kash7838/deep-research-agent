import streamlit as st
from src.deep_research_agent.agent import DeepResearchAgent

st.set_page_config(
    page_title="Deep Research Agent",
    page_icon="🤖",
    layout="centered"
)

st.title("🤖 Autonomous Deep Research Agent")
st.markdown("Powered by **Streamlit**, **Local RAG**, and strict **500-Token Budget Constraints**.")

# Initialize agent session state
if "agent" not in st.session_state:
    st.session_state.agent = DeepResearchAgent()

# Input form
with st.form("research_form"):
    topic_input = st.text_input("Research Topic", placeholder="e.g., State of Agentic AI workflows in 2026")
    submitted = st.form_submit_button("Start Research")

if submitted:
    if not topic_input.strip():
        st.warning("Please enter a valid research topic.")
    else:
        with st.spinner("Executing RAG retrieval and generating report..."):
            try:
                # Run research pipeline
                report = st.session_state.agent.run_research(topic_input)
                
                st.success("Research completed successfully!")
                st.markdown("### Generated Report")
                st.markdown(report)
                
            except Exception as e:
                st.error(f"An error occurred during research execution: {e}")