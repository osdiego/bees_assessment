# Task 1 – Identification of issues and improvements

## Short description of the task

In this task is requested to create a data pipeline to do some cleaning on CSV files.

### Additional notes

- For performance reasons, it is necessary to do some cleaning on the datasets before doing the merge, that is why the actions on the Task 1 script does not follow the order of the bullet points in the docx;
- Most of the logic is being kept on the scrip for analysis, but not all, in an attempt to keep it as clear as possible and still give the opportunity for it to be properly assessed. Some **logger** and **pprint** statements are also being kept, sometimes commented, to also make it easier to assess the code and the line of thinking;
- A data pipeline is not exactly what was build. The created script is "simply" a set of actions to understand and clean the data;
- A pipeline would probably:
  - save different files along the process to avoid losing the progress during breaking actions;
  - use a efficient file format to store this data (e.g. parquet), with proper partitioning according to the amount of data;
  - have some better error handling to detect when the process brakes;
  - have a recovery strategy;
  - be triggered recurrently using specific source and target file locations.
- Additional actions could be performed to clean this data deeper, like ensure that a column does not have similar values, like "A / B" and "A /B", where the difference is only the format of the values (the space in this case), or even convert the values in the column **questions_224112_149402_210209_including_yourself_how_many_people_do_you_share_your_home_with** to be all in the same format (e.g. transform "four" into "4"), but it would be just a matter of putting more hours into it and not necessarily demonstrate my skills, so this kind of additional operation won't be performed.

## Instructions to run the code

- Inside the **task_1** folder, run: `py treatment.py`

## Deliverables

- A Python file with the code of the treatment: [treatment.py](treatment.py);
- A Python file with the functions created to do the cleaning: [helpers.py](helpers.py);
- A JSON file with some helping metadata: [list_like_columns_map.json](list_like_columns_map.json);
- Dummy log file, containing the logs of some executions: [task_1.log](task_1.log);
- The final datasets after all the cleaning: [output/background_dataset.xlsx](output/background_dataset.xlsx), and [output/logs_dataset.xlsx](output/logs_dataset.xlsx).

## Planed / executed actions

### Acquire knowledge of the challenge by cleaning the files and comparing its structure with the information on the docx

- Read files using pandas;
- Compare the headers of the files (result: background schemas have only the difference in the map, log schemas are the same).

### Create functions for each of the following bullets

- "Merge" (it needs actually to be concatenated) background and logs DataFrames (rename columns in **df_bg_1** according to **df_bg_2** columns);
- Set gender column to lowercase;
- Set location names all to codes (PyCountry?);
- Fix mismatched user age groups (**this topic will not have a solution implemented**);
- Merge duplicated columns in the same dataset;
- Convert **Level2dish_coded** column from dictionary to string;
- Remove brackets from **Questions_135633_and_who_are_you_sharing_your_home_with** column values;
- Merge duplicated values in the same cell (`["a", "a"]` -> `["a"]`).

## Problems found / Actions taken

- The headers of the background_mapping.csv file needed treatment (trim white spaces at the end of the string);
- The columns in the mapping file are actually switched:
  - "Project 1 Question" should be "Project 2 Question";
  - "Project 2 Question" should be "Project 1 Question".
- The project 2 was used as baseline to set the name of the final columns as the docx says it has the most recent data (what suggests that these are the right names to be used, despite the questions identifiers of the different columns being higher on the project 1 file)
- Mismatched user age groups -> there is no right way of cleaning it, at least not that I'm aware of. A few possible (not optimal) solutions were found, but a final decision would include some discussion with the team, so **this topic will not have a solution implemented**. The possible solutions found are:
  1. Delete some age groups and set the rows that use these deleted groups to a most common overlapping age group, what would possibly put a person in the wrong age group;
  2. Merge all the overlapping age groups, what would cause the existence of a "meaningless" age group with a too large range (too generic);
  3. Put a person in multiple existent age groups (which would make it harder to know the original range);
  4. Create sub groups and put a person in multiple shorter age groups (e.g. [25-34] would be [25, 26-34], [26-35] would be [26-34, 35], [35-44] would be [35, 36-44], etc.) - probably the best presented solution;
- The country code used on the dataset for United Kingdom was **UK**, but that is not the ISO code for the country, so it was updated to **GB**;
- Both "**l**evel2dish_coded" and "**q**uestions_135633_and_who_are_you_sharing_your_home_with" column names are capitalized in the docx, but not in the datasets.

## Dictionary of abbreviations

| Key  | Meaning    |
| :--: | ---------- |
| bg   | background |
| cols | columns    |
| df   | DataFrame  |
| prj  | project    |
