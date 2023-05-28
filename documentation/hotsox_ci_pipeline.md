[Return to README.md](../README.md)

## CI Pipeline & GitHub actions workflow
<br/>

### Description and technical implementation
<br/>

#### Purpose:
The general purpose of having a GitHub Actions CI (Continuous Integration) pipeline for our Python project is ensuring code quality, reliability, and efficiency throughout the software development lifecycle.
Our pipeline was focused on automatic testing using Pytest and the test coverage module and code formatting using the black formatter. During the development process any code commit that was violating the rules of our pipeline was directly noticed via notifications from the pipeline to the maintainers via email. This way, no code that did not meet our specific requirements was merged to either the development branch, or the main production branch.
<br/><br/>

#### Description and Implementation:
Our Github actions workflow is triggered on a push event, meaning it will run whenever code is pushed to the repository. Our main testing environment runs on an Ubuntu system since our project should be deployed to a server which are mainly run on Linux based systems.

The job starts by setting up a PostgreSQL service using the latest postgres image. It sets the required environment variables for the PostgreSQL container and exposes port 5432 for communication. It also includes options for performing health checks on the PostgreSQL container.
We make sure the CI job only continuous after the PostgreSQL service is up and running.
<br/><br/>
#### The further global steps in the CI job are as follows:

- Checkout code:
This step checks out (git checkout) the code at the current commit that triggered the workflow.

- Cache dependency:
This step caches the Python dependency directory (~/.cache/pip) to speed up subsequent builds. The cache key is generated based on the operating system and the hash of the requirements.txt file.

- Setup python environment:
This step sets up the Python environment using the specified Python version.

- Check Python version:
This step prints the installed Python version. It should be the latest 3.xx version. At the time of this documentation  it is 3.11.3.

We have two further CI parts for then pushed code. One for the Django part of the application and one for FastAPI:

- CI for Django:
We install the Python dependencies required for the Django project by executing pip install -r requirements.txt in the django directory.
We setup the database for Django and FastApi by run the Django makemigrations command to create database migration files and the Django migrate command to create all tables in the database.
To ensure that pushed code is properly formatted we run black in check mode.
All unittests that are supplied are now executed using pytest with coverage. Only a full pass will lead to a successful acceptance of the commit.

- CI for FastAPI:
The FastAPI Ci section follows the same principals as the one provided for Django.
We install the Python dependencies required for the FastAPI project by executing pip install -r requirements.txt in the fastapi directory. We do not need to setup the database since this was done in the Django segment. We also ensure that pushed code is properly formatted via running black in check mode. All supplied unittests are are now executed using pytest with coverage. Only a full pass will lead to a successful acceptance of the commit.

Overall, this workflow performs code checks, installs dependencies, runs database migrations, and executes tests for both Django and FastAPI projects. It also includes code formatting checks for both parts of the project.
<br/><br/>
## Licenses/ Dependencies:
- GitHub Actions  (https://github.com/features/actions)
- Pytest (https://docs.pytest.org/en/7.3.x/)
- Coverage (https://coverage.readthedocs.io/en/7.2.6)
- Black formatter (https://pypi.org/project/black/)
