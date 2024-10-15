import json
from os import walk

def SetNoCount(noCount):
    if (noCount):
        return "SET NOCOUNT ON;"
    else:
        return "SET NOCOUNT OFF;"

def StoredProcedure(StoredProcedureName):
    return "EXEC " + StoredProcedureName

class Test:
    NEWLINE = "\n"
    
    def __init__(self, testName, storedProcedureName1, storedProcedureName2, arguments):
        self.Query1 = ""
        self.Query2 = ""
        self.testName = testName
        self.storedProcedureName1 = storedProcedureName1
        self.storedProcedureName2 = storedProcedureName2
        self.arguments = []
        for arg in arguments:
            if arg["type"] == "INT":
                self.arguments.append(IntParamater(arg["name"], arg["value"]))
            elif arg["type"] == "DATETIME":
                self.arguments.append(DateTimeParamater(arg["name"], arg["value"]))
            else:
                raise Exception(arg["type"] + " is not a valid paramater type")

    def createTestSQL(self):
        Query1 = SetNoCount(True) + self.NEWLINE
        Query2 = SetNoCount(True) + self.NEWLINE

        for arg in self.arguments:
            Query1 = Query1 + arg.SetUp() + self.NEWLINE
            Query2 = Query2 + arg.SetUp() + self.NEWLINE

        Query1 = Query1 + StoredProcedure(self.storedProcedureName1) + " "
        Query2 = Query2 + StoredProcedure(self.storedProcedureName2) + " "

        for arg in self.arguments:
            Query1 = Query1 + arg.AddParamater() + ","
            Query2 = Query2 + arg.AddParamater() + ","

        self.Query1 = Query1.rstrip(',') + ";"
        self.Query2 = Query2.rstrip(',') + ";"

class Paramater:
    def __init__(self, name, value):
        self.name = name
        self.value = value

class IntParamater(Paramater):
    def __init__(self, name, value):
        super().__init__(name, value)

    def SetUp(self):
        return f'DECLARE @{self.name} INT = {self.value};'

    def AddParamater(self):
        return f'@{self.name} = @{self.name}'

class DateTimeParamater(Paramater):
    def __init__(self, name, value):
        #TODO validate format
        super().__init__(name, value)

    def SetUp(self):
        return f'DECLARE @{self.name} DATETIME = \'{self.value}\';'

    def AddParamater(self):
        return f'@{self.name} = @{self.name}'

def loadTestsFromJsonFile(path):
    filenames = next(walk(path), (None, None, []))[2]
    for file in filenames:
        if file.endswith(".json"):
            with open(path + "\\" + file, "r") as f:
                tests = json.load(f)
                for test in tests:
                    yield Test(test["test name"], test["procedure 1 name"]
                               ,test["procedure 2 name"], test["arguments"])
