# CONNECT
from qdrant_client import QdrantClient,models
import torch
from collecting_data_sql import data_sql

from model_embedding import embedding_text, model_embedding

import datetime



def create_vector_db(my_collection, dataset):
    #TẠO COLLECTION

    client.delete_collection(collection_name=my_collection)
    client.create_collection(
        collection_name=my_collection,
        vectors_config=models.VectorParams(size=768, distance=models.Distance.COSINE),
    )
    tokenizer, model = model_embedding()
    if client.collection_exists(collection_name=my_collection):
        print(my_collection," exists")

        client.upload_points(
            collection_name=my_collection,
            points=[
                models.PointStruct(
                    id=doc['KeyPK'],
                    vector=embedding_text(doc['ChunkingText'], tokenizer, model),
                    payload=doc,
                )for doc in dataset #if doc['KeyPK'] > 80000
            ],
        )
if __name__ == "__main__":
    start_time = datetime.datetime.now()


    

    client=QdrantClient(url="http://localhost:6333")
    dataset=data_sql()
    my_collection="Chunking_text_VBPL_v2"
    create_vector_db(my_collection, dataset)





    # Kết thúc đo thời gian
    end_time = datetime.datetime.now()
    # Tính toán thời gian thực thi
    elapsed_time = end_time - start_time
    # Tính giờ, phút, giây
    hours, remainder = divmod(elapsed_time.total_seconds(), 3600)
    minutes, seconds = divmod(remainder, 60)

    print(f"Thời gian chạy: {int(hours)} giờ {int(minutes)} phút {seconds:.2f} giây")