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
    result = searching_text_to_doc (json_text["ChunkingText"], my_collection, 1, tokenizer, model)
    if result[0]["id"] == json_text["ID"]:
        print("True",result[0]["score"] )
        score_array.append(result[0]["score"])
        
        # print("search: ",json_text["ChunkingText"])
        # print("result: ",result[0]["ChunkingText"])

        accuracy = accuracy + 1
        score = score + result[0]["score"]
    else:
        print("False")
    print(score_array)
print(f"accuracy =  {accuracy}") 
print(f"accuracy/total =  {accuracy/len(dataset_test)}")
print(f"score/accuracy {score/accuracy}")
torch.save(score_array,'score_array.pt')

# Kết thúc đo thời gian
end_time = datetime.datetime.now()
# Tính toán thời gian thực thi
elapsed_time = end_time - start_time
# Tính giờ, phút, giây
hours, remainder = divmod(elapsed_time.total_seconds(), 3600)
minutes, seconds = divmod(remainder, 60)

print(f"Thời gian chạy: {int(hours)} giờ {int(minutes)} phút {seconds:.2f} giây")

'''
accuracy =  4711
accuracy/total =  0.9422
score/accuracy 0.6820208023774146
Thời gian chạy: 0 giờ 39 phút 49.42 giây
'''