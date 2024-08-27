import json
from os import walk

def loadTestsFromFile(path):
    filenames = next(walk(path), (None, None, []))[2]
    for file in filenames:
        with open(path + "\\" + file, "r") as f:
            tests = json.load(f)
            for test in tests:
                yield createTest(test)

def createTest(testParamaters):
    testParamaters["SQL_Query1"] = """
        SET NOCOUNT ON;
        EXEC _rsp_GetPlaylistContent [USERID]
        """
    testParamaters["SQL_Query2"] = """
        SET NOCOUNT ON;
        EXEC _rsp_GetPlaylistContent [USERID]
        """

    val = testParamaters["val"]
    testParamaters["SQL_Query1"] = testParamaters["SQL_Query1"].replace('[USERID]', str(val))
    testParamaters["SQL_Query2"] = testParamaters["SQL_Query2"].replace('[USERID]', str(val))

    return testParamaters
