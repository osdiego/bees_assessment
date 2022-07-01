# Task 1 – Identification of issues and improvements

## Short description of the task

In this task is requested to create a data pipeline to do some cleaning on CSV files.

## Instructions to run the code

- Inside the **task_1** folder, run: `py treatment.py`

## Deliverables

- A single python file with all the code.

## Planed / executed actions

### Acquire knowledge of the challenge by cleaning the files and comparing its structure with the information of the docx

- Read files using pandas;
- Compare the headers of the files (result: background schemas have only the difference in the map, log schemas are the same).

### Create functions for each of the following bullets

- Merge background and logs DataFrames (rename columns in **df_bg_1** according to **df_bg_2** columns);
- Set gender column to lowercase;
- Set location names all to codes (PyCountry?);
- Fix mismatched user age groups;
- Merge duplicated columns in the same dataset;
- Convert **Level2dish_coded** column from dictionary to string;
- Remove brackets from **Questions_135633_and_who_are_you_sharing_your_home_with** column values;
- Merge duplicated values in the same cell (`["a", "a"]` -> `["a"]`).

## Problems found

- The headers of the background_mapping.csv file needed treatment (trim white spaces at the end of the string);
- The columns in the mapping file are actually switched:
  - "Project 1 Question" should be "Project 2 Question";
  - "Project 2 Question" should be "Project 1 Question".
- The order of the columns is not always the same, so they all were sorted to guarantee proper comparison.

## Dictionary of abbreviations

| Key  | Meaning    |
| :--: | ---------- |
| bg   | background |
| cols | columns    |
| df   | DataFrame  |
| prj  | project    |
