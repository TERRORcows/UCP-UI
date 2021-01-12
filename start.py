import eel, os, json

eel.init('app')

@eel.expose
def loadPackageList():
    def mergeJSON(x):
        tmp = json.loads(readFile(x))
        tmp['filename'] = x
        return tmp
    def readFile(x):
        with open("files/"+x,"r") as y:
            z = y.read()
            y.close()
            return z
    return [mergeJSON(x) for x in os.listdir('files') if x.endswith('.ucp')]

@eel.expose
def savePackage(pkg,filename):
    with open('files/'+filename,'w') as file:
        json.dump(pkg,file,indent=2) # enable pretty-printing for now
        file.close()

eel.start('main.html',geometry={'size':(650,500)})
