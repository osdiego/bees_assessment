# bees_assessment

Private repository that contains the code for the Streetbees Data Engineer - technical assessment.

## Information regarding the repository

Looking at the folder structure, you will be able to see 3 folders, one for each task.
The instructions to assess each of the tasks are on the README.md of the respective folders.

### Files / folders on the root of the repo

- [.vscode](.vscode): the settings for the workspace;
- [assets](assets): all the provided files for the test;
- [task_1](task_1): all the code and additional files for the Task 1 – Identification of issues and improvements;
- [task_2](task_2): all the code and additional files for the Task 2 – Create a package;
- [task_3](task_3): all the code and additional files for the Task 3 – Demonstration of the package;
- [.gitignore](.gitignore): all the files and patterns to be ignored on commits (automatically generated on repo creation);
- [LICENSE](LICENSE): the license (MIT) of the repo (automatically generated on repo creation);
- [README.md](README.md): the README file with the basic information regarding the repo (another README files can be found inside the folders of each task);
- [requirements.txt](requirements.txt): all the external packages necessary to run the scripts in this repo.

## Instructions to be able to run the code

Before starting, you may want to create a virtual environment, once the execution of the scripts in this repo will require the installation of some external packages from PyPi. If desired, you can get some details on the [official Python docs](https://docs.python.org/3/library/venv.html), or simply install it outside a virtual environment.

- Install python (Python 3.9.7 was the one used for development, so any version higher than that should work without problems)
- Install the necessary dependencies using a packaging tool of your choice. Running one of the following with pip will do the job:
  - pip install --upgrade -r [requirements.txt](requirements.txt)
  - python -m pip install --upgrade -r [requirements.txt](requirements.txt) (in case the pip can't be found due to PATH not well configured)
- You should now be able to run the scripts
