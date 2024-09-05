import pyodbc
import pandas as pd
import configparser
import test_creator

configP = configparser.ConfigParser()
configP.read('config.ini')

SERVER = configP['Database Connection Values']['SERVER']
DATABASE = configP['Database Connection Values']['DATABASE']
USERNAME = configP['Database Connection Values']['USERNAME']
PASSWORD = configP['Database Connection Values']['PASSWORD']

connectionString = f'DRIVER={{SQL Server}};SERVER={SERVER};DATABASE={DATABASE};UID={USERNAME};PWD={PASSWORD}'

conn = pyodbc.connect(connectionString)

tests = test_creator.loadTestsFromJsonFile(configP['Database Connection Values']['TESTFOLDERPATH'])

for test in tests:
    df1 = pd.read_sql(test["SQL_Query1"], conn)
    columns = df1.columns.to_list()
    df1.sort_values(by=columns, inplace=True, ignore_index=True)

    df2 = pd.read_sql(test["SQL_Query2"], conn)
    df2.sort_values(by=columns, inplace=True, ignore_index=True)

    comparisonDF = df1.compare(df2)
    if comparisonDF.empty:
        print('test with value: ' + str(test["val"]) + ' is successful')
    else:
        print('test with value: ' + str(test["val"]) + ' produced diffrences:')
        print(comparisonDF)

conn.close()


