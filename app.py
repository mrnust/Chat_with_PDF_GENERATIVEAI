import streamlit as st
from langchain.vectorstores.cassandra import Cassandra
from langchain.indexes.vectorstore import VectorStoreIndexWrapper
from langchain.llms import OpenAI
from langchain.embeddings import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
import cassio
from PyPDF2 import PdfReader

# Initialize OpenAI
OPENAI_API_KEY = "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"
llm = OpenAI(openai_api_key=OPENAI_API_KEY)
embedding = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)

# Initialize Cassio with Astra DB credentials
ASTRA_DB_APPLICATION_TOKEN = "AstraCS:fQXcRdfxLhjzHgZWHZdILOwu:94209d2df354fd1475a6e177d3c41565ef3eccbc6f88f150e630801a276c0d44"
ASTRA_DB_ID = "a8db79b4-3f9c-4f78-ae32-0f0f8f43b866"
cassio.init(token=ASTRA_DB_APPLICATION_TOKEN, database_id=ASTRA_DB_ID)

# Initialize Cassandra Vector Store
astra_vector_store = Cassandra(
    embedding=embedding,
    table_name="qa_demo",  # Provide your Astra DB table name
    session=None,
    keyspace=None  # No need to specify, Astra DB manages the keyspace
)

# Function to upload PDF and store it in Astra DB
def upload_and_store_pdf(pdf_file):
    raw_text = ""
    pdf_reader = PdfReader(pdf_file)
    for page in pdf_reader.pages:
        raw_text += page.extract_text()
    texts = text_splitter.split_text(raw_text)
    astra_vector_store.add_texts(texts)

# Function to ask question and get response
def ask_question(question):
    try:
        response = astra_vector_index.query(question, llm=llm).strip()
        return response
    except Exception as e:
        print("Error querying Astra DB:", e)
        return "Sorry, there was an error processing your request. Please try again later."

# Initialize Vector Store Index
astra_vector_index = VectorStoreIndexWrapper(vectorstore=astra_vector_store)

# Initialize text splitter
text_splitter = CharacterTextSplitter(
    separator="\n",
    chunk_size=800,
    chunk_overlap=200,
    length_function=len
)

# Streamlit UI

st.set_page_config(page_title="Chat with PDF")

def main():
    st.title("PDF Q&A Chatbot")

    uploaded_file = st.file_uploader("Upload a PDF", type="pdf")
    if uploaded_file:
        st.success("PDF uploaded successfully!")
        upload_and_store_pdf(uploaded_file)
        st.success("PDF stored")

    st.write("You can now start asking questions.")

    question = st.text_input("Enter your question:")
    if st.button("Ask"):
        if question:
            answer = ask_question(question)
            st.write("Answer:", answer)
        else:
            st.warning("Please enter a question.")
    
if __name__ == "__main__":
    main()






#   only displays   chat bot -----------------------------------------------------
    

# import streamlit as st
# from langchain.vectorstores.cassandra import Cassandra
# from langchain.indexes.vectorstore import VectorStoreIndexWrapper
# from langchain.llms import OpenAI
# from langchain.embeddings import OpenAIEmbeddings
# from langchain.text_splitter import CharacterTextSplitter
# import cassio

# # Initialize OpenAI
# OPENAI_API_KEY = "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"
# llm = OpenAI(openai_api_key=OPENAI_API_KEY)
# embedding = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)

# # Initialize Cassio with Astra DB credentials
# ASTRA_DB_APPLICATION_TOKEN = "AstraCS:fQXcRdfxLhjzHgZWHZdILOwu:94209d2df354fd1475a6e177d3c41565ef3eccbc6f88f150e630801a276c0d44"
# ASTRA_DB_ID = "a8db79b4-3f9c-4f78-ae32-0f0f8f43b866"
# cassio.init(token=ASTRA_DB_APPLICATION_TOKEN, database_id=ASTRA_DB_ID)

# # Initialize Cassandra Vector Store
# astra_vector_store = Cassandra(
#     embedding=embedding,
#     table_name="qa_demo",  # Provide your Astra DB table name
#     session=None,
#     keyspace=None  # No need to specify, Astra DB manages the keyspace
# )

# # Function to ask question and get response
# def ask_question(question):
#     try:
#         response = astra_vector_index.query(question, llm=llm).strip()
#         return response
#     except Exception as e:
#         print("Error querying Astra DB:", e)
#         return "Sorry, there was an error processing your request. Please try again later."

# # Initialize Vector Store Index
# astra_vector_index = VectorStoreIndexWrapper(vectorstore=astra_vector_store)

# # Initialize text splitter
# text_splitter = CharacterTextSplitter(
#     separator="\n",
#     chunk_size=800,
#     chunk_overlap=200,
#     length_function=len
# )

# # Streamlit UI
# def main():
#     st.title("PDF Q&A Chatbot")

#     st.write("You can now start asking questions.")

#     question = st.text_input("Enter your question:")
#     if st.button("Ask"):
#         if question:
#             answer = ask_question(question)
#             st.write("Answer:", answer)
#         else:
#             st.warning("Please enter a question.")
    
# if __name__ == "__main__":
#     main()

