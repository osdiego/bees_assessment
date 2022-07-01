# bees_assessment
Private repository that contains the code for the Streetbees Data Engineer - technical assessment.

## Instructions to be able to run the code:
- Install python (Python 3.9.7 used for development, so any version higher than that should work without problems)
- Install the necessary dependencies using a packaging tool of your choice, running one of the following with pip will do the job:
-- pip install --upgrade -r requirements.txt
-- python -m pip install --upgrade -r requirements.txt (in case the pip can't be found due to PATH not well configured)
- You should now be able to run, on the root of the repository: py treatment.py

## Planed / executed actions:
- Acquire knowledge of the challenge by cleaning the files and comparing its structure with the information of the docx
-- Read files using pandas
-- Compare the headers of the files (result: background schemas have only the difference in the map, log schemas are the same)

## Problems found:
- The headers of the background_mapping.csv file needed treatment (trim white spaces at the end of the string)
- The columns in the mapping file are actually switched:
-- "Project 1 Question" should be "Project 2 Question"
-- "Project 2 Question" should be "Project 1 Question"
- The order of the columns is not always the same, so they all were sorted to guarantee proper comparison

## Dictionary of abbreviations:
- bg = background
- cols = columns
- df = DataFrame
- prj = project
