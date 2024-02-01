# The code in this file is related to the creation of a retrieval QA chain.
# The retrieval QA chain is built using Langchain.
# The Pinecone vectorstore is used as a retriever and Cohere is used as an embedding model
# The chain handles the embedding of the user's question, the retrieval of the most similar document, and the answering of the question.

from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from cohere_embeddings import CustomCohereEmbeddings, fetch_cohere_key
from pinecone_store import CustomPineconeVectorstore, load_existing_index
from deploy_llm import build_sagemaker_llm_endpoint
import os
from dotenv import load_dotenv
load_dotenv()


def create_prompt_template():
    """
    This function creates a prompt template.
    The template is a string containing the text to be prepended to the user's question.
    The template also contains a placeholder for the user's question 
    and a placeholder for the context retrieved from the Pinecone index.
    """

    prompt_template = """
    Act as a helpful cyber security expert and answer the question below.
    If you do not know the answer to the question, explain that you do not know.
    Context is provided above the question and acts as additional information to complement your built-in knowledge.
    Utilise the context and your knowledge to answer the question and provide citations for any context used.

    Context: {context}

    Question: {question}

    Answer: 
    """

    prompt = PromptTemplate(
        template=prompt_template,
        input_variables=["context", "question"],
    )

    return prompt

    
def create_qa_chain():
    """
    This function generates the retrieval QA chain.
    The chain is built using Langchain.
    The Pinecone vectorstore is used as a retriever and Cohere is used as an embedding model.
    """
    cohere_api_key = fetch_cohere_key()
    embeddings = CustomCohereEmbeddings(
        model="embed-english-v3.0",
        cohere_api_key=cohere_api_key,
    )
    sagemaker_execution_role = os.environ.get("SAGEMAKER_EXECUTION_ROLE")
    llm = build_sagemaker_llm_endpoint(sagemaker_execution_role)
    index_name = "rag-test-cohere"
    pinecone_index = load_existing_index(index_name)
    text_field = "text"
    vectorstore = CustomPineconeVectorstore(pinecone_index, embeddings, text_field)
    prompt = create_prompt_template()

    chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=vectorstore.as_retriever(search_kwargs={"k": 1}),
        chain_type_kwargs={"prompt": prompt},
    )

    # The following code can be used to test the chain, however the chain object will be returned and used elsewhere.
    
    # query = "What is the purpose of security awareness?"

    # test_output = chain.run({"query": query})

    # print(test_output)

# create_qa_chain()