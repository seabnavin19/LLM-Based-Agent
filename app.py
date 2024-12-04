import time
import streamlit as st
import google.generativeai as genai
from Agent import Agent


st.set_page_config(
    page_title="LLM-Based Agent",
    page_icon="resources/images/robot.png",
    layout="wide",
)

agent = Agent()

col1, col2 = st.columns([8, 1])
with col1:
    st.title("LLM-Based Agent")
with col2:
    st.image("resources/images/robot.png", width=100)

st.subheader("Powered by Function Calling in Gemini")


with st.expander("Sample prompts", expanded=True):
    st.write(
        """
        1. **Can you recommend a hotel in Phnom Penh for next week?**
        2. **What events are happening in Siem Reap this weekend?**
        3. **What is the weather like in Phnom Penh tomorrow?**
        4. **Can you suggest some events for this week in Sihanoukville?**
        5. **Find me a hotel in Battambang for next month.**

    """
    )

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"].replace("$", r"\$"))  # noqa: W605

if prompt := st.chat_input("Ask me about information in the database..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""




        try:
            answer,fcs = agent.answer(prompt)

            api_requests_and_responses = []
            backend_details = fcs

            full_response = answer
            with message_placeholder.container():
                st.markdown(full_response.replace("$", r"\$")) 
                with st.expander("Function calls, parameters, and responses:"):
                    st.markdown(backend_details)

            st.session_state.messages.append(
                {
                    "role": "assistant",
                    "content": full_response,
                    'backend_details': fcs,
                }
            )
            
        except Exception as e:
            print(e)
            error_message = f"""
                Something went wrong! We encountered an unexpected error while
                trying to process your request. Please try rephrasing your
                question. Details:

                {str(e)}"""
            st.error(error_message)
            st.session_state.messages.append(
                {
                    "role": "assistant",
                    "content": error_message,
                }
            )