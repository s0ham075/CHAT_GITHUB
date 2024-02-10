import streamlit as st
import pandas as pd
import random 
import time
import os 
from query import answer_query
from main import repository_loader,get_repo_name
from agent import agent_query

st.title("Chat with Github")

if 'flag' not in st.session_state:
    st.session_state['flag'] = True

url = st.sidebar.text_input("Github url")
if url and st.session_state.flag:
    with st.spinner('Embedding your Repository...'):
      os.environ["collection_name"] =url
      repository_loader(url)
      st.session_state.flag = False
    st.success('Done!')

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# React to user input
if prompt := st.chat_input("What is up?"):
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    if not url:
        st.warning('Please enter your Github Link!', icon='⚠')
    if url and os.getenv("collection_name"):
        with st.chat_message("assistant"):
          message_placeholder = st.empty()
          full_response = ""
        #   assistant_response =answer_query(prompt,url)
          assistant_response = agent_query(prompt)
        # Simulate stream of response with milliseconds delay
        # for chunk in assistant_response.split():
        #     full_response += chunk + " "
        #     time.sleep(0.05)
        #     # Add a blinking cursor to simulate typing
        #     message_placeholder.markdown(full_response + "▌")
        message_placeholder.markdown(assistant_response)
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": assistant_response})

    