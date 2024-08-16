import json
from text_search import searching_text_to_doc #(text_query, my_collection, limit, tokenizer, model)
import datetime
from model_embedding import model_embedding
import torch

start_time = datetime.datetime.now()

path_json = "/home/tuanda/Semantic-Search-in-Vietnam-Legislation/search_text_with_Qdrant/dataset_test_5000.json"

with open(path_json, 'r') as file:
    dataset_test = json.load(file) 

        
my_collection="Chunking_text_VBPL"
tokenizer, model = model_embedding()
accuracy =0 
score =0 
score_array= []
for (i,json_text) in enumerate(dataset_test):
    print(i+1,"===========")
    results = searching_text_to_doc (json_text["ChunkingText"], my_collection, 3, tokenizer, model)
    
    for result in results:
        if result["id"] == json_text["ID"]:
            print("True", result["score"])
            score_array.append(result["score"])
            accuracy = accuracy + 1
            continue
        
print(f"accuracy =  {accuracy}") 
print(f"accuracy/total =  {accuracy/len(dataset_test)}")
print(f"len(score_array) = {len(score_array)}")
print(f"score/accuracy = {sum(score_array)/len(score_array)}")
torch.save(score_array,'score_array_limit_3.pt')


# Kết thúc đo thời gian
end_time = datetime.datetime.now()
# Tính toán thời gian thực thi
elapsed_time = end_time - start_time
# Tính giờ, phút, giây
hours, remainder = divmod(elapsed_time.total_seconds(), 3600)
minutes, seconds = divmod(remainder, 60)

print(f"Thời gian chạy: {int(hours)} giờ {int(minutes)} phút {seconds:.2f} giây")

'''accuracy =  4955
accuracy/total =  0.991
score/accuracy 0.6835519677093844
Thời gian chạy: 0 giờ 38 phút 29.13 giây'''