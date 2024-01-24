# WIP

# The code in this file is related to ingesting data into the Pinecone vector database.
# This file will handle the generation of embeddings for the PDFs, and the storage of the embeddings in the Pinecone database.

import os
import json
import boto3
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_loaders import AmazonTextractPDFLoader
from pinecone_store import load_existing_index


def chunk_pdfs(pdf_path: str):
    """
    This function utilises AWS Textract to extract text from the PDFs.
    The text is then chunked into 512 word chunks using the RecursiveCharacterTextSplitter from Langchain.
    """

    textract_client = boto3.client("textract")
    # Chunk size and overlap values can be modified and tested to determine the optimal values.
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=512, chunk_overlap=0)
    chunks = []
    for pdf in os.listdir(pdf_path):
        full_path = pdf_path + pdf
        pdf_loader = AmazonTextractPDFLoader(full_path, client=textract_client)
        pdf_document = pdf_loader.load()
        document_chunks = text_splitter.split_documents(pdf_document)
        chunks.extend(document_chunks)
        print(f"Loaded {full_path}\n {len(document_chunks)} chunks")
    return chunks


def get_embeddings(chunks):
    """
    This function returns the embeddings generated for the supplied text chunks.
    The `batch_embeddings` function from `cohere_embeddings.py` is used to generate the embeddings.
    The chunks are flattened into a single list of strings containing the content of the `page_content` field of each chunk.
    """

    # The page_content field of each chunk contains the actual text extracted from the PDF
    # Other fields, such as page_number and other metadata, are not utilised for embedding generation
    # The metadata is used when creating entries in the Pinecone database, and can be seen in `store_embeddings()`
    chunk_text = [chunk.page_content for doc_chunks in chunks.values() for chunk in doc_chunks]
    embeddings = batch_embeddings(chunks)
    return embeddings


def store_embeddings(chunks, embeddings):

    document_ids = [str(i) for i in range(len(chunks))]

    index_name = "rag-test-cohere"

    pinecone_index = load_existing_index(index_name)

    metadata = [
        {
            "source": chunk.metadata.get("source", "unknown"),
            "page": chunk.metadata.get("page", 0),
            "text": chunk.page_content,
        }
        for chunk in chunks
    ]

    data_to_upsert = list(zip(document_ids, embeddings, metadata))
    batch_size = 12

    for i in range(0, len(data_to_upsert), batch_size):
        index_end = min(i + batch_size, len(data_to_upsert))
        batch = data_to_upsert[i:index_end]
        pinecone_index.upsert(items=batch)
