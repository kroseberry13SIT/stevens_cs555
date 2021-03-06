from datetime import datetime
from datetime import date
from prettytable import PrettyTable

tags = {'INDI':'0','NAME':'1','SEX':'1','BIRT':'1','DEAT':'1','FAMC':'1','FAMS':'1','FAM':'0','MARR':'1','HUSB':'1','WIFE':'1','CHIL':'1','DIV':'1','DATE':'2','HEAD':'0','TRLR':'0','NOTE':'0'}
individualsDict = {}
familiesDict = {}
outputtableI = PrettyTable()
outputtableF = PrettyTable()
#
class Individual:
    type = "I"
    id = ""
    name = ""
    gender = ""
    birthDate = None
    deathDate = None
    children = []
    Spouse = ""
    familyIdChild = None
    familyIdSpouse = None
    
    def toString(self):
        outputtableI.add_row(self.id,self.name,self.gender,self.birthDate,self.calculateAge())
    
    def calculateAge(self):
        #TODO parse birthdate from string to date object
        today = date.today()
        
        return today.year - self.birthDate.year - ((today.month, today.day) < (self.birthDate.month, self.birthDate.day))

class Family:
    type = "F"
    id = ""
    marriageDate = None
    divorcedDate = None
    husbandId = ""
    husbandeName = ""
    wifeId = ""
    wifeName = ""
    children = []

def parseStringtoDate(day,month,year):
    retDate = None
    if (int(day) < 10):
        day = "0" + day
    try:
        retDate = datetime.strptime(day + " " + month + " " + year,'%d %b %Y')
    except ValueError:
        print "Wrong Date Format for " + day + " " + month + " " + year
    return retDate

inputFileName = "proj02test.ged"
inputFile = open(inputFileName,"r")

tmpObj = None
dateType = None

for line in inputFile:
    lineSplit = line.split()
    if lineSplit[0] == "0" and len(lineSplit) > 2 and (lineSplit[2] == "INDI" or lineSplit[2] == "FAM"):
        if tmpObj is not None:
            if tmpObj.type == "I":
                individualsDict[tmpObj.id] = tmpObj
            else:
                familiesDict[tmpObj.id] = tmpObj
        tmpObj = None
        if lineSplit[2] == "INDI":
            tmpObj = Individual()
        else:
            tmpObj = Family()
        tmpObj.id = lineSplit[1]
    elif lineSplit[1] in tags and (lineSplit[0] == "1" or lineSplit[0] == "2"):
        if lineSplit[1] == "NAME":
            tmpObj.name = ' '.join(lineSplit[2:])
        elif lineSplit[1] == "SEX":
            tmpObj.gender = lineSplit[2]
        elif lineSplit[1] == "BIRT" or lineSplit[1] == "DEAT" or lineSplit[1] == "MARR" or lineSplit[1] == "DIV":
            dateType = lineSplit[1]
        elif lineSplit[1] == "FAMC":
            tmpObj.familyIdChild = lineSplit[2]
        elif lineSplit[1] == "FAMS":
            tmpObj.familyIdSpouse = lineSplit[2]
        elif lineSplit[1] == "HUSB":
            tmpObj.husbandId = lineSplit[2]
        elif lineSplit[1] == "WIFE":
            tmpObj.wifeId = lineSplit[2]
        elif lineSplit[1] == "CHIL":
            tmpObj.children.append(lineSplit[2])
        elif lineSplit[1] == "DATE" and dateType is not None and len(lineSplit) > 4:
            if (dateType == "BIRT"):
                tmpObj.birthDate = parseStringtoDate(lineSplit[2],lineSplit[3],lineSplit[4])
            elif dateType == "DEAT":
                tmpObj.deathDate = parseStringtoDate(lineSplit[2],lineSplit[3],lineSplit[4])
            elif dateType == "MARR":
                tmpObj.marriageDate = parseStringtoDate(lineSplit[2],lineSplit[3],lineSplit[4])
            elif dateType == "DIV":
                tmpObj.divorcedDate = parseStringtoDate(lineSplit[2],lineSplit[3],lineSplit[4])
            dateType = None
            
if tmpObj is not None:
    if tmpObj.type == "I":
        individualsDict[tmpObj.id] = tmpObj
    else:
        familiesDict[tmpObj.id] = tmpObj

inputFile.close()

for i in individualsDict:
    individualsDict[i].toString()

print outputtableI
