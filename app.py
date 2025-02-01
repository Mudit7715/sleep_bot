import streamlit as st
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, Settings
from llama_index.llms.ollama import Ollama
from llama_index.core.query_engine import RetrieverQueryEngine
from llama_index.core.response_synthesizers import get_response_synthesizer
import os
import sys


# Access the API keys
openai_key = os.environ.get("OPENAI_API_KEY")

def main():

    # Configure Streamlit page
    st.set_page_config(page_title="Sleep Bot", page_icon="💤")
    
    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    rtf_path = "C:/Users/gupta/OneDrive/Desktop/LLMS/Multi-Agent/env/sleep_bot"

    # Display chat header
    st.title("Sleep Bot 💤")
    st.subheader("Your personal sleep assistant")

    documents = SimpleDirectoryReader(rtf_path).load_data()
    index = VectorStoreIndex.from_documents(documents)
    retriever = index.as_retriever(similarity_top_k=3)
    
    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])
    
    # Chat input and response
    if prompt := st.chat_input("How can I help you with your sleep?"):
        # Add user message
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.write(prompt)
        
        # Generate response using existing query engine
        response_synthesizer = get_response_synthesizer(response_mode="tree_summarize")
        query_engine = RetrieverQueryEngine(
            retriever=retriever,
            response_synthesizer=response_synthesizer,
        )
        response = query_engine.query(prompt)
        
        # Display assistant response
        with st.chat_message("assistant"):
            st.write(response.response)
        
        # Add assistant response to history
        st.session_state.messages.append({"role": "assistant", "content": response.response})

if __name__ == "__main__":
    main()
