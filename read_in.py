
from collections import OrderedDict
import csv

def readInStudents(student_path):
    studentReader = csv.reader(open(student_path, newline=''), delimiter=',', quotechar='"')
    students = []
    for student in studentReader:
        [SID, version] = student
        students.append((SID, version))

    return students

def readInVars(vars_path):
    vars_dict = OrderedDict()

    varReader = csv.reader(open(vars_path, newline=''), delimiter=',', quotechar='"')
    next(varReader) # skip titles
    for var in varReader:

        (varName, val, transType, account) = (var[0], var[4], var[6], var[7])
        if varName != "":
            vars_dict[varName] = (val, transType, account)

    return vars_dict

def readInAccounts(accounts_path):
    accounts_dict = OrderedDict()

    accountsReader = csv.reader(open(accounts_path, newline=''), delimiter=',', quotechar='"')
    next(accountsReader) # skip titles
    for account in accountsReader:
        # transform to useful format
        (accountName, accountType, openingBalance) = (account[0], account[1], account[2])
        accounts_dict[accountName] = (accountType, openingBalance)

    return accounts_dict
