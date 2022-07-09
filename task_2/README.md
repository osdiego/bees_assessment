# Task 2 – Create a package

## Short description of the task

In this task is requested to create a package with the functions that were built in the ***Task 1***.

### Additional notes

* The package could have being made available on PyPi, but was chosen not to due to the request to not make things public;
* The documentation of the package was built using pdoc3 (Python package already listed in the requirements file);
To generate an HTML file automatically from the Docstrings of the package (already done, see [documentation](documentation)), run the following inside the **task_2** folder:
  * `pdoc --html --output-dir documentation package/src/sbees`
* The settings of the unit tests were all set on [pyproject.toml](pyproject.toml).

## Instructions to run the code

* The package was built locally and its [wheel](task_2/package/dist/sbees-1.0b1-py3-none-any.whl) is already being provided (if you already installed the requirements, it is already installed), and to build it again you can run the following command inside **task_2/package** folder:
  * `py -m build`
* To run the unit tests, show brief results on console and save the report to [report.json](task_2/package/test/coverage/report.json), run the following inside the **task_2/package** folder:
  * `coverage run & coverage json`

## Deliverables

* Zip file with the code of the package;
* Documentation;
* Wheel of the package;

## Planed / executed actions

* Created a package with the functions of the ***Task 1***, but generalize them;
* Add unit tests (pytest and coverage) - 100% coverage is not required;
* Generate documentation from Docstrings using pdoc3;
* Create a wheel of the code;
* Zip the code.
