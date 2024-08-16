
import re
import os
import win32com.client as win32
from win32com.client import constants
#pip pypiwin32

def save_as_docx(file_path):
    word = win32.gencache.EnsureDispatch('Word.Application')
    try: 
        doc = word.Documents.Open(file_path)
        doc.Activate ()

        # Rename
        new_file_abs = os.path.abspath(file_path)
        new_file_abs = re.sub(r'\.\w+$', '.docx', new_file_abs)

        # Save and Close
        word.ActiveDocument.SaveAs(
            new_file_abs, FileFormat=constants.wdFormatXMLDocument
        )
        doc.Close(False)
        
        os.remove(file_path)
        print(f"Converted and Removed file doc: {file_path}")
        
    except:
        word.Quit()
        os.remove(file_path)
        print(f"Removed file Error Open: {file_path}")


def convert_doc_to_docx(folder_path):

    files = os.listdir(folder_path)

    for file in files:
        file_path = os.path.join(folder_path, file)

        if re.search(r'\(1\)', file_path):
            os.remove(file_path)
            print(f"Removed same file: {file}")
            
        else:
            name, duoi = file.split('.')
            if(duoi == 'doc'):
                print(f"Processing file doc: {file}")
                save_as_docx(file_path)
                
        
if __name__=="__main__":
    folder_path = "D:\\NLP\\process_van_ban\\data_1_00\\"
    convert_doc_to_docx(folder_path)