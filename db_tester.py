import pyodbc
import pandas as pd
import configparser
import test_creator
import argparse

def RunTests(tests, conn):
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

def PrintTests(tests):
    i = 0
    for test in tests:
        print("Test " + str(i))
        print(test["SQL_Query1"])
        print(test["SQL_Query2"])
        print("---------")
        i += 1

## Command Line Arguments Parse
commandParser = argparse.ArgumentParser()
commandParser.add_argument("--debug", help="prints sql commands instead of running them",
                    action="store_true")
args = commandParser.parse_args()
## End Command Line Arguments Parse

## Config File Parse
configP = configparser.ConfigParser()
configP.read('config.ini')
## End Config File Parse

tests = test_creator.loadTestsFromJsonFile(configP['Database Connection Values']['TESTFOLDERPATH'])

if args.debug:
    PrintTests(tests)
else:
    SERVER = configP['Database Connection Values']['SERVER']
    DATABASE = configP['Database Connection Values']['DATABASE']
    USERNAME = configP['Database Connection Values']['USERNAME']
    PASSWORD = configP['Database Connection Values']['PASSWORD']

    connectionString = f'DRIVER={{SQL Server}};SERVER={SERVER};DATABASE={DATABASE};UID={USERNAME};PWD={PASSWORD}'

    conn = pyodbc.connect(connectionString)
    RunTests(tests, conn)
    conn.close()
