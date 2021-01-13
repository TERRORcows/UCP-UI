#import srctools
from zipfile import ZipFile

# Script to generate info.txt and editoritems.txt

def _genInfoStr(ucp):
    temp = f'''//Created with UCP-UI
"ID"    "{ucp['id']}"
"Name"  "{ucp['title']}"
"Desc"  "{ucp['description']}"


'''
    for item in ucp['items']:
        temp += '''
"Item"
    {
    "ID"    "'''+str(item['id'])+'''"
    "Version"
        {
        "Styles"
            {
            "BEE2_CLEAN"    "'''+str(item['id'])+'''"
            }
        }
    }
'''
    return temp

def _genEditoritemsStr(item):
    pass

def genFiles(ucp,zipname):
    with ZipFile(zipname,'w') as file:
        file.writestr('info.txt',_genInfoStr(ucp))
        for item in ucp['items']:
            file.writestr('items/{item.id}/editoritems.txt',_genEditoritemsStr(item))
