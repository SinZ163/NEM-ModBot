import simplejson
import datetime
import os
import re
import traceback

ID = "modbot"
permission = 0
class ModBot():
    lists = {}
    current = ""
    
    htmlData = {}
    def __init__(self):
        self.readDisk()
        
        #make "latest" list, the default on launch
        sortedList = sorted(self.lists.iterkeys())
        self.current = sortedList[len(sortedList)-1]
        
        #load html template into memory (faster than loading it every time maybe?
        for fileName in ["header","breaker","footer"]:
            with open("commands/NEM/"+fileName+".txt", "r") as f:
                self.htmlData[fileName] = f.read()
    def readDisk(self):
        fileList = os.listdir("commands/NEM/")
        for fileName in fileList:
            if fileName[-5:] == ".json":
                with open("commands/NEM/"+fileName,"r") as f:
                    version = fileName[:-5]
                    fileInfo = f.read()
                    self.lists[version] = simplejson.loads(fileInfo, strict = False)
                    
    def saveList(self, version):
        with open("commands/NEM/"+version+".json", "w") as f:
            f.write(simplejson.dumps(self.lists[version], sort_keys=True, indent=4 * ' '))
            
    def compileHTML(self, version):
        with open("commands/NEM/website/"+version+".html", "w") as f:
            timeStamp = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
            timeStampedInfo = re.sub("~UPDATE_TIME~", timeStamp, self.htmlData["header"])
            print(self.lists[version])
            print(str(type(self.lists[version])))
            f.write(re.sub("~MOD_COUNT~", str(len(self.lists[version])), timeStampedInfo))
            for modName, info in self.lists[version].iteritems():
                f.write("""
  <tr>
    <td class='name'><a href='{}' target='_blank'>{}</a></td>
    <td class='aliases'>{}</td>
    <td class='author'>{}</td>
    <td class='version'>{}</td>
    <td class='dev'>{}</td>
    <td class='comment'>{}</td>
  </tr>""".format(info["longurl"],modName,info["aliases"],info["author"],info["version"],info["dev"],info["comment"]))
            f.write(self.htmlData["footer"])
modbot = ModBot()
            
def execute(self, name, params, channel, userdata, rank):
    if params[0] == "compile":
        try:
            modbot.compileHTML(params[1])
        except Exception as e:
            self.sendChatMessage(self.send, channel, str(e))
            traceback.print_exc()