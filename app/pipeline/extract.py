import json
import os
import logging
from sqlalchemy import create_engine, text

DATA_DIR = "/app/data"
DB_URL = "mysql+pymysql://root:12345@ecommerce_mysql:3306/rag_chatbot_db"
engine = create_engine(DB_URL)
_logger = logging.getLogger(__name__)

def extract_products_data_to_jsonl(output_file: str):
    _logger.info("Starting multi-table data extraction from MySQL database.")
    
    try:
        with engine.connect() as connection:
            query = text("""
            SELECT 
                p.id, p.gender, p.masterCategory, p.subCategory, p.articleType, 
                p.baseColour, p.season, p.year, p.usage, p.productDisplayName,
                i.link AS image_url
            FROM products p
            INNER JOIN product_images i ON p.id = i.style_id
            """)

            result = connection.execute(query)
            
            with open(output_file, "w", encoding="utf-8") as f:
                for row in result:
                    safe_desc = row.productDisplayName if row.productDisplayName else "Unknown product"
                    safe_category = row.masterCategory if row.masterCategory else "Uncategorized"
                
                    context_text = (
                        f"Name: {safe_desc}. "
                        f"This is a {row.baseColour} {row.articleType} for {row.gender}, "
                        f"designed for {row.usage} wear in {row.season} {row.year}. "
                        f"Category: {row.masterCategory} - {row.subCategory}."
                    )
                
                    doc = {
                        "doc_id": f"prod_{row.id}", 
                        "content": context_text,
                        "metadata": {
                            "category": safe_category,
                            "type": "product_info",
                            "gender": row.gender,
                            "color": row.baseColour if row.baseColour else "Unknown",
                            "season": row.season if row.season else "Unknown",
                            "year": int(row.year) if row.year and str(row.year).isdigit() else 0,
                            "article_type": row.articleType if row.articleType else "Unknown",
                            "image_url": row.image_url
                        }
                    }
                    f.write(json.dumps(doc, ensure_ascii=False) + "\n")

            _logger.info(f"Extraction completed. Data saved to {output_file}")
            
    except Exception as e:
        _logger.error(f"Error during data extraction: {e}")
        raise

if __name__ == "__main__":
    output_file = os.path.join(DATA_DIR, "products_data_raw.jsonl")
    extract_products_data_to_jsonl(output_file)
    try: 
        extract_products_data_to_jsonl(output_file)

        print("\nTEST (PRINT 2 FIRST ROW)")
        if os.path.exists(output_file):
            with open(output_file, 'r', encoding = 'utf-8') as f:
                for i, line in enumerate(f):
                    if i<2:
                        parsed_json = json.loads(line)
                        print(json.dumps(parsed_json, indent = 2, ensure_ascii=False))
                    else:
                        break
    except Exception as e:
        print(f"TEST FAILED!: {e}")