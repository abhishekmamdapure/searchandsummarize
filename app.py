import streamlit as st
import time 
import pandas as pd
from openai_valid import GPTValidator
from sentence_transformers import SentenceTransformer
embeddings_model = SentenceTransformer('multi-qa-mpnet-base-dot-v1')

import faiss
index_file = "faiis_index_book.index"
book_index = faiss.read_index(index_file)

import json 
with open('extracted_data.json','r') as w:
    data = json.load(w)

text_to_search = list(data.values())

def get_search(query, topK):
    query_embedding = embeddings_model.encode([query])
    distances, indices = book_index.search(query_embedding, topK)
    res = [text_to_search[i] for i in indices[0]]
    return "         ".join(res)


PROMPT = """Generate the summary of given set of documents into around {} sentences or less.
Do not behave in assertive tone, just give the summary.
Do not add any other pre and post text. Do not explain for every individual documents. 
Summary sould be combined from all the documents. Do not start your summary by "document says this" or "document discuss this".
Here are the documents: {}\n\n"""
# Set a title and description

st.markdown(
    """
    <style>
    .logo {
        position: absolute;
        top: 10px; /* Adjust the top position as needed */
        right: 10px; /* Adjust the right position as needed */
        width: 100px; /* Adjust the width as needed */
        height: auto; /* Maintain aspect ratio */
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Display the logo image with the "logo" class
st.image("logo.png",output_format="PNG",width=200)

st.title("Book Search Engine by i/oFactory")
st.write("Ask anything about the book and get your summarized answers. ")

api_key = st.sidebar.text_input("Enter your OpenAI API key \n\n (only uses gpt-3.5-turbo)")
api_key_valid = bool(api_key)  # Check if API key is provided

col1, col2 = st.columns([3, 3])

with col1:
    query = st.text_input("Enter your text query:")
    
    
    

    def process_query(query):
        # Simulate loading by adding a sleep here
        res = get_search(query=query,topK=k_value)

        summary = GPTValidator(sys_PROMPT=PROMPT.format(length,res),usr_PROMPT="Generated Summary:", model = "gpt-3.5-turbo",OPENAI_API_KEY=api_key)

        return summary

# Column 2: Image and Summary
with col2:
    
    cover_image = "881719.jpg"
    if cover_image:
        st.image(cover_image, caption="ML Handbook", width=200)

    k_value = st.slider("Top documents to choose", min_value=3, max_value=10, value=7)
    length = st.slider("Length of the Generated Summary", min_value=3, max_value=20, value=5)
# Add some advanced styling
st.markdown(
    """
    <style>
        .stButton > button {
            background-color: #FF5733;
            color: white;
            border: none;
            border-radius: 5px;
            padding: 10px 20px;
            font-size: 16px;
            cursor: pointer;
        }
        .stButton > button:hover {
            background-color: #FF4500;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# Button to trigger query processing
if st.button("Process Query", key="process_query_button", disabled=not api_key_valid):
    if query:
        with st.spinner("Generating..."):
            output = process_query(query)
        st.success("Generated Summary:")
        st.write(output)
    else:
        st.warning("Please enter a query before processing.")


st.markdown("***")
data = {
    "Sample Input": ["What is cross-validation ? ","What is over-fitting ?", "Evaluation metrics for classification problem"]}

# Create a DataFrame from the data
df = pd.DataFrame(data)

# Display the table at the bottom
st.table(df)