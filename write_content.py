
import os
import pdfkit
from collections import OrderedDict

def print_rename(SID, vars_dict):
    js_file = open("template/rename.js", 'w')
    js_file.write("$(function(){\n")
    js_file.write("  document.getElementById('SID').innerHTML = '{0}'\n".format(SID))

    for var in vars_dict:
        js_file.write("  document.getElementById('{0}').innerHTML = '{1}'\n".format(var, vars_dict[var]))
    js_file.write("})")
    js_file.close()

# prints accounts values and var values to a file in a path dictated by the SID
def printDicts(SID, accounts_dict, vars_dict):

    filePath = "students/{0}".format(SID)

    if not os.path.exists(filePath):
        os.makedirs(filePath)

    # Text file for quiz referencing
    outFile = open("{0}/{1}.txt".format(filePath, SID), 'w')
    outFile.write("SID: {}\n\n".format(SID))

    outFile.write("accounts:\n")
    for acc in accounts_dict:
        outFile.write("\t{}: {}\n".format(acc, accounts_dict[acc]))

    outFile.write("\nvars:\n")
    for k in vars_dict:
        outFile.write("\t{}: {}\n".format(k, vars_dict[k]))

    # pdf output
    print_rename(SID, vars_dict)

    # call wkhtmltopdf
    options = {
        'page-size': 'A4',
        'margin-top': '0.75in',
        'margin-right': '0.75in',
        'margin-bottom': '0.75in',
        'margin-left': '0.75in',
        'dpi': 360
    }

    input_path = "template/index.html"
    output_path = "students/" + SID + "/"

    if not os.path.exists(output_path):
        os.makedirs(output_path)

    pdfkit.from_file(input_path, output_path+ SID + ".pdf", options=options)
