import streamlit as st
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, Settings
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
    
    rtf_path = "."

    # Display chat header
    st.title("Sleep Bot 💤")
    st.subheader("Your personal sleep assistant")

    documents = SimpleDirectoryReader(rtf_path).load_data()
    index = VectorStoreIndex.from_documents(documents)
    retriever = index.as_retriever(streaming = True ,similarity_top_k=2)
    
    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])
    
    # Chat input and response
   # Chat input and response
    if prompt := st.chat_input("How can I help you with your sleep?"):
        # Add user message
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.write(prompt)
        
        try:
            # Generate response using streaming
            response_synthesizer = get_response_synthesizer(
                response_mode="tree_summarize",
                streaming=True
            )
            query_engine = RetrieverQueryEngine(
                retriever=retriever,
                response_synthesizer=response_synthesizer,
            )
            
            # Stream response
            with st.chat_message("assistant"):
                response_placeholder = st.empty()
                full_response = ""
                
                # Get streaming response
                streaming_response = query_engine.query(prompt)
                for chunk in streaming_response.response_gen:
                    if chunk:
                        full_response += chunk
                        response_placeholder.markdown(full_response + "▌")
                
                # Display final response
                response_placeholder.markdown(full_response)
            
            # Add complete response to history
            st.session_state.messages.append({
                "role": "assistant", 
                "content": full_response
            })

        except Exception as e:
            st.error(f"Error generating response: {str(e)}")
                    
if __name__ == "__main__":
    main()
