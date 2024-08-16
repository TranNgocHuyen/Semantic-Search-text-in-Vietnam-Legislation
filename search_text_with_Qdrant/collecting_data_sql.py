import pyodbc # thư viện kết nối với csdl

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
        sql_query = "SELECT TOP 200000 *FROM [DataV03].[dbo].[Dataset_chunking_v2]"
        
        # Thực thi truy vấn
        cursor.execute(sql_query)
        # Lấy hàng từ tất cả
        rows = cursor.fetchall()

        data_json_new = []
        for row in rows:
            jsons = {
                'KeyPK': row[0],
                'ID': row[1],
                'TrichYeu': row[3],
                'UrlFileDoc': row[4],
                'ChunkingText': row[5] 
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
        array_id_vb=[]
        
        for i in dataset:
            print(f"ID {i['ID']}")
            if len(array_id_vb) ==0:
                array_id_vb.append(i['ID'])
            else:
                count =0
                for j in array_id_vb:
                    if i['ID'] == j:
                        count =count +1
                if count ==0:
                    array_id_vb.append(i['ID'])
        print(len(array_id_vb))