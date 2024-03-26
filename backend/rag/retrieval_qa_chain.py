# The code in this file is related to the creation of a retrieval QA chain.
# The retrieval QA chain is built using Langchain.
# The Pinecone vectorstore is used as a retriever and Cohere is used as an embedding model
# The chain handles the embedding of the user's question, the retrieval of the most similar document, and the answering of the question.

from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate, ChatPromptTemplate, MessagesPlaceholder
from common.custom_embeddings import CustomCohereEmbeddings
from common.fetch_keys import fetch_cohere_key
from common.custom_vectorstore import CustomPineconeVectorstore, load_existing_index
from langchain_core.runnables import RunnablePassthrough, RunnableParallel
from langchain_core.output_parsers import StrOutputParser
from build_llm_endpoint import build_sagemaker_llm_endpoint
import os
import logging
from dotenv import load_dotenv
load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


sagemaker_execution_role = os.environ.get("SAGEMAKER_EXECUTION_ROLE")
llm = build_sagemaker_llm_endpoint(sagemaker_execution_role)

def create_prompt_template():
    """
    This function creates a prompt template.
    The template is a string containing the text to be prepended to the user's question.
    The template also contains a placeholder for the user's question 
    and a placeholder for the context retrieved from the Pinecone index.

    Returns:
    - PromptTemplate: A Langchain prompt template object
    """

    prompt_template = """
    Act as a helpful cyber security expert and answer the question below.
    If you do not know the answer to the question, explain that you do not know.
    Use the following pieces of retrieved context to answer the question.
    Keep the answer concise and informative.


    Context: {context}
    """

    system_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", prompt_template),
            MessagesPlaceholder(variable_name="chat_history"),
            ("human", "{question}"),
        ]
    )

    # prompt = PromptTemplate(
    #     template=prompt_template,
    #     input_variables=["context", "question"],
    # )

    return system_prompt

def contextualize_prompt_and_history():
    """
    This function returns a chain that reformulates an incoming prompt.
    It utilises a message placeholder for the chat history and 
    features a system prompt that tells the model to reformulate the question.
    """

    system_prompt = """
    Given a conversation history and the latest human user question, which might reference context
    in the conversation history, create a standalone question which can be answered without the chat history.
    DO NOT answer the question, just reformulate it if needed, or return it as is.
    """
    contextualize_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system_prompt),
            MessagesPlaceholder(variable_name="chat_history"),
            ("human", "{question}")
        ]
    )
    contextualize_prompt_chain = contextualize_prompt | llm | StrOutputParser()
    return contextualize_prompt_chain

def contextualized_prompt(input: dict):
    context_chain = contextualize_prompt_and_history()
    if "chat_history" in input:
        return context_chain
    else:
        return input["question"]

def format_docs(docs):
    for doc in docs:
        logger.info(f"Doc: {doc}")
        logger.info(f"Page content: {doc.page_content}")
        logger.info(f"Metadata: {doc.metadata}")
    return "\n\n".join([f"{doc.page_content} (Metadata: {doc.metadata})" for doc in docs])
    
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

    index_name = "rag-index"
    pinecone_index = load_existing_index(index_name)
    text_field = "text"
    vectorstore = CustomPineconeVectorstore(pinecone_index, embeddings, text_field)
    retriever = vectorstore.as_retriever(search_kwargs={"k": 2})
    prompt = create_prompt_template()
    # handler = StdOutCallbackHandler() # Initialise an output callback handler for streaming

    rag_chain = (
        RunnablePassthrough.assign(
            context=contextualize_prompt_and_history | retriever | format_docs
        )
        | prompt
        | llm
    )

    return rag_chain

    # chain_from_docs = (
    #     RunnablePassthrough.assign(context=(lambda docs: format_docs(docs["context"])))
    #     | prompt
    #     | llm
    #     | StrOutputParser()
    # )

    # chain_with_source = RunnableParallel(
    #     {"context": retriever, "question": RunnablePassthrough()}
    # ).assign(answer=chain_from_docs)


    # chain = (
    #     {"context": vectorstore.as_retriever(search_kwargs={"k": 4}) | format_docs, "question": RunnablePassthrough()}
    #     | prompt
    #     | llm
    #     | StrOutputParser()
    # )

    # chain = RetrievalQA.from_chain_type(
    #     llm=llm,
    #     chain_type="stuff",
    #     retriever=vectorstore.as_retriever(search_kwargs={"k": 1}),
    #     chain_type_kwargs={"prompt": prompt},
    #     return_source_documents=True,
    # )

    return chain_with_source

    # The following code can be used to test the chain, however the chain object will be returned and used elsewhere.
    
    # query = "What is the purpose of security awareness?"

    # test_output = chain.run({"query": query})

    # print(test_output)
