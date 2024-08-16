import os
os.environ["KMP_DUPLICATE_LIB_OK"]="TRUE"
# from sklearn.model_selection import train_test_split # Thư viện chia tách dữ liệu
import re
from pyvi.ViTokenizer import tokenize

'''
https://ayselaydin.medium.com/1-text-preprocessing-techniques-for-nlp-37544483c007
https://www.analyticsvidhya.com/blog/2021/06/text-preprocessing-in-nlp-with-python-codes/
B1: Chunking (đã làm trong xử lý văn bản => đẩy lên database)
B2: text_cleaning
    Loại bỏ loại bỏ các số, ký tự đặc biệt và dấu câu không cần thiết. use re
B3: Tokenize use underthesea/ pyvi
B4: Loại bỏ stopword ( vì có 1 số từ dừng nhg nằm trong từ ghép)
B5: Creating Document Keyword Matrix (Tạo ma trận từ khóa tài liệu)
Mô tả: Tạo ra ma trận từ khóa tài liệu, trong đó mỗi hàng đại diện cho một tài liệu và mỗi cột đại diện cho một từ khóa, giá trị tại mỗi ô là tần suất xuất hiện của từ khóa đó trong tài liệu.
'''


# B1+B2
# process document

def processing_document(document):
    # tinh chỉnh để cắt đoanj
    document = document.replace("\n\xa0\n", "\n")\
                        .replace("\n- ", " ")\
                        .replace("\n+ ", " ")\
                        .replace("đ)", "d)")
                                                                            
    document=re.sub(r'\n[a-z]\) ', ".",document)
    document = re.sub(r'[\…]', '', document)
    
    
    # xóa dòng k cần thiết
    document = re.sub(r'\n_+\n', '\n', document)

    # thay đổi dấu câu về chấm
    document = document.replace("...", ".")\
                        .replace("(...)", ".")\
                        .replace("!", ".")\
                        .replace("?", ".") \
                        .replace("..",".")
    
    # thay đổi kí tự lạ
    document = document.replace("\xa0", " ")\
                        .replace(".)", ")")\
                        .replace("v.v.",".")\
                        .replace("\t", " ")
    # xóa khoảng cách liên tiếp
    #document = re.sub(r'\s+', ' ', document)
    document = document.replace("\n\n", "\n")
    document = re.sub(r'\.{2,}','.' , document)               
    return document

def clean_text(text):
    text = processing_document(text)
    # xóa xuống dòng
    text=text.replace("\n"," ")

    # xóa các mục lục đầu dòng
    text = re.sub(r'\d\.\s*', '', text)

    text=re.sub(r'\(\d\) ', " ",text)
    text = re.sub(r'\b([0-9]|1[0-9]|20) \b', ' ', text)

    # Sử dụng biểu thức chính quy để thay thế các ký tự đặc biệt bằng khoảng trắng
    text = re.sub(r'[,\t;“:”\'"!?\-?\[\]|\n\(\)\.\*\/]', ' ', text)

    # Thay thế các khoảng trắng liên tiếp bằng một khoảng trắng duy nhất
    text = re.sub(r'\s+', ' ', text)

    return text.lower()

# B3: Loại bỏ stopword
def remove_stopword(text):
    words_list = text.split()

    with open("/home/tuanda/Semantic-Search-in-Vietnam-Legislation/search_text_with_Qdrant/vietnamese-stopwords.txt", encoding='utf-8') as f:
        stopwords=f.read()                                                                                                                                                                                                                                          
    filtered_words= [i for i in words_list if i not in stopwords]

    filtered_text = ' '.join(filtered_words)

    return filtered_text
# B4 : tokenizer

def tokenize_pyvi(text):
    processed_text = tokenize(text)
    return processed_text


# Preprocess_text function
def preprocess_text(text):
    cleaned_text=clean_text(text) # B1+B2
    tokenized_text=tokenize_pyvi(cleaned_text) # B4 
    filtered_text=remove_stopword(tokenized_text)   # B3 vì có một số từ khi ghép lại thì ko còn là stopword nứa
    return filtered_text

