# Task 2 – Create a package

## Short description of the task

In this task is requested to create a package with the functions that were built in the ***Task 1***.

### Additional notes

The documentation of the package was built using pdoc3 (Python package already listed in the requirements file).
To generate an HTML file automatically from the Docstrings of the package (already done, see [documentation](documentation)), run the following inside the **task_2** folder:

* `pdoc --html --output-dir documentation task_2.py`

## Instructions to run the code

TODO

## Deliverables

* Zip file with the code of the package;
* Documentation;
* Wheel of the package (not required, but nice to have);
* Make the package available on PyPi (not required, and asked explicitly on the docx to not make any repos public, so it won't be done).

## Planed actions

* Make a package with the functions of the ***Task 1***, but generalize them;
* Add unit tests (pytest) - 100% coverage is not required, but ideal;
* Generate documentation from Docstrings using pdoc3;
* Create a wheel of the code;
* Zip the code.
