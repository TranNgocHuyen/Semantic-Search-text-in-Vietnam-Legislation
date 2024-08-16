import pyodbc
import csv
import re
import json
import docx

def tach(data):
    arr1 = []
    arr2 = []
    arr3 = []
    data = data.split('.')
    regex_nb = r"(\d+)"
    for data1 in data:
        data_new1 = data1.split('\n')
        for cau in data_new1:
            if(len(cau) > 15):
                arr1.append(cau)
    
    for data2 in arr1:
        data_new2 = data2.split(':')
        for cau in data_new2:
            if(len(cau) > 15):
                arr2.append(cau)
    for data3 in arr2:
        data_new3 = data3.split(';')
        for cau in data_new3:
            if(len(cau) > 15):
                row = cau.replace(",", " ").replace(".", " ") \
                     .replace(";", " ").replace("“", " ") \
                     .replace(":", " ").replace("”", " ") \
                     .replace('"', " ").replace("'", " ") \
                     .replace("!", " ").replace("?", " ") \
                     .replace("-", " ").replace("?", " ") \
                     .replace("]"," ").replace("["," ") \
                     .replace("|", " ").replace("\n", " ") \
                     .replace("a)", " ").replace("b)", " ") \
                     .replace("c)", " ").replace("d)", " ") \
                     .replace('e)', " ").replace("f)", " ") \
                     .replace("g)", " ").replace("h)", " ") \
                     .replace("i)", " ").replace("k)", " ") \
                     .replace("l)", " ").replace("m)", " ") \
                     .replace("A)", " ").replace("B)", " ") \
                     .replace("C)", " ").replace("D)", " ") \
                     .replace('E)', " ").replace("F)", " ") \
                     .replace("G)", " ").replace("H)", " ") \
                     .replace("I)", " ").replace("K)", " ") \
                     .replace("L)", " ").replace("M)", " ") \
                     .replace("“", " ").replace("”", " ") \
                     .replace("đ)", " ").replace("n)", " ") \
                     .replace("o)", " ").replace("q)", " ") \
                     .replace("p)", " ").replace("x)", " ") \
                     .replace("O)", " ").replace("Q)", " ") \
                     .replace("P)", " ").replace("X)", " ") \
                     .replace("N)", " ").replace("_", "") \
                     .replace('(1)', "").replace('(2)', "") \
                     .replace('(3)', "").replace('(4)', "")\
                     .replace('(5)', "").replace('(6)', "") \
                     .replace('(7)', "").replace('(8)', "") \
                     .replace('(9)', "").replace('(10)', "") \
                     .replace('(11)', "").replace('(12)', "") \
                     .replace('(13)', "").replace('(14)', "") \
                     .replace('(15)', "").replace('(16)', "") \
                     .replace('(17)', "").replace('(18)', "") \
                     .replace('(19)', "").replace('(20)', "") \
                     .replace('(21)', "").replace('(22)', "") \
                     .replace('(23)', "").replace('(24)', "") \
                     .replace('(25)', "").replace('(26)', "") \
                     .replace('(27)', "").replace('(28)', "") \
                     .replace('(29)', "").replace('(30)', "") \
                     .replace('(31)', "").replace('(32)', "") \
                     .replace('(33)', "").replace('(34)', "") \
                     .replace('(35)', "").replace('(36)', "") \
                     .replace('(37)', "").replace('(38)', "") \
                     .replace('(39)', "").replace('(40)', "") \
                     .replace('(41)', "").replace('(42)', "") \
                     .replace('(43)', "").replace('(44)', "") \
                     .replace('(45)', "").replace('(46)', "") \
                     .replace('(47)', "").replace('(48)', "") \
                     .replace('(49)', "").replace('(50)', "") \
                     .replace('(51)', "").replace('(52)', "") \
                     .replace('(53)', "").replace('(54)', "") \
                     .replace('(55)', "").replace('(56)', "") \
                     .replace('(57)', "").replace('(58)', "") \
                     .replace('(59)', "").replace('(60)', "") \
                     .replace('(61)', "").replace('(62)', "") \
                     .replace('(63)', "").replace('(64)', "") \
                     .replace('(65)', "").replace('(66)', "") \
                     .replace('(67)', "").replace('(68)', "") \
                     .replace('(69)', "").replace('(70)', "") \
                     .replace('*', "")
                if(len(row) > 15):
                    arr3.append(row)
    return arr3

def value(ch):
   val = -1
   if(ch=='I'):
      val = 1
   if(ch=='V'):
      val = 5
   if(ch=='X'):
      val = 10
   if(ch=='L'):
      val = 50
   if(ch=='C'):
      val = 100
   if(ch=='D'):
      val = 500
   if(ch=='M'):
      val = 1000
   return val
