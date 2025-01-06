import streamlit as st
from dotenv import load_dotenv
from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.vectorstores import FAISS
# from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_huggingface import HuggingFaceEndpoint
from langchain.memory import ConversationBufferMemory
from langchain.chains.conversational_retrieval.base import ConversationalRetrievalChain
from langchain_core.prompts import PromptTemplate
from htmlTemplates import css, bot_template, user_template
import os

def get_pdf_text(pdf_docs):
    text = ""
    for pdf in pdf_docs:
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages:
            text += page.extract_text()
    return text

def get_text_chunks(raw_text):
    text_splitter = CharacterTextSplitter(separator="\n", chunk_size=800, chunk_overlap=150, length_function=len)
    chunks = text_splitter.split_text(raw_text)
    return chunks

@st.cache_resource
def get_vectors(text_chunks):
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    vectors = FAISS.from_texts(texts=text_chunks, embedding=embeddings)
    return vectors

def get_conversation(vectors):
    llm = HuggingFaceEndpoint(
        repo_id="mistralai/Mistral-7B-Instruct-v0.3",
        temperature=0.5,
        model_kwargs={
            "max_length": 1024
        },
        huggingfacehub_api_token=os.environ.get("HF_TOKEN")
    )
    
    memory = ConversationBufferMemory(memory_key='chat_history', return_messages=True)
    
    CUSTOM_PROMPT_TEMPLATE = """
        Use the pieces of information provided in the context to answer user's question.
        If you don't know the answer, just say that you don't know. Don't try to make up an answer.
        Provide only the information within the given context.

        Context: {context}
        Question: {question}
        
        Start the answer directly. Avoid small talk.
    """
    
    prompt = PromptTemplate(template=CUSTOM_PROMPT_TEMPLATE, input_variables=["context", "question"])
    
    conversation_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=vectors.as_retriever(search_kwargs={'k': 3}),
        memory=memory,
        combine_docs_chain_kwargs={"prompt": prompt}
    )
    
    return conversation_chain

def handle_userinput(user_question):
    if st.session_state.conversation is not None:
        response = st.session_state.conversation({'question': user_question})
        # print(response)
        if 'answer' in response:
            st.write(bot_template.replace("{{MSG}}", response['answer']), unsafe_allow_html=True)
            st.session_state.messages.append({'role': 'assistant', 'content': response['answer']})
            
        else:
            st.error("No answer found in the response.")
    else:
        st.error("Conversation chain is not initialized. Please upload and process documents first.")
def main():
    load_dotenv()
    st.set_page_config(page_title="Chat with Multiple PDFs", page_icon="🤖", layout="wide")
    st.title("🤖 AI Chatbot Assistant")
    st.write(css, unsafe_allow_html=True)

    if "conversation" not in st.session_state:
        st.session_state.conversation = None

    if 'messages' not in st.session_state:
        st.session_state.messages = []

    st.markdown("<h1 style='color: #fff; text-align: center;'>Chat with Multiple PDFs</h1>", unsafe_allow_html=True)

    # Chat message display
    for message in st.session_state.messages:
        with st.chat_message(message['role']):
            st.markdown(message['content'])

    user_question = st.chat_input("Ask a question about your documents:")

    if user_question:
        st.write(user_template.replace("{{MSG}}", user_question), unsafe_allow_html=True)
        st.session_state.messages.append({'role': 'user', 'content': user_question})
        handle_userinput(user_question)

    with st.sidebar:
        st.subheader("Your Documents")
        pdf_docs = st.file_uploader("Upload your PDFs here and click on process", accept_multiple_files=True)
        if st.button("Process"):
            with st.spinner("Processing"):
                raw_text = get_pdf_text(pdf_docs)
                chunks = get_text_chunks(raw_text)
                vectors = get_vectors(chunks)
                st.session_state.conversation = get_conversation(vectors)
                st.success("Documents processed successfully! The bot is ready to answer your questions.")

if __name__ == '__main__':
    main()


