from backend.core import run_llm
import streamlit as st
from streamlit_chat import message
from collections import Set
import os

os.environ["LANGCHAIN_TRACING"] = "true"

def create_source_string(source_urls: set) -> str:
    if not source_urls:
        return ""
    source_list = list(source_urls)
    source_list.sort()
    sources_string = "sources:\n"
    for i, source in enumerate(source_list):
        sources_string += f"{i+1}. {source}\n"
    return sources_string


st.header("CBOT Rulebook - Helper BOT")
prompt = st.text_input("Prompt", placeholder="Enter your prompt here..")

if "user_prompt_history" not in st.session_state:
    st.session_state['user_prompt_history'] = []

if "chat_answer_history" not in st.session_state:
    st.session_state['chat_answer_history'] = []   

if prompt:
    with st.spinner("Generating response..."):
        generated_response = run_llm(query=prompt)
        sources = set([doc.metadata['source'] for doc in generated_response["source_documents"]])

        formatted_response = f"{generated_response['result']} \n\n {create_source_string(sources)}"
        #st.text(formatted_response)

        html_str = f"""
            <html>
            <body>
            <p>{generated_response['result']} \n\n {create_source_string(sources)}</p> </body></html>
            """

        st.markdown(html_str, unsafe_allow_html=True)

        #st.markdown(":green{formatted_response}")

        st.session_state['user_prompt_history'].append(prompt)
        st.session_state['chat_answer_history'].append(formatted_response)

if st.session_state['chat_answer_history']:
    for response,user_query  in zip(st.session_state['chat_answer_history'],st.session_state['user_prompt_history']):
        message(user_query,is_user=True)
        message(response)
        