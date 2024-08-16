#pip install -U sentence-transformers
#pip install pyvi

# from sentence_transformers import SentenceTransformer
import torch
from transformers import AutoModel, AutoTokenizer

from preprocessing import preprocess_text

def model_embedding():
    # checkpoint_model = 'dangvantuan/vietnamese-embedding'  # 512 -> 768
    checkpoint_model = "VoVanPhuc/sup-SimCSE-VietNamese-phobert-base"  # 256 -> 768
    tokenizer = AutoTokenizer.from_pretrained(checkpoint_model) #vocab_size=64000, model_max_length=256 
    model = AutoModel.from_pretrained(checkpoint_model)
    # print(tokenizer)
    # print(model)
    return tokenizer, model

# Load model and embedding text funtion
def embedding_text(text, tokenizer, model):
    text = preprocess_text(text)
    inputs = tokenizer(text,padding=True, truncation=True, return_tensors="pt") #258
    
    # print(inputs.input_ids.shape,'=') #431
    #print(f"Token sau khi tokenizer: {tokenizer.tokenize(text)}",'==')
    print(f"Chiều dài token: {len(tokenizer.tokenize(text))}",'===')

    with torch.no_grad():
        embeddings = model(**inputs, output_hidden_states=True, return_dict=True).pooler_output

    return embeddings.numpy()[0].tolist()
            #torch.Tensor [1, 768] =>numpy.ndarray (1, 768)=> (768,) => list

if __name__=="__main__":
        
    text='''QUYẾT ĐỊNH
VỀ VIỆC CÔNG BỐ THỦ TỤC HÀNH CHÍNH NỘI BỘ MỚI BAN HÀNH VÀ SỬA ĐỔI, BỔ SUNG TRONG LĨNH VỰC THI ĐUA, KHEN THƯỞNG GIỮA CÁC CƠ QUAN, ĐƠN VỊ TRỰC THUỘC BỘ VĂN HÓA, THỂ THAO VÀ DU LỊCH
BỘ TRƯỞNG BỘ VĂN HÓA, THỂ THAO VÀ DU LỊCH
QUYẾT ĐỊNH:
Điều 1. Công bố kèm theo Quyết định này thủ tục hành chính nội bộ mới ban hành và sửa đổi, bổ sung trong lĩnh vực Thi đua, khen thưởng giữa các cơ quan, đơn vị trực thuộc Bộ Văn hóa, Thể thao và Du lịch.
Điều 2. Quyết định này có hiệu lực thi hành kể từ ngày ký.
Thủ tục hành chính lĩnh vực Thi đua, khen thưởng có số thứ tự 01, 02 điểm A1 mục A danh mục 1 ban hành kèm theo Quyết định số 786/QĐ-BVHTTDL ngày 31 tháng 3 năm 2023 của Bộ trưởng Bộ Văn hóa, Thể thao và Du lịch về việc công bố thủ tục hành chính nội bộ giữa các cơ quan, đơn vị trực thuộc Bộ và trong nội bộ cơ quan, đơn vị trực thuộc Bộ thuộc phạm vi chức năng quản lý của Bộ Văn hóa, Thể thao và Du lịch hết hiệu lực thi hành kể từ ngày Quyết định này có hiệu lực thi hành.
Điều 3. Chánh Văn phòng Bộ, Vụ trưởng Vụ Tổ chức cán bộ, Thủ trưởng các cơ quan, đơn vị thuộc Bộ chịu trách nhiệm thi hành Quyết định này./.
 
THỦ TỤC HÀNH CHÍNH NỘI BỘ MỚI BAN HÀNH VÀ SỬA ĐỔI, BỔ SUNG TRONG LĨNH VỰC THI ĐUA, KHEN THƯỞNG GIỮA CÁC CƠ QUAN, ĐƠN VỊ TRỰC THUỘC BỘ VĂN HÓA, THỂ THAO VÀ DU LỊCH
(Kèm theo Quyết định số 987/QĐ-BVHTTDL ngày 11 tháng 4 năm 2024 của Bộ trưởng Bộ Văn hóa, Thể thao và Du lịch)
PHẦN I
DANH MỤC THỦ TỤC HÀNH CHÍNH NỘI BỘ
1. Thủ tục hành chính nội bộ mới ban hành
    '''
    

    # print(text)
    # preprocessed_text= preprocess_text(text)
    # print(' preprocessed_text\n',  preprocessed_text)
    '''
    Công_bố kèm theo Quyết_định này thủ_tục hành_chính nội_bộ mới ban_hành và sửa_đổi bổ_sung trong lĩnh_vực Thi_đua khen_thưởng giữa các cơ_quan đơn_vị trực_thuộc Bộ Văn_hóa Thể_thao và Du_lịchh'''


    checkpoint_model = 'dangvantuan/vietnamese-embedding'  # 512 -> 768
    # checkpoint_model = "VoVanPhuc/sup-SimCSE-VietNamese-phobert-base"  # 256 -> 768
    embedded_text= embedding_text(text)
    print(len(embedding_text(text))) 
    '''
    tokenize:
    torch.Size([1, 32])
    ['Công_bố', 'kèm', 'theo', 'Quyết_định', 'này', 'thủ_tục', 'hành_chính', 'nội_bộ', 'mới', 'ban_hành', 'và', 'sửa_đổi', 'bổ_sung', 'trong', 'lĩnh_vực', 'Thi_đua', 'khen_thưởng', 'giữa', 'các', 'cơ_quan', 'đơn_vị', 'trực_thuộc', 'Bộ', 'Văn_@@', 'h@@', 'ó@@', 'a', 'Thể_thao', 'và', 'Du_lịch']

    
    giải thích vể tokenize:
    Vector 768 dimensions thường được sử dụng để biểu diễn văn bản có độ dài khoảng 256-512 tokens, tương đương với khoảng 200-400 từ tiếng Việt.
    
    Các mô hình như BERT, mBERT, và PhoBERT sử dụng kỹ thuật subword tokenization, cụ thể là Byte-Pair Encoding (BPE) hoặc WordPiece. Kỹ thuật này chia văn bản thành các phần nhỏ hơn gọi là subwords.
    
    Tuy nhiên, từ "Văn_hóa" bị tách thành các subwords: "Văn_@@", "h@@", "ó@@", "a". Điều này có thể là do từ "Văn_hóa" ít gặp hơn hoặc không có trong từ điển đầy đủ của tokenizer.
    @@: Ký hiệu này cho biết rằng phần trước của từ vẫn tiếp tục, và phần này không phải là một từ độc lập.

    muốn thêm từ Văn_hóa vào từ điển thì phải huấn luyện
    '''