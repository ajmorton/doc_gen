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


import read_in
import write_content

import sys
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

def calculate_assignment(vars_dict, accounts_dict):
    unique_vars_dict = OrderedDict()
    unique_accounts_dict = OrderedDict()

    for account in accounts_dict:
        (accountType, openingBalance) = accounts_dict[account]
        unique_accounts_dict[account] = int(openingBalance)

    for var in vars_dict:
        (val, transType, account) = vars_dict[var]

        val = parseVal(val, unique_vars_dict)

        if var not in unique_vars_dict:
            unique_vars_dict[var] = val

        if account:
            if account not in accounts_dict:
                print("ERRORRRRRR")

            if transType == "CR":
                # print("{} credited {}".format(account, val))
                unique_accounts_dict[account] += val
            if transType == "DR":
                # print("{} debited {}".format(account, val))
                unique_accounts_dict[account] -= val

    return (unique_vars_dict, unique_accounts_dict)

# read in an accounts list and a var list for a single student, then print values
# out to said students folder. Random values in the lists a seeded by the
# students number and a version number for regeneration
# TODO this reads in the same vars_list and accounts_list once per student.
#      With a fair bit of refactoring we could potentially mitigate this.
#      However, I can see interdependence of rng state across students causing
#      issues
def read_csv(student_path, accounts_path, vars_path):

    # read in vars_dict, don't evaluate values
    vars_dict    = read_in.readInVars(vars_path)

    # read in accounts_dict, initial states
    accounts_dict = read_in.readInAccounts(accounts_path)

    students = read_in.readInStudents(student_path)

    # use vars_dict and accounts_dict to generate unique per student versions

    for student in students:
        (SID, version) = student
        try:
            seed(SID + version)
            (unique_vars_dict, unique_accounts_dict) = calculate_assignment(vars_dict, accounts_dict)
            write_content.printDicts(SID, unique_accounts_dict, unique_vars_dict)
        except UnicodeDecodeError as e:
            print("Unicode decoding error:\n\tplease check input for non utf8"
                  " characters (é, ü, â)")


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Invalid number of args: input should be\n\t"
              "student_list, accounts_path, vars_path")
    else:
        [student_list, accounts_path, vars_path] = sys.argv[1:]
        read_csv(student_list, accounts_path, vars_path)
