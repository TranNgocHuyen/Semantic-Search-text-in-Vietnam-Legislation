import pyodbc # thư viện kết nối với csdl
import json

connection_string = (
    "DRIVER={ODBC Driver 17 for SQL Server};"
    f"SERVER={'10.0.0.39'};"    # địa chỉ máy chủ
    f"DATABASE={'DataV03'};"    # tên csdl
    f"UID={'sa'};"              # tên user
    f"PWD={'Ab@123456'}"        # mật khẩu
)

def data_sql():
    try:
        # thiết lập kết nối
        connection = pyodbc.connect(connection_string)
        # tạo 1 con trỏ để thực hiện các lệnh SQL và truy vấn kết quả
        cursor = connection.cursor()

        # CHỌN DATABASE CÂU 'data_ND' ?ĐIỀU 'data_ND_dieu' ?ĐOẠN   
        sql_query = "SELECT TOP 100 *FROM [DataV03].[dbo].[Dataset_chunking_v2]"
        
        # Thực thi truy vấn 
        cursor.execute(sql_query)
        # Lấy hàng từ tất cả
        rows = cursor.fetchall()

        data_json_new = []
        for row in rows:
            jsons = {
                'KeyPK': row[0],
                'ID': row[1],
                'TrichYeu': row[2],
                'UrlFileDoc': row[3],
                'ChunkingText': row[4] 
            }
            data_json_new.append(jsons)
        return data_json_new
    
    except pyodbc.Error as ex:
        print("Error connecting to SQL Server:", ex)

    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()


if __name__=='__main__':
    dataset=data_sql()
    for i in dataset:
        print("=============")
        print(i['ChunkingText'])
    # json_file=open("dataset_test_5000.json","w")

    # json.dump(dataset,json_file, indent=4)

    # print("Conversion to JSON completed successfully.")  

# 6090
'''
json_file=open("dataset.json","w")

json.dump(data,json_file, indent=4)

print("Conversion to JSON completed successfully.")   
'''