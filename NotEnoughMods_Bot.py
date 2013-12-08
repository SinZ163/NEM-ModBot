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
            with open("commands/modbot.mca.d3s.co/"+fileName+".txt", "r") as f:
                self.htmlData[fileName] = f.read()
    def readDisk(self):
        fileList = os.listdir("commands/modbot.mca.d3s.co/htdocs/")
        for fileName in fileList:
            if fileName[-5:] == ".json":
                with open("commands/modbot.mca.d3s.co/htdocs/"+fileName,"r") as f:
                    version = fileName[:-5]
                    fileInfo = f.read()
                    rawOutput = simplejson.loads(fileInfo, strict = False)
                    self.lists[version] = {}
                    for modInfo in rawOutput:
                        modName = modInfo["name"]
                        del modInfo["name"]
                        self.lists[version][modName] = modInfo
                    
    def saveList(self, version):
        with open("commands/modbot.mca.d3s.co/htdocs/"+version+".json", "w") as f:
            output = []
            rawOutput = self.lists[version]
            for key, value in sorted(rawOutput.iteritems()):
                value["name"] = key
                output.append(value)
            f.write(simplejson.dumps(output, sort_keys=True, indent=4 * ' '))
            
    def compileHTML(self, version):
        with open("commands/modbot.mca.d3s.co/htdocs/"+version+".html", "w") as f:
            timeStamp = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
            timeStampedInfo = re.sub("~UPDATE_TIME~", timeStamp, self.htmlData["header"])
            #print(self.lists[version])
            #print(str(type(self.lists[version])))
            f.write(re.sub("~MOD_COUNT~", str(len(self.lists[version])), timeStampedInfo))
            for modName, info in sorted(self.lists[version].iteritems()):
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
    try:
        if rankTranslate[rank] >= commands[params[0]]["rank"]:
            command = commands[params[0]]["function"]
            command(self, name, params, channel, userdata, rank)
        else:
            self.sendNotice(name, "You do not have permissions for this command!")
    except KeyError:
        self.sendChatMessage(self.send, channel, "invalid command!")
        self.sendChatMessage(self.send, channel, "see =modbot help for a list of commands")
        
def debug_compile(self, name, params, channel, userdata, rank):
    try:
        modbot.compileHTML(params[1])
    except Exception as e:
        self.sendChatMessage(self.send, channel, str(e))
        traceback.print_exc()
def debug_save(self, name, params, channel, userdata, rank):
    try:
        modbot.saveList(params[1])
    except Exception as e:
        self.sendChatMessage(self.send,channel,str(e))
        traceback.print_exc()
def command_show(self, name, params, channel, userdata, rank):
    if len(params) < 2:
        self.sendChatMessage(self.send, channel, name+ ": Insufficent amount of parameters provided.")
        self.sendChatMessage(self.send, channel, name+ ": "+help["list"][1])
        return
    if len(params) >= 3:
        version = params[2]
    else:
        version = modbot.current
    try:
        data = modbot.lists[version]
        if params[1] not in data:
            #TODO: search aliases here
            self.sendChatMessage(self.send, channel, "Mod not found.")
            return
       
        darkgreen = "03"
        red = "05"
        purple = "06"
        orange = "7"
        blue = "12"
        pink = "13"
        gray = "14"
        bold = unichr(2)
        colour = unichr(3)
        alias = colour
        if data[params[1]]["aliases"] != "":
            alias = colour+"("+colour+pink+str(re.sub(" ", colour+', '+colour+pink, data[params[1]]["aliases"]))+colour+") "
        comment = colour
        if data[params[1]]["comment"] != "":
            comment = str(colour+"("+colour+gray+data[params[1]]["comment"]+colour+") ")
        dev = colour
        try:
            if data[params[1]]["dev"] != "":
                dev = str(colour+" ("+colour+gray+"dev"+colour+": "+colour+red+data[params[1]]["dev"]+colour+")")
        except Exception as error:
            print(error)
            traceback.print_exc()
            #lol
        self.sendChatMessage(self.send, channel, colour+purple+params[1]+" "+alias+colour+darkgreen+data[params[1]]["version"]+dev+" "+comment+colour+orange+data[params[1]]["shorturl"]+colour)  
    except Exception as error:
        self.sendChatMessage(self.send, channel, name+": "+str(error))
        traceback.print_exc()
        
rankTranslate = {
    "" : 0,
    "+" : 1,
    "@" : 2,
    "@@" : 3
}
commands = {
    "compile" : {
        "function" : debug_compile,
        "rank" : 2,
        "help" : "Debug command for generating the HTML pages",
        "args" : [
            {
                "name" : "version",
                "description" : "The MC Version to save the html page for.",
                "required" : True
            }
        ]
    },
    "save" : {
        "function" : debug_save,
        "rank" : 2,
        "help" : "Debug command for generating the JSON files",
        "args" : [
            {
                "name" : "version",
                "description" : "The MC Version to save the JSON file for.",
                "required" : True
            }
        ]
    },
    "show" : {
        "function" : command_show,
        "rank" : 0,
        "help" : "Does a direct search for the mod, then outputs info",
        "args" : [
            {
                "name" : "mod name",
                "description" : "The mod to output info of",
                "required" : True
            }, {
                "name" : "version",
                "description" : "The MC version to search in.",
                "required" : False
            }
        ]
    }
}