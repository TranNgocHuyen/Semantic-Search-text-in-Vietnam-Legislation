import docx
import os

import re

# pip install --quiet langchain
# pip install --quiet -U langchain-community
from langchain_text_splitters import CharacterTextSplitter, RecursiveCharacterTextSplitter

import pyodbc

import datetime

# lấy tên, title và content
def read_file_docx(folder_path, file_name):
    file_path = os.path.join(folder_path, file_name)
    print(file_path)
    #check file và đường dẫn file        
    if os.path.exists(file_path):
        
        print("File docx "+file_name+ " exist")
        try: 
            full_text = ""
            document = docx.Document(file_path) # là 1 đối tượng
            for paragraph in document.paragraphs:
                if search_remove_line(paragraph.text) is not True:
                    full_text += paragraph.text + "\n"
            full_text = full_text.strip()#.replace('\n', '\\n')
            return full_text
        
        except FileNotFoundError:
            print(f"Error: File '{file_name}' not found.")
            return None
    else:
        print("File docx "+file_name+ " didn't exist")
        return None


# process document
def search_remove_line(line):
    # Biểu thức chính quy để tìm các thành phần "Căn cứ vào" hoặc "Căn cứ theo"
    pattern = re.compile(r'\bCăn cứ (Hiến pháp|Luật|Nghị|Thông|Pháp lệnh)\b')

    # Tìm kiếm tất cả các thành phần khớp
    match = re.search(pattern, line)

    pattern_2 = re.compile(r'\bTheo đề nghị của\b')
    match_2 = re.search(pattern_2, line)

    if match or match_2:
        return True

        
def processing_document(document):
    # tinh chỉnh để cắt đoanj
    document = document.replace("\n\xa0\n", "\n")\
                        .replace("\n- ", ".")\
                        .replace("\n+ ", ".")\
                        .replace("đ)", "d)")
    document = re.sub(r"(Điều \d+)\.", r"\1", document)                                                                        
    document=re.sub(r'\n[a-z]\) ', ".",document)
    document = re.sub(r'[\…]', '', document)  
    document = re.sub(r'[□]', '', document)
    
    
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
    document = document.replace("\n\n", "\n")\
                        .replace("\n.\n", "\n")
    document = re.sub(r'\.{2,}','.' , document)               
    return document

# chunking document
def chunking_document(document):
    text_splitter = RecursiveCharacterTextSplitter(
        separators=["\n\n","\n",".",";"],
        chunk_size=1500,
        chunk_overlap=200
    )
    split_texts = text_splitter.split_text(document)
    
    # for text in split_texts:
    #     print(text)
    #     print(len(text.split()))
    return split_texts

def get_list_chunking_texts(folder_path, file_name):
    original_document = read_file_docx(folder_path, file_name)
    #print(original_document)
    if original_document is not None:
        processed_document = processing_document(original_document)
        
        list_chunked_document = chunking_document(processed_document)
        return list_chunked_document
    else:
        return None
'''
folder_path = "D:\\NLP\\process_van_ban\\data_1_00\\"
folder = os.listdir(folder_path)

'''
# đẩy Nhãn+ Nội dung văn bản vào json
def push_dataset(folder_path):
    # connection 
    connection_string = (
        "DRIVER={ODBC Driver 17 for SQL Server};"  # Adjust driver name if needed
        f"SERVER={'10.0.0.39'};"
        f"DATABASE={'DataV03'};"
        f"UID={'sa'};"
        f"PWD={'Ab@123456'}"
    )
    try:
        # thiết lập kết nối
        connection = pyodbc.connect(connection_string)
        # tạo 1 con trỏ để thực hiện các lệnh SQL và truy vấn kết quả
        cursor = connection.cursor()

        #Tạo 1 db mới để ghi dữ liệu vào:
        create_table_query = """
            CREATE TABLE Dataset_chunking (
                KeyPK INT PRIMARY KEY,
                ID INT,
                TrichYeu NVARCHAR(MAX),
                UrlFileDoc NVARCHAR(100),
                ChunkingText NVARCHAR(MAX)
            );
         """
        cursor.execute(create_table_query)
        connection.commit()
        print("Table 'Dataset_chunking' created successfully.")
        insert_query = f"""
                        INSERT INTO Dataset_chunking (KeyPK, ID, TrichYeu, UrlFileDoc, ChunkingText)
                        VALUES (?, ?, ?, ?, ?);
                    """

        #Truy cập db đã tồn tại
        sql_query = "SELECT * FROM [DataV03].[dbo].[VanBans]"     
        # Thực thi truy vấn
        cursor.execute(sql_query)
        # Lấy hàng từ tất cả
        rows = cursor.fetchall()
        i = 1
        id = 1
        for row in rows:
            print(i," =====")
            i = i + 1
            # Láy name file từ db
            file_name = row[10]
            #print(row)
            if file_name != None:
                # chỉnh sửa name_file cho khop
                new_file_name = file_name.replace("Đ", "D").replace("_m", "").replace('.doc', '.docx')
                print(new_file_name)
                list_chunking_texts = get_list_chunking_texts(folder_path, new_file_name)   
                if list_chunking_texts is not None:
                    for text in list_chunking_texts:
                        if len(text.split())>10:
                            data_to_insert = [id, int(row[0]),row[12], new_file_name, text]
                            id = id + 1
                            data_to_insert = [data_to_insert] # vì yêu cầu vào là list
                            cursor.executemany(insert_query, data_to_insert)
                            connection.commit()
                else:
                    continue
            print(f"Done {new_file_name}")
            

    except pyodbc.Error as ex:
        print("Error connecting to SQL Server:", ex)

    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()


if __name__ == "__main__":

    '''
    folder_path = "D:\\NLP\\process_van_ban\\data_1_00\\"
    folder = os.listdir(folder_path)
    '''
    start_time = datetime.datetime.now()
    folder_path = "D:\\NLP\\process_van_ban\\data_1_00\\"

    #push_dataset(folder_path)

    file_name = "987_QD_BVHTTDL_606009.docx"
    for i in get_list_chunking_texts(folder_path, file_name):
        print("=============")
        if len(i.split())>10:
            i = clean_text(i) 
            print([i])

    # Kết thúc đo thời gian
    end_time = datetime.datetime.now()
    # Tính toán thời gian thực thi
    elapsed_time = end_time - start_time
    # Tính giờ, phút, giây
    hours, remainder = divmod(elapsed_time.total_seconds(), 3600)
    minutes, seconds = divmod(remainder, 60)

    print(f"Thời gian chạy: {int(hours)} giờ {int(minutes)} phút {seconds:.2f} giây")
