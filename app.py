import streamlit as st
import os
from rag_engine import load_and_index_data, get_query_engine

st.title("💰 Financial Report Analyst")

# File upload sidebar
with st.sidebar:
    st.header("Upload Document")
    uploaded_file = st.file_uploader("Upload a PDF", type=["pdf"])
    
    if uploaded_file and st.button("Process File"):
        with st.spinner("Reading complex tables..."):
            # Save temp file - LlamaParse needs a file path not bytes
            with open("temp.pdf", "wb") as f:
                f.write(uploaded_file.getbuffer())
            
            # Index the document
            load_and_index_data("temp.pdf")
            st.success("File indexed! Ask away.")
            
            # Cleanup
            os.remove("temp.pdf")

# Chat interface
if "messages" not in st.session_state:
    st.session_state.messages = []

# Show chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Handle new messages
if prompt := st.chat_input("Ask a question about the PDF..."):
    # Add user message to history
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate response
    with st.chat_message("assistant"):
        query_engine = get_query_engine()
        response = query_engine.query(prompt)
        st.markdown(response.response)
        
    # Add assistant response to history
    st.session_state.messages.append({
        "role": "assistant", 
        "content": response.response
    })