if __name__=='__main__':
    #text='Thủ tục hành chính và lĩnh vực Thi đua  khen thưởng có số thứ tự 01  02 điểm A1 mục A danh mục 1 ban hành kèm theo Quyết định số 786 QĐ BVHTTDL ngày 31 tháng 3 năm 2023 của Bộ trưởng Bộ Văn hóa  Thể thao và Du lịch về việc công bố thủ tục hành chính nội bộ giữa các cơ quan  đơn vị trực thuộc Bộ và trong nội bộ cơ quan  đơn vị trực thuộc Bộ thuộc phạm vi chức năng quản lý của Bộ Văn hóa  Thể thao và Du lịch hết hiệu lực thi hành kể từ ngày Quyết định này có hiệu lực thi hành'
    text = '''
        QUYẾT ĐỊNH
VỀ VIỆC CÔNG BỐ THỦ TỤC HÀNH CHÍNH NỘI BỘ MỚI BAN HÀNH VÀ SỬA ĐỔI, BỔ SUNG TRONG LĨNH VỰ LỊCH
BỘ TRƯỞNG BỘ VĂN HÓA, THỂ THAO VÀ DU LỊCH
QUYẾT ĐỊNH:
Điều 1. Công bố kèm theo Quyết định này thủ tục hành chính nội bộ mới ban hành và sửa đổ Văn hóa, Thể thao và Du lịch.
Điều 2. Quyết định này có hiệu lực thi hành kể từ ngày ký.
Thủ tục hành chính lĩnh vực Thi đua, khen thưởng có số thứ tự 01, 02 điểm A1 mục A danh 
trưởng Bộ Văn hóa, Thể thao và Du lịch về việc công bố thủ tục hành chính nội bộ giữa cáhạm vi chức năng quản lý của Bộ Văn hóa, Thể thao và Du lịch hết hiệu lực thi hành kể từ
Điều 3. Chánh Văn phòng Bộ, Vụ trưởng Vụ Tổ chức cán bộ, Thủ trưởng các cơ quan, đơn vị 

THỦ TỤC HÀNH CHÍNH NỘI BỘ MỚI BAN HÀNH VÀ SỬA ĐỔI, BỔ SUNG TRONG LĨNH VỰC THI ĐUA, KHEN 
(Kèm theo Quyết định số 987/QĐ-BVHTTDL ngày 11 tháng 4 năm 2024 của Bộ trưởng Bộ Văn hóa
PHẦN I
DANH MỤC THỦ TỤC HÀNH CHÍNH NỘI BỘ
1. Thủ tục hành chính nội bộ mới ban hành
(1) Danh hiệu “Cờ thi đua của Bộ” được xét tặng vào dịp kết thúc năm công tác hoặc kết t, khen thưởng.
(2) Danh hiệu “Cờ thi đua của Bộ” được xét tặng cho tập thể dẫn đầu phong trào thi đua thong trào.
* Đối tượng xét tặng danh hiệu “Cờ thi đua của Bộ” là các tập thể tiêu biểu, dẫn đầu pho, bao gồm: Cơ quan, đơn vị thuộc Bộ; Phòng thuộc các cơ quan, đơn vị thuộc Bộ.Căn cứ phágày 31/12/2023 của Chính phủ quy định chi tiết thi hành một số điều của Luật Thi đua, khhể thao và Du lịch quy định về công tác thi đua, khen thưởng Ngành văn hóa, thể thao và 
Mẫu số 01
TỜ TRÌNH
Về việc đề nghị khen thưởng .5./tặng (truy tặng) danh hiệu.6.
Kính gửi: .
Căn cứ Luật Thi đua, khen thưởng ngày 15/6/2022;
Căn cứ  7. quy định chức năng, nhiệm vụ, quyền hạn và cơ cấu tổ chức của. 2 .;
Căn cứ . 8. ; .2 kính trình .:
Xét tặng/truy tặng (danh hiệu .6 ) cho. tập thể/ hộ gia đình/.cá nhân.
Hoặc xét, tặng/truy tặng (hình thức khen thưởng của Chính phủ, Thủ tướng Chính phủ 9) ch
        '''
    print(preprocess_text(text))

