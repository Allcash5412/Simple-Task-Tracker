### Simple-Task-Tracker

- Solution's author: Ponomarenko Kyrylo, @Allcash5412
- Last revision: 2024-09-20

#### Task description:

- [UA](./task_description_ua.md)
- [EN](./task_description_en.md)

#### Table of contents:

- [Description](#description)
- [Dependencies to run the app](#requirements-to-run-the-app)
- [Steps to run app](#steps-to-run-app)
- [How to run tests](#how-to-run-tests)
- [Types of commits](#types-of-commits)
- [License](#license)


#### Description:
- This is a simple task tracker that allows you to create/edit/delete tasks.
- Each task has:
  - Name
  - Description
  - Responsible person
  - Performers
  - Status (TODO, In progress, Done)
  - Priority

#### Requirements to run the app:

- Python: app was developed and tested using **3.12** version, but it should work with 3.10+ version
- External python libraries: check [Pipfile](./Pipfile)

#### Steps to run app

To start the project correctly, you need to follow these steps: 
1. Create an .env file similar to this one
```ini
    # Database setting
    DB_NAME=simple_task_tracker.db
    
    # To test authorization
    TEST_USERNAME=test_user
    TEST_PASSWORD=12345
    TEST_EMAIL=test_user_email@email.com
    
    # Secret key for JWT
    SECRET=b26d34b99a811c37ba23ec9c8f2f17380a2ab376f1e334dbf9b4b0bde77165e702a6d2a110c57653325f3ac50827d4b77bcdcaeef5a1fb1f323ada4d6c11baa6af00a8a1b6dd84d5b4b8dc34955dd707088b3ee5d65c692782dfb640c46d6ea87638cb401dadb335388857a0e52c3133fa324155bb127717c613dbfc43ddadf30b5bf07bf11f8f75343e81dd31d1a8e8cdf7a9b287f630dc5766cb9b6c11ea475464a1f6434d8caa3fb76ada993009356e4c609890d94e22c478290e581f8933309d5a2d8f122a25924e3028d44e91bcae615583a20545396a594ebedd9aa065041d0199406288d99822b5f224d762798de02f7eb8529e83b166b49b9ab40ac9
    
    # Setting for Logger
    START_SETTING=DEV
  
    # The pipenv setting that allows you to create a virtual environment in a project
    PIPENV_VENV_IN_PROJECT=1
  ```
2. After you have created the .env, you should have the pipenv library 
   installed on your computer, if you do not have it installed, install it with the command 
` pip install pipenv`


3. To install all dependencies, run the `pipenv install` command to create a virtual environment and install all dependencies
    and after run the `pipenv shell` to activate virtualenv, you can check all installed libraries
    with the `pip list`/`pip freeze` command, or you can check the [Pipfile](./Pipfile)


4. The next step is to create a database using migrations,
to do this you need to run the command `alembic upgrade head`


5. Now that the database has been created, you can easily run the application 
with the command `uvicorn src.main:app --reload`


6. Go to localhost:8000/docs or http://127.0.0.1:8000/docs
to view the endpoints

#### How to run tests:

- Go to terminal and run next command
```bash
python -m pytest '@tests_to_run.txt'
```

#### Types of commits

- `chore`: changes that do not directly affect the code, something that the end user will not see (installing/removing dependencies, project/tool settings)
- `docs`: changes related to documentation
- `feat`: new feature
- `fix`:  bug fix
- `perf`: changes related to performance improvement
- `refactor`: changes that are not related to feat or fix
- `revert`: revert a commit
- `test`: adding new tests or fixing existing ones

#### License

This project is licensed under the MIT License.