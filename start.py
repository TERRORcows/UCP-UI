import eel, os, json
from zipfile import ZipFile

eel.init('app')

def loadPackage(filename):
    if os.path.isfile(filename):
        with ZipFile(filename,'r') as pkg:
            out = json.loads(pkg.read('package.json'))
            pkg.close()
        return out
    else:
        print(f'WARNING: {filename} DOES NOT EXIST!')

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
    return [mergeJSON(loadPackage('files/'+x),x) for x in os.listdir('files') if x.endswith('.ucp')]

'''
@eel.expose
def savePackage(pkg,filename):
    with open('files/'+filename,'w') as file:
        json.dump(pkg,file,indent=2) # enable pretty-printing for now
        file.close()
'''

eel.start('main.html',geometry={'size':(650,500)})
