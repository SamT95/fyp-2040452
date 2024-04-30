# The code in this file is related to the creation of a retrieval QA chain.
# The retrieval QA chain is built using Langchain.
# The Pinecone vectorstore is used as a retriever and Cohere is used as an embedding model
# The chain handles the embedding of the user's question, the retrieval of the most similar document, and the answering of the question.

from langchain.chains import create_retrieval_chain, create_history_aware_retriever
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from common.custom_embeddings import CustomCohereEmbeddings
from common.fetch_keys import fetch_cohere_key, fetch_key
from common.custom_vectorstore import CustomPineconeVectorstore, load_existing_index
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_community.chat_message_histories import DynamoDBChatMessageHistory
from build_llm_endpoint import build_sagemaker_llm_endpoint
import os
import logging
from dotenv import load_dotenv
load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

cohere_api_key = fetch_key("rag/CohereKeyProd", "COHERE_API_KEY")
os.environ["COHERE_API_KEY"] = cohere_api_key
langsmith_api_key = fetch_key("rag/LangsmithKey", "LANGSMITH_API_KEY")
os.environ["LANGSMITH_API_KEY"] = langsmith_api_key
os.environ["LANGCHAIN_TRACING_V2"] = "true"
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
    You have up-to-date knowledge on cyber security and vulnerabilities.
    If the question asks about recent vulnerabilities, you should be able to provide the latest information,
    so long as it is provided in the context.
    If the question asks about a specific vulnerability, you should be able to provide detailed information about it.
    If the question asks about new vulnerabilities, you should use the context to provide the most recent information,
    or explain that you do not have the information.
    Use the following pieces of retrieved context to answer the question.

    Context: {context}
    """

    system_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", prompt_template),
            MessagesPlaceholder(variable_name="chat_history"),
            ("human", "{input}"),
        ]
    )

    return system_prompt


def format_docs(docs):
    for doc in docs:
        logger.info(f"Doc: {doc}")
        logger.info(f"Page content: {doc.page_content}")
        logger.info(f"Metadata: {doc.metadata}")
        logger.info(f"Formatted: {doc.page_content} (Metadata: {doc.metadata})")
    return "\n\n".join(f"{doc.page_content} (Metadata: {doc.metadata})" for doc in docs)
    
def create_qa_chain(table_name, session_id, conversation_id):
    """
    This function generates the retrieval QA chain.
    The chain is built using Langchain.
    The Pinecone vectorstore is used as a retriever and Cohere is used as an embedding model.
    """
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

    dynamo_db_key = {
        "user_id": session_id,
        "conversation_id_timestamp": conversation_id
    }

    contextualize_question_prompt = """
    Given a conversation history and the latest human user question, which might reference content
    in the conversation history, create a standalone question which can be answered without the chat history.
    IMPORTANT! DO NOT answer the question, just reformulate it if needed, or return it as is.
    NEVER generate an answer to the incoming prompt.
    If the question relates to new vulnerabilities, reformulate the question
    to ask about new CVEs. If the question is about a specific CVE, ask about the details of the CVE.
    """
    contextualize_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", contextualize_question_prompt),
            MessagesPlaceholder(variable_name="chat_history"),
            ("human", "{input}")
        ]
    )
    context_aware_retriever = create_history_aware_retriever(
        llm,
        retriever,
        contextualize_prompt,
    )

    qa_chain = create_stuff_documents_chain(llm, prompt)

    rag_chain = create_retrieval_chain(context_aware_retriever, qa_chain)

    chain_with_history = RunnableWithMessageHistory(
        rag_chain,
        lambda session_id: DynamoDBChatMessageHistory(
            table_name=table_name,
            session_id=session_id,
            key=dynamo_db_key
        ),
        input_messages_key="input",
        history_messages_key="chat_history",
        output_messages_key="answer"
    )

    return chain_with_history