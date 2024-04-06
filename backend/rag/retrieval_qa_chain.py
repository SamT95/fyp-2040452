# The code in this file is related to the creation of a retrieval QA chain.
# The retrieval QA chain is built using Langchain.
# The Pinecone vectorstore is used as a retriever and Cohere is used as an embedding model
# The chain handles the embedding of the user's question, the retrieval of the most similar document, and the answering of the question.

from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate, ChatPromptTemplate, MessagesPlaceholder
from common.custom_embeddings import CustomCohereEmbeddings
from common.fetch_keys import fetch_cohere_key
from common.custom_vectorstore import CustomPineconeVectorstore, load_existing_index
from langchain_core.runnables import RunnablePassthrough, RunnableParallel, Runnable, RunnableConfig
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.output_parsers import StrOutputParser
from langchain_community.chat_message_histories import DynamoDBChatMessageHistory
from build_llm_endpoint import build_sagemaker_llm_endpoint
from langchain_cohere import ChatCohere
from operator import itemgetter
from typing import Any, Optional
import os
import logging
from dotenv import load_dotenv
load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

cohere_api_key = fetch_cohere_key()
os.environ["COHERE_API_KEY"] = cohere_api_key
sagemaker_execution_role = os.environ.get("SAGEMAKER_EXECUTION_ROLE")
llm = build_sagemaker_llm_endpoint(sagemaker_execution_role)
chat_llm = ChatCohere(model="command", max_tokens="512",  temperature="0.1")

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
contextualize_prompt_chain = contextualize_prompt | chat_llm | StrOutputParser()


def contextualized_prompt(input: dict):
    if "chat_history" in input:
        return contextualize_prompt_chain
    else:
        return input["question"]

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

    class CustomRunnable(Runnable):
        async def invoke(self, input: Any, config: Optional[RunnableConfig] = None) -> dict:
            context = input["context"]
            question = input["question"]
            llm_output = prompt | llm
            return {
                "context": context,
                "question": question,
                "answer": llm_output
            }
            

    context_chain = itemgetter("question") | retriever | format_docs

    first_step = RunnablePassthrough.assign(context=context_chain)

    passthrough_with_context = RunnablePassthrough.assign(
        context=context_chain,
        question=itemgetter("question")
    )

    chain = ({
        "context": itemgetter("question") | retriever | format_docs,
        "question": itemgetter("question"),
        "chat_history": itemgetter("chat_history")
    } | RunnableParallel({
        "answer": prompt | llm,
        "context": itemgetter("context")
    })
    )

    # chain = first_step | prompt | llm 

    # final_chain = RunnableParallel({
    #     "answer": chain,
    #     "context": itemgetter("context")
    # })

    # final_chain = {
    #     "context": retriever | format_docs,
    #     "question": RunnablePassthrough(),
    # } | RunnablePassthrough.assign(answer=chain)
    # final_chain = RunnablePassthrough.assign(answer=chain, source_documents=context_chain)

    chain_with_history = RunnableWithMessageHistory(
        chain,
        lambda session_id: DynamoDBChatMessageHistory(
            table_name=table_name,
            session_id=session_id,
            key=dynamo_db_key
        ),
        input_messages_key="question",
        history_messages_key="chat_history",
        output_messages_key="answer"
    )

    return chain_with_history

    # rag_chain = (
    #     RunnablePassthrough.assign(
    #         context=contextualized_prompt | retriever
    #     )
    #     | RunnablePassthrough.assign(context = lambda docs: format_docs(docs["context"]) )
    #     | RunnablePassthrough.assign(response = lambda prompt: chat_llm(prompt) )
    # )

    # return rag_chain

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

    # return chain_with_source

    # The following code can be used to test the chain, however the chain object will be returned and used elsewhere.
    
    # query = "What is the purpose of security awareness?"

    # test_output = chain.run({"query": query})

    # print(test_output)
