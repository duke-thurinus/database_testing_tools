def createTest(val):
    test = {
        "SQL_Query1" : """
        SET NOCOUNT ON;
        EXEC _rsp_GetPlaylistContent [USERID]
        """,

        "SQL_Query2" : """
        SET NOCOUNT ON;
        EXEC _rsp_GetPlaylistContent [USERID]
        """
    }

    test["SQL_Query1"] = test["SQL_Query1"].replace('[USERID]', str(val))
    test["SQL_Query2"] = test["SQL_Query2"].replace('[USERID]', str(val))

    return test
