import unittest
from unittest.mock import patch, MagicMock
from rag.retrieval_qa_chain import create_qa_chain, format_docs, create_prompt_template
from langchain.docstore.document import Document
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder, SystemMessagePromptTemplate, HumanMessagePromptTemplate

def normalize_whitespace(text):
    return " ".join(text.split())

class TestRetrievalQAChain(unittest.TestCase):
    @patch('rag.retrieval_qa_chain.load_existing_index')
    @patch('rag.retrieval_qa_chain.CustomCohereEmbeddings')
    @patch('rag.retrieval_qa_chain.CustomPineconeVectorstore')
    @patch('rag.retrieval_qa_chain.create_prompt_template')
    @patch('rag.retrieval_qa_chain.create_history_aware_retriever')
    @patch('rag.retrieval_qa_chain.create_stuff_documents_chain')
    @patch('rag.retrieval_qa_chain.RunnableWithMessageHistory')
    @patch('rag.retrieval_qa_chain.DynamoDBChatMessageHistory')
    def test_create_qa_chain(self, mock_dynamodb, mock_runnable, mock_create_stuff_documents_chain,
                             mock_create_history_aware_retriever, mock_create_prompt_template,
                             mock_custom_vectorstore, mock_custom_embeddings, mock_load_existing_index):
        # Mock the necessary dependencies
        mock_dynamodb.return_value = MagicMock()
        mock_runnable.return_value = MagicMock()
        mock_create_stuff_documents_chain.return_value = MagicMock()
        mock_create_history_aware_retriever.return_value = MagicMock()
        mock_create_prompt_template.return_value = MagicMock()
        mock_custom_vectorstore.return_value = MagicMock()
        mock_custom_embeddings.return_value = MagicMock()
        mock_load_existing_index.return_value = MagicMock()

        # Call the function under test
        result = create_qa_chain("table_name", "session_id", "conversation_id")

        # Assert that the necessary dependencies were called with the correct arguments
        # mock_dynamodb.assert_called_once_with(table_name="table_name", session_id="session_id",
                                            #   key={"user_id": "session_id", "conversation_id_timestamp": "conversation_id"})
        mock_runnable.assert_called_once()
        mock_create_stuff_documents_chain.assert_called_once()
        mock_create_history_aware_retriever.assert_called_once()
        mock_create_prompt_template.assert_called_once()
        mock_custom_vectorstore.assert_called_once()
        mock_custom_embeddings.assert_called_once()
        mock_load_existing_index.assert_called_once()

        # Assert that the function returned the expected result
        self.assertIsInstance(result, MagicMock)

    def test_format_docs(self):
        # Create a list of Document objects
        docs = [
            Document(page_content="This is the first document", metadata={"title": "Document 1"}),
            Document(page_content="This is the second document", metadata={"title": "Document 2"})
        ]

        # Define the expected formatted docs string
        expected_docs = "This is the first document (Metadata: {'title': 'Document 1'})\n\nThis is the second document (Metadata: {'title': 'Document 2'})"

        # Call the function under test
        result = format_docs(docs)

        # Assert that the function returned the expected result
        self.assertEqual(result, expected_docs)

    def test_create_prompt_template(self):
        # Call the function under test
        result = create_prompt_template()

        # Assert that the function returned a ChatPromptTemplate object
        self.assertIsInstance(result, ChatPromptTemplate)

        # Assert that the prompt template has the correct structure
        self.assertIsInstance(result[0], SystemMessagePromptTemplate)
        self.assertIsInstance(result[1], MessagesPlaceholder)
        self.assertIsInstance(result[2], HumanMessagePromptTemplate)

        # Assert that the prompt template has the correct messages
        system_message = result[0].prompt
        system_instructions = """
        Act as a helpful cyber security expert and answer the question below.
        If you do not know the answer to the question, explain that you do not know.
        Use the following pieces of retrieved context to answer the question.

        Context: {context}
        """
        normalized_system_instructions = normalize_whitespace(system_instructions)
        normalized_system_message = normalize_whitespace(system_message.template)
        self.assertEqual(normalized_system_message, normalized_system_instructions)
        self.assertEqual(system_message.input_variables, ['context'])

        # Assert that the prompt template has the correct placeholders
        history_placeholder = result[1]
        self.assertEqual(history_placeholder.input_variables, ["chat_history"])
        human_message = result[2]
        self.assertEqual(human_message.input_variables, ["input"])
        self.assertEqual(human_message.prompt.template, "{input}")

if __name__ == '__main__':
    unittest.main()


