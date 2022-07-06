# bees_assessment

Private repository that contains the code for the Streetbees Data Engineer - technical assessment.

Please read both the main README file (this one), and the ones inside each task folder, they are essential to understand everything that was done.

I, Diego Soares, put a lot of effort on trying to keep everything simple, but with quality. If you find any specific piece of code that needs clarification or would require some sort of improvement, please bring that to a discussion with me, it might be done this way for a specific reason not explicit in the code or in the documentation.

## Information regarding the repository

Looking at the folder structure, you will be able to see 3 folders, one for each task.
The instructions to assess each of the tasks are on the README.md of the respective folders.

### Additional notes

- The master branch of the repo is called ***main***, following the community most recent practices;
- All the commits were done directly on the main branch to save some time and preserve the history of commits as requested, but in a real environment GitFlow would be followed and the PR's and squashes would be properly used;
- The written code tries to follow at risk the guidelines of the PEPs, and if something was forgotten I apologize, I did my best with the given time;
- The Python Docstrings style chosen for the project was the one from Google, as this is one of the simplest ones to read, but any other could be used in case of need;
- Multiline statements usually ends with a comma so it is easier to see the difference in possible future Pull Requests;
- The logging library was superficially used just to exemplify this best practice when it comes to logging on processes like data pipelines. Different from simple notebooks of prof of concepts, pipelines need to be handled carefully when it comes to logs, well handled, like setting the proper level of log per environment and configuring log file rotations;
- A lot of error treatments, including the creation of special error classes, could be done, but for a matter of keeping the level of complexity on the assessment it was not developed deeply;
- Most of the time, at least inside the methods, creating a copy of the data is used as an approach to avoid messing up with the original variable unintentionally, but it could be developed in such a way to update the original object in place in case of need (something like pandas parameter "inplace=True");
- Pandas is widely used in this project due its simplicity and the easy an fast way of handling small sets of data. For more complex / larger datasets, PySpark could be an option, or even transforming the data to another data structure to perform some operations (sometimes transforming the data into a Python dictionary and performing the operations on top of it are faster than working with Pandas DataFrames, the best data structure / tool to handle the problem will depend from case to case).

### Files / folders on the root of the repo

- [.vscode](.vscode): the settings for the workspace;
- [assets](assets): all the provided files for the test;
- [task_1](task_1): all the code and additional files for the **Task 1 – Identification of issues and improvements**;
- [task_2](task_2): all the code and additional files for the **Task 2 – Create a package**;
- [task_3](task_3): all the code and additional files for the **Task 3 – Demonstration of the package**;
- [.gitignore](.gitignore): all the files and patterns to be ignored on commits (automatically generated on repo creation);
- [LICENSE](LICENSE): the license (MIT) of the repo (automatically generated on repo creation);
- [README.md](README.md): the README file with the basic information regarding the repo (another README files can be found inside the folders of each task);
- [requirements.txt](requirements.txt): all the external packages necessary to run the scripts in this repo.

## Instructions to be able to run the code

Before starting, you may want to create a virtual environment, once the execution of the scripts in this repo will require the installation of some external packages from <https://pypi.org/>. If desired, you can get some details on the [official Python docs](https://docs.python.org/3/library/venv.html), or simply install it outside a virtual environment.

1. Install Python (**Python 3.9.7** was the one used for development, so any version higher than that should work without problems);
2. Install the necessary dependencies using a packaging tool of your choice. Running one of the following with pip will do the job:
     - `pip install --upgrade -r requirements.txt`
     - `python -m pip install --upgrade -r requirements.txt` (in case the pip can't be found due to PATH not well configured)
3. You should now be able to run the scripts.
