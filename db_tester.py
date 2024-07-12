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

SQL_Query = """
SET NOCOUNT ON;
EXEC _rsp_getStudentDashContentByID 200840797
"""


df1 = pd.read_sql(SQL_Query, conn)
columns = df1.columns.to_list()
df1.sort_values(by=columns, inplace=True, ignore_index=True)

SQL_Query = """
SET NOCOUNT ON;
EXEC _rsp_getStudentDashContentByID_test 200840797
"""

df2 = pd.read_sql(SQL_Query, conn)
df2.sort_values(by=columns, inplace=True, ignore_index=True)

comparisonDF = df1.compare(df2)
print(comparisonDF)

conn.close()


