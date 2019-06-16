# web-screenshot-importer

Capture a screenshot of a web page by providing it’s URL

## Technologies used
* **[Virtualenv](https://virtualenv.pypa.io/en/stable/)**
* **[Python3](https://www.python.org/downloads/)**
* **[Flask](flask.pocoo.org/)**
* **[Flask-RESTful](https://flask-restful.readthedocs.io/en/latest/index.html)**
* Minor dependencies can be found in the requirements.txt file on the root folder.

## Installation / Usage

* First ensure you have python3 globally installed in your computer. If not, you can get python3 [here](https://www.python.org).
* After this, ensure you have installed virtualenv globally as well. If not, run this:
    ```
        $ pip install virtualenv
    ```
* Git clone this repo to your PC
    ```
        $ git clone https://github.com/klapen/web-screenshot-importer.git
    ```

* #### Dependencies
    1. Cd into your the cloned repo as such:
        ```
        $ cd web-screenshot-importer
        ```

    2. Create and fire up your virtual environment in python3:
        ```
        $ virtualenv -p python3 venv
        $ source venv/bin/active
        ```

* #### Environment Variables
    Create the following file and add the following:
    ```
    $ export SECRET="some-very-long-string-of-random-characters"	
    $ export APP_SETTINGS="development"
    $ export AWS_ACCESS_KEY_ID="aws_access_key_id"
    $ export AWS_SECRET_ACCESS_KEY="aws_secret_access_key"
    $ export APP_TEMP_FOLDER="path/to/repo/tmp"
    ```

    If you are on MacOS or Linux, you can use the **set_enviroment_vars_template.sh** to change the values and run the script.

    To create SECRET varible, you can use the command:
    ```
    $ openssl rand -base64 64
    ```

* #### Before running
    Install your requirements
    ```
    (venv)$ pip install -r requirements.txt
    ```

    And initialize the database:
    ```
    (venv)$ python src/init_db.py
    ```
        
* #### Running Api
    On your terminal, run the server using this one simple command:
    ```
    (venv)$ python src/api.py
    ```
    You can now access api endpoints on:
    ```
    http://localhost:5000/api/
    ```
    
* #### Running Test
    On your terminal, run the test using this one simple command:
    ```
    (venv)$ cd src/
    (venv)$ python run_tests.py
    ```
    This command will look on *tests* folder to files like *test_&ast;.py*, to run tests.

    If you want to run just one test, use the following command:
    ```
    (venv)$ cd src/
    (venv)$ python -m unittest tests.test_maintenance
    ```

* #### Database migration
    If you requiere to change the database scheme, remember to migrate it:
    ```
    (venv)$ cd src/
    (venv)$ python migrate.py db migrate
    ```
    For more information how migration work, please check [Flask-migrate](https://flask-migrate.readthedocs.io/en/latest/) documentation webpage.

* #### Docker image
    To run it on Docker, first build the image:
    ```
    $ cd web-screenshot-importer
    $ docker build -t screenshot-importer:latest .
    ```

    To run the container:
    ```
    $ docker run -it --name screenshot-importer -e AWS_ACCESS_KEY_ID=aws_access_key_id -e AWS_SECRET_ACCESS_KEY=aws_secret_access_key --rm -p 5000:5000 screenshot-importer
    ```
