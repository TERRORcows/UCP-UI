import eel, os, json
from zipfile import ZipFile
from tkinter import filedialog
import tkinter
import base64
import filegen #omg custom file

root = tkinter.Tk()
root.withdraw()

eel.init('app')

subfolder = 'files/'

def loadPackage(filename):
    if os.path.isfile(filename):
        try:
            with ZipFile(filename,'r') as pkg:
                out = json.loads(pkg.read('package.json'))
                pkg.close()
            return out
        except:
            return {'title':'[CORRUPTED] '+filename}
    else:
        print(f'WARNING: {filename} DOES NOT EXIST!')

@eel.expose
def requestFileToSave(ucpname,header,filetypes,destination):
    root.lift()
    temp = filedialog.askopenfile(title=header,filetypes=filetypes)
    if (temp is None):
        return
    print(f'Saving {temp.name} to zip...')
    with ZipFile(subfolder+ucpname,'w') as pkg:
        pkg.write(temp.name,destination)
        pkg.close()
    return 'data:image/png;base64,'+base64.b64encode(open(temp.name,"rb").read()).decode('utf-8')

@eel.expose
def savePackage(package,filename):
    with ZipFile('files/'+filename,'w') as pkg:
        pkg.writestr('package.json',json.dumps(package,indent=2))
        pkg.close()

@eel.expose
def loadPackageList():
    def mergeJSON(x,y):
        tmp = x
        tmp['filename'] = y
        return tmp # This is mildly janky. The `filename` parameter inserted into the json is overwritten every time the file is loaded. This is just to know what to save the file as.
    return [mergeJSON(loadPackage(subfolder+x),x) for x in os.listdir(subfolder) if x.endswith('.ucp')]

@eel.expose
def deleteFile(x):
    print(x)
    if os.path.isfile(subfolder+x):
        os.remove(subfolder+x)

'''
@eel.expose
def savePackage(pkg,filename):
    with open('files/'+filename,'w') as file:
        json.dump(pkg,file,indent=2) # enable pretty-printing for now
        file.close()
'''

eel.start('main.html',geometry={'size':(650,500)})
