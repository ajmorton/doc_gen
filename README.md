# Per student document generation
Proof of Concept  
Takes in three csv's to generate values for an assignment template and outputs unique assignments for each student

## dependencies
- python3
- pdfkit `pip3 install pdfkit`
  - pdfkit may require `wkhtmltopdft`
- any version of LaTex (for pdf creation)

## usage
run with `python3 gen_docs.py <student_list> <accounts_list> <vars_list>`

For a current working example try:
`python3 gen_docs.py student_list.txt example_accnts.csv example_vars.csv`

## Folders
- `template` contains a assignment template (currently called index.html)
- `students` the output folder of student pdf's
