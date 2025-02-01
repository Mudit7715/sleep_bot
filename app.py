import streamlit as st
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, Settings
from llama_index.core.query_engine import RetrieverQueryEngine
from llama_index.core.response_synthesizers import get_response_synthesizer
import os
import sys

def get_data_path():
    # Get the directory where the script is located
    script_dir = Path(__file__).parent.absolute()
    
    # Look for data files in the same directory as the script
    data_files = list(script_dir.glob("*.rtf"))
    
    if not data_files:
        # If no RTF files found in script directory, try a 'data' subdirectory
        data_dir = script_dir / "data"
        if not data_dir.exists():
            raise ValueError(f"No RTF files found in {script_dir} or {data_dir}")
        data_files = list(data_dir.glob("*.rtf"))
        if not data_files:
            raise ValueError(f"No RTF files found in {data_dir}")
            
# Access the API keys
openai_key = os.environ.get("OPENAI_API_KEY")

def main():

    # Configure Streamlit page
    st.set_page_config(page_title="Sleep Bot", page_icon="💤")
    
    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    rtf_path = get_data_path()

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