def convertRomanToDecimal(str):
   decVal = 0
   i = 0
   n = len(str)
   while (i < n): 
       current = value(str[i])
 
       if (i + 1 < n): 
         next = value(str[ i + 1 ]) 
         if (current >= next): 
            decVal = decVal + current
            i = i + 1
         else:
            decVal = decVal + next - current
            i = i + 2
       else:
          decVal = decVal + current
          i = i + 1 
   return decVal


# def chuong(txt):
#    data_text = txt.split("\nChương ")
#    arrs = []
#    for i in range(len(data_text)):
#       if(i>0):
#          lines = data_text[i].split('\n')
#          list_tx = lines.copy()
#          list_tx[0] = ""
#          list_tx[1] = ""
#          new_text = "\n".join(list_tx)
#          new_text = new_text.replace("\n\n", "\n")
#          clause_number = convertRomanToDecimal(lines[0])
#          if(int(clause_number) > 0):
#             if(clause_number < 10):
#                ids = str(clause_number)
#                new_ar = [{
#                   "id" : ids,
#                   "name_chapter" : lines[1],
#                   "content" : new_text
#                }
#                ]
#                arrs.append(new_ar[0])
#             else:
#                ids = str(clause_number)
#                new_ar = [{
#                   "id" : ids,
#                   "name_chapter" : lines[1],
#                   "content" : new_text
#                }
#                ]
#                arrs.append(new_ar[0])
#          else:
#             json_chung = json.dumps(arrs)
#             data = json.loads(json_chung)
#             lines2 = data[(i-2)]
#             lines2['content'] = lines2['content'] + new_text
         
#    return arrs

# def muc(arrs):
#    json_chung = json.dumps(arrs)
#    data = json.loads(json_chung)

#    for person in data:
#       data_content = person["content"].split("\nMục ")
#       number_muc = len(data_content)
#       if(number_muc > 1):
#          list_tx = data_content.copy()
#          content_muc = []
#          for i in range(len(list_tx)):
#             if(i > 0):
#                new_list = list_tx[i].split("\n")
#                list_copy = new_list.copy()
#                list_copy[0] = ''
#                content_dieu = '\n'.join(list_copy)
#                title_muc = new_list[0].split(".")
#                if(title_muc[0].isdigit() and int(title_muc[0]) < 10):
#                   id_muc = int(title_muc[0])*1000
#                elif(title_muc[0].isdigit() and int(title_muc[0]) >= 10):
#                   id_muc = int(title_muc[0])*1000 
#                if(len(title_muc) > 1):
#                   name_muc = title_muc[1]
#                else:
#                   name_muc = title_muc
#                new_content = [{
#                   "id_muc" : id_muc,
#                   "name_muc" : name_muc,
#                   "content_muc" : content_dieu
#                }]
#                content_muc.append(new_content[0])
#          person["content"] = content_muc
#       else:
#          new_content = [{
#             "id_muc" : 0,
#             "name_muc" : '',
#             "content_muc" : person["content"]
#          }]
#          person["content"] = new_content
   
#    return data

# def dieu(arr):
#    json_chung = json.dumps(arr)
#    data_json = json.loads(json_chung)
#    for person in data_json:
#       mucs = person["content"]
#       for data_muc in mucs:
#          data_content_replace = data_muc["content_muc"].replace("\nĐiều", "\nĐiều").replace("\n\x07\n\x07Điều", "\nĐiều")
#          data_content = data_content_replace.split("\nĐiều ")
#          list_tx = data_content.copy()
#          content_dieu = []
#          ids = []
#          for i in range(len(list_tx)):
#             if(i > 0):
#                list_id = list_tx[i].split(".")
#                ids.append(list_id[0])
#                id_dieu = 0
#                if(list_id[0].isdigit()):
#                   id_dieu = int(list_id[0])
#                new_list = tach(list_tx[i])
#                new_content = [{
#                   "id_dieu" : str(id_dieu),
#                   "content_dieu" : new_list
#                }]
#                content_dieu.append(new_content[0])
#          data_muc["content_muc"] = content_dieu
#    return data_json

# def no_dieu(arr):
#    json_chung = json.dumps(arr)
#    data_json = json.loads(json_chung)
#    for person in data_json:
#       mucs = person["content"]
#       for data_muc in mucs:
#          list_tx = data_muc["content_muc"]
#          content_dieu = []
#          new_list = tach(list_tx)
#          new_content = [{
#             "id_dieu" : 0,
#             "content_dieu" : new_list
#          }]
#          content_dieu.append(new_content[0])
#          data_muc["content_muc"] = content_dieu
#    return data_json

