import json
import os
import logging
from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

INPUT_FILE = "/app/data/products_data_raw.jsonl" 
COLLECTION_NAME = "rag_chatbot_vector_database_products"
VECTOR_SIZE = 768  # kích thước của mô hình BAAI/bge-base-en-v1.5 

def main():
    logger.info("Loading embedding model BAAI/bge-base-en-v1.5...")
    model = SentenceTransformer('BAAI/bge-base-en-v1.5')
    
    logger.info("Connecting to Qdrant Vector DB...")
    qdrant_client = QdrantClient(host="qdrant_vectoer_db", port=6333) 
    
    try:
        qdrant_client.get_collection(collection_name=COLLECTION_NAME)
        logger.info(f"Collection '{COLLECTION_NAME}' already exists.")
    except Exception:
        logger.info(f"Creating a new Collection '{COLLECTION_NAME}' with {VECTOR_SIZE} dimensions...")
        qdrant_client.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=VectorParams(size=VECTOR_SIZE, distance=Distance.COSINE)
        )

    if not os.path.exists(INPUT_FILE):
        logger.error(f"File {INPUT_FILE} not found.")
        return

    # đọc file, embedding văn bản thành vector 
    logger.info("Starting embedding and data ingestion process into Vector DB...")
    points = []
    
    with open(INPUT_FILE, 'r', encoding='utf-8') as f:
        for idx, line in enumerate(f):
            data = json.loads(line)
            
            # chuỗi văn bản cần làm embedding
            text_to_embed = data["content"]
            
            # chuyển văn bản thành vector 768 chiều
            vector = model.encode(text_to_embed).tolist()
            
            # đóng gói theo qdrant point
            point = PointStruct(
                id=idx,  
                vector=vector,
                payload={
                    "doc_id": data["doc_id"],
                    "content": data["content"],
                    **data["metadata"]  # giữ lại các trường lọc: category, color, gender, image_url...
                }
            )
            points.append(point)
            
            # đẩy theo cụm 64 sản phẩm 
            if len(points) >= 64:
                qdrant_client.upsert(collection_name=COLLECTION_NAME, points=points)
                logger.info(f"Successfully ingested {idx + 1}...")
                points = []  
                
        # còn lại
        if points:
            qdrant_client.upsert(collection_name=COLLECTION_NAME, points=points)
            logger.info("Done!")

if __name__ == "__main__":
    main()