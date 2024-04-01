from backend.scraper.cybok_scraper import CybokScraper
# from backend.scraper.cisa_scraper import CisaScraper
from backend.scraper.cve_scraper import CveScraper
from vectorisation.cohere_embeddings import batch_embeddings
from vectorisation.pinecone_store import load_pinecone_index
import uuid
import argparse

def fetch_all_content(selected_scrapers):
    # Fetch all the content from the different sources
    # Map each scraper to its corresponding adapter function
    scraper_to_adapter_map = {
        "cybok": (CybokScraper(), adapt_cybok_data),
        "cve": (CveScraper(), adapt_cve_data),
        # "cisa": (CisaScraper(), adapt_cisa_data)
    }

    all_content = []
    for scraper_name in selected_scrapers:
        if scraper_name not in scraper_to_adapter_map:
            raise ValueError(f"Scraper {scraper_name} not found in scraper_to_adapter_map")
        scraper, adapter_function = scraper_to_adapter_map[scraper_name]
        print(f"Fetching content from {scraper_name} scraper")
        content = scraper.extract_all_data()
        print(f"Adapting content from {scraper_name} scraper")
        adapted_content = adapter_function(content)
        all_content.extend(adapted_content)
    return all_content

def chunk_text(text, title, chunk_size=1024):
    """
    Chunk the text into chunks of approximately chunk_size characters
    while maintaining whole words.
    
    Parameters:
    - text (str): The text to chunk

    Returns:
    - List[str]: List of chunks
    """
    full_text = f"title: {title} text: {text}"
    words = full_text.split()
    chunks = []
    current_chunk = []

    for word in words:
        if len(" ".join(current_chunk)) + len(word) < chunk_size:
            current_chunk.append(word)
        else:
            chunks.append(" ".join(current_chunk))
            current_chunk = [word]
    
    if current_chunk:
        chunks.append(" ".join(current_chunk))

    return chunks

## Adapter functions to ensure congruency between the data from different sources
def adapt_cybok_data(cybok_data):
    adapted_data = []
    for chapter in cybok_data:
        # CyBOK chapter text can be quite long, so we chunk it into smaller pieces (1024 chars each) for embedding
        text_chunks = chunk_text(chapter["text"], chapter["title"], chunk_size=1024)
        for chunk in text_chunks:
            adapted_data.append({
                "text": chunk,
                "metadata": {
                    "source": chapter["source"],
                    "title": chapter["title"],
                }
            })
    return adapted_data

def adapt_cve_data(cve_data):
    adapted_data = []
    for item in cve_data:
        # Combine the description, id, and other metadata into a single text for embedding
        # This ensures things like the CVE ID are included in the embedding,
        # which is useful for similarity search
        combined_text = f"CVE ID: {item['cve_id']} Description: {item['description']} Affected Products: {item['affected_products']} Published Date: {item['published_date']}" 
        adapted_data.append({
            "text": combined_text,
            "metadata": {
                "id": item["cve_id"],
                "published_date": item["published_date"],
                "affected_products": item["affected_products"],
                "references": item["references"],
            }
        })
    return adapted_data


def batch_upsert_to_pinecone(index, embeddings, all_content, batch_size=12):
    """
    Upserts embeddings and corresponding metadata to the Pinecone index
    in batches of batch_size
    
    Parameters:
    index (pinecone.Index): Pinecone index to upsert to
    embeddings (List[np.array]): List of embeddings to upsert
    chunks (List[Dict]): List of text and metadata to upsert

    Returns:
    None
    """
    for i in range(0, len(embeddings), batch_size):
        batch_embeddings = embeddings[i:i+batch_size]
        batch_chunks = all_content[i:i+batch_size]
        print(f"Upserting batch {i} to {i+batch_size}")
        vectors_to_upsert = [{
            "id": str(uuid.uuid4()),
            "values": embedding,
            "metadata": {
                **chunk["metadata"],
                "text": chunk["text"] # Add the text key to the metadata for Pinecone's similarity search
            }
        } for embedding, chunk in zip(batch_embeddings, batch_chunks)]
        index.upsert(vectors_to_upsert)

def main(selected_scrapers):
    print(f"Running scrapers: {selected_scrapers}")
    all_content = fetch_all_content(selected_scrapers=selected_scrapers)
    print("Chunking and embedding content")
    # Embed only the text-based content (i.e. description, extracted text, etc)
    chunk_texts_to_embed = [item["text"] for item in all_content]
    embeddings = batch_embeddings(chunk_texts_to_embed)
    print(f"Generated {len(embeddings)} embeddings.")
    print("Loading Pinecone index")
    index = load_pinecone_index("rag-index")
    print("Upserting embeddings to Pinecone index")
    batch_upsert_to_pinecone(index, embeddings, all_content)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run specific data scrapers and upsert to Pinecone index.")
    parser.add_argument("--scrapers", nargs="+", help="The scrapers to run. Options: cybok, cve, cisa")
    args = parser.parse_args()
    selected_scrapers = args.scrapers

    main(selected_scrapers)