def read_docx_file(filename):
   try:
      document = docx.Document(filename)
      full_text = ""
      for paragraph in document.paragraphs:
         full_text += paragraph.text + "\n"
      return full_text.strip()
   except FileNotFoundError:
      print(f"Error: File '{filename}' not found.")
      return None

# def cut_data(name_file):
#    file_names = name_file.replace('.doc', '')
#    new_path = 'D:/vbpl_project/data_1_30/' + file_names + '.docx'
#    text = read_docx_file(new_path)
#    regex_chuong = r"\nChương [A-Z]"
#    regex_muc = r"\nMục \d+"
#    regex_dieu = r"\nĐiều \d+."
   
#    data_arr = []
#    if(re.search(regex_chuong, text)):
#       data_chuong = chuong(text)
#       if(re.search(regex_muc, text)):
#          data_muc = muc(data_chuong)
#          if(re.search(regex_dieu, text)):
#             data_arr = dieu(data_muc)
#       else:
#             data_arr = dieu(data_muc)
#    elif(re.search(regex_muc, text)):
#       new_arrs = [{
#          "id" : "0",
#          "name_chapter" : '',
#          "content" : text
#       }]
#       data_muc = muc(new_arrs)
#       if(re.search(regex_dieu, text)):
#          data_arr = dieu(data_muc)
#    elif(re.search(regex_dieu, text)):
#       new_arrs = [{
#          "id" : "0",
#          "name_chapter" : '',
#          "content" : [{
#             "id_muc" : "0",
#             "name_muc" : '',
#             "content_muc" : text
#          }]
#       }]
#       data_arr = dieu(new_arrs)
#    else:
#       pattern = r"^.*?(?=\bnăm\s+(\d{4}))"

#       match = re.findall(pattern, text, flags=re.DOTALL)
#       modified_text = ''
#       if match:
#          year = match[0]
#          remove_pattern = r"^.*?(?=năm\s+" + year + ")"
#          modified_text = re.sub(remove_pattern, "", text, flags=re.DOTALL)
#       else:
#          print("No 'năm' and year found in the text.")
#       lines = modified_text.split('\n')
#       data_text = ''
#       for i in range(len(lines)):
#          lines = ''
#          data_text = "\n".join(lines)
#       new_arrs = [{
#          "id" : "0",
#          "name_chapter" : '',
#          "content" : [{
#             "id_muc" : "0",
#             "name_muc" : '',
#             "content_muc" : data_text
#          }]
#       }]
#       data_arr = no_dieu(new_arrs)
#    json_new = json.dumps(data_arr)
#    data_json = json.loads(json_new)
#    return data_json

connection_string = (
    "DRIVER={ODBC Driver 17 for SQL Server};"  # Adjust driver name if needed
    f"SERVER={'10.0.0.39'};"
    f"DATABASE={'DataV03'};"
    f"UID={'sa'};"
    f"PWD={'Ab@123456'}"
)

try:
    connection = pyodbc.connect(connection_string)
    cursor = connection.cursor()

    # Your SQL query here
    sql_query = "SELECT * FROM [DataV03].[dbo].[VanBans]"  # Replace with your actual query

    cursor.execute(sql_query)
    rows = cursor.fetchall()
    
    with open('data.csv', 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['ID', 'SoHieu', 'LoaiVanBan', 'NoiBanHanh', 'NguoiKy', 'NgayBanHanh', 'NgayHieuLuc', 'NgayCongBao', 'SoCongBao', 'TinhTrang', 'Chuong', 'Muc', 'Dieu', 'NoiDung'])
        for row in rows:
            name_files = row[10]
            # name_files = '01_2022_TT-BTP_502821.doc'
            new_name = name_files.replace("Đ", "D")
            json_data = cut_data(new_name)
            json_data = cut_data(new_name)
            json_new = json.dumps(json_data)
            data_json = json.loads(json_new)
            id_chuong = ''
            id_muc = ''
            id_dieu = ''
            content_dieu = []
            print(row[10])
            for chapter in data_json:
                id_chuong = chapter["id"]
                for mucs in chapter["content"]:
                    id_muc = mucs["id_muc"]
                    for dieus in mucs["content_muc"]:
                        id_dieu = dieus["id_dieu"]
                        content_dieu = dieus["content_dieu"]
                        for cau in content_dieu:
                            data = [row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], id_chuong, id_muc, id_dieu, cau]
                            writer.writerow(data)
                           
                           
except pyodbc.Error as ex:
    print("Error connecting to SQL Server:", ex)

finally:
    if cursor:
        cursor.close()
    if connection:
        connection.close()