import pyodbc
import pandas as pd
import configparser

configP = configparser.ConfigParser()
configP.read('config.ini')

SERVER = configP['Database Connection Values']['SERVER']
DATABASE = configP['Database Connection Values']['DATABASE']
USERNAME = configP['Database Connection Values']['USERNAME']
PASSWORD = configP['Database Connection Values']['PASSWORD']

connectionString = f'DRIVER={{SQL Server}};SERVER={SERVER};DATABASE={DATABASE};UID={USERNAME};PWD={PASSWORD}'

conn = pyodbc.connect(connectionString)

SQL_Query1 = """
SET NOCOUNT ON;
EXEC _rsp_getStudentDashContentByID [USERID]
"""

SQL_Query2 = """
SET NOCOUNT ON;
EXEC _rsp_getStudentDashContentByID_test [USERID]
"""

values = [200840797, 200938901, 200938922]
for val in values:
    df1 = pd.read_sql(SQL_Query1.replace('[USERID]', str(val)), conn)
    columns = df1.columns.to_list()
    df1.sort_values(by=columns, inplace=True, ignore_index=True)

    df2 = pd.read_sql(SQL_Query2.replace('[USERID]', str(val)), conn)
    df2.sort_values(by=columns, inplace=True, ignore_index=True)

    comparisonDF = df1.compare(df2)
    if comparisonDF.empty:
        print('test with value: ' + str(val) + ' is successful')
    else:
        print('test with value: ' + str(val) + ' produced diffrences:')
        print(comparisonDF)

conn.close()


