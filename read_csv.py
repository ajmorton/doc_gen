#TODO
#   - approx. 3s per pdf, that's an hour for 1000 students
#   - currently only casting to int, need floating point?
#   - replace eval with own string parsing
#       - SUM, Random, basic maths
#   - accounts aren't currently storing their account type
#     this may affect how debiting and crediting work
#   - csv reader uses utf-8 encoding: characters like "é" raise UnicodeDecodeError
#   - need more error/exception testing
#   - error catching:
#       - key not in dict
#   - precision of output
#       - round/floor?
#   - Categories not currently in use:
#       - Date, inputDate, type, subaccount, acctPeriod, UsedInDocuments
#   - confirm that empty lines (with no variable can be skipped)

# reading in
# writing out

import write_content

import os
import sys
import csv
import re
from collections import OrderedDict
from random import randrange, seed

# takes in a string describing the value of a variable
# handles constants (cast to int), references (lookup vars in dict),
# random (rand), and mathematical expressions
def parseVal(val, vars_dict):

    # regex to recognise a variable, defined as an alphanumeric string
    # preceded by a '$'
    aVar = re.compile("\$([A-Za-z0-9]+)")

    # replace $ with calls to vars_dict
    if '$' in val:
        # r'\$(\w+)' <-- old pattern match
        val = re.sub(aVar, r'vars_dict["\1"]', val)

    if "SUM" in val:
        print("Warning: SUM not yet implemented, returning 1")
        return 1

    val = val.replace("Random", "randrange")

    # TODO remove usage of eval
    try:
        val = eval(val)
    except (KeyError) as e:
        print("\tERROR: No such key: ", end="")
        print(e, end=", evaluating term to one\n")
        print("\tCheck that you have spelled the term correctly")
        val = 1
    except (ZeroDivisionError):
        print("Trying to Divide by Zero in term {}, returning 1".format(val))
        val = 1

    return val

# readInAccounts reads in a csv containing a list of accounts used in the assignment
def readInAccounts(accounts_path, accounts_dict, vars_dict):
    acctReader = csv.reader(open(accounts_path, newline=''), delimiter=',', quotechar='"')
    next(acctReader)

    for acct in acctReader:
        # transform to useful format
        (acctName, acctType, startingVal) = (acct[0], acct[1], int(acct[2]))
        accounts_dict[acctName] = startingVal
        # TODO add type of account


# readInVars reads from a csv file of all variables defined in the assignment
# and assigns them values (constants, derived or random)
def readInVars(vars_path, accounts_dict, vars_dict):

    varReader = csv.reader(open(vars_path, newline=''), delimiter=',', quotechar='"')
    next(varReader)
    for row in varReader:
        # print(row)
        # transform to useful format
        (varName, val, transType, account) = (row[0], row[4], row[6], row[7])

        if varName == "":
            #skip lines that don't referring to variable
            continue
        # print("{}, {}, {}, {}".format(varName, val, transType, account))

        val = parseVal(val, vars_dict)

        if varName not in vars_dict:
            vars_dict[varName] = val


        if account:
            if account not in accounts_dict:
                print("ERRORRRRRR")

            if transType == "CR":
                # print("{} credited {}".format(account, val))
                accounts_dict[account] += val
            if transType == "DR":
                # print("{} debited {}".format(account, val))
                accounts_dict[account] -= val


# read in an accounts list and a var list for a single student, then print values
# out to said students folder. Random values in the lists a seeded by the
# students number and a version number for regeneration
# TODO this reads in the same vars_list and accounts_list once per student.
#      With a fair bit of refactoring we could potentially mitigate this.
#      However, I can see interdependence of rng state across students causing
#      issues
def read_csv(SID, version, accounts_path, vars_path):
    try:
        vars_dict = OrderedDict()
        accounts_dict = OrderedDict()

        seed(SID + version)
        readInAccounts(accounts_path, accounts_dict, vars_dict)
        readInVars(vars_path, accounts_dict, vars_dict)
        write_content.printDicts(SID, accounts_dict, vars_dict)
    except UnicodeDecodeError as e:
        print("Unicode decoding error:\n\tplease check input for non utf8"
              " characters (é, ü, â)")


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Invalid number of args: input should be\n\t"
              "student_list, accounts_path, vars_path")
    else:
        [student_list, accounts_path, vars_path] = sys.argv[1:]

        studentReader = csv.reader(open(student_list, newline=''), delimiter=',', quotechar='"')
        for student in studentReader:
            [SID, version] = student
            read_csv(SID, version, accounts_path, vars_path)
