# Research Project for 3rd Year Computer Science Module

To access a hosted version of this repository, please visit

[Hosted version of the website](https://flask-sfi.herokuapp.com/)

# Streamlined set up guide

### Install prerequisites

- Git
- Python
- npm (node)
- Postgresql

### Activate and create your virtual environment

    ```bash
    python -m venv venv
    source venv/bin/activate
    ```

### Start up postgresql and create a database "research_dev"

    ```bash
        For example you could run the following in a terminal;
        psql -h localhost -U user_name

        create database research_dev;
    ```

### Run the first-time setup script

    ```bash
    ./first-time-setup.sh

    ```

### Finally, run the app

    ```bash
        flask run
    ```


# Old/manual version

## Running the app

1.  Activate your venv

    ```bash
        source venv/bin/activate
    ```

    Or, on Windows

    ```bash
        venv\Scripts\activate.bat
    ```

2.  Run flask
    ```bash
        flask run
    ```

## Installation guide (Setup guide)

1. Download & Install python/git/npm (if you haven't already)

   #### Python

   [Any OS](https://www.python.org/downloads/ "Python")

   Or, for linux (debian)

   ```bash
       sudo apt install python
   ```

   #### Git

   [Any OS](https://git-scm.com/downloads "Git")

   Or, for linux (debian)

   ```bash
       sudo apt install git
   ```

   #### NPM/Node

   [Any OS](https://nodejs.org/en/download/ "NPM")

   Or, for linux (debian)

   ```bash
       sudo apt install nodejs
   ```

2. Clone this repository:

   #### Terminal

   ```bash
      git clone https://github.com/dwalsh01/research-project.git
   ```

   #### Github Desktop

   Windows and Mac users can use [Github Desktop](https://desktop.github.com/ "Github Desktop")

3. Then create a "virtual environment":

   Do this in the "research-project" directory.

   ```bash
       mkdir venv
       python -m venv venv
   ```

4. You must then activate the virtual environment:

   #### Bash/Terminal

   ```bash
       source venv/bin/activate
   ```

   #### Windows

   ```bash
       venv/Scripts/activate.bat
   ```

5. Install the requirements:

   ```bash
       pip install -r requirements.txt
   ```

6. Setting up the postgres db:

   - Install postgresql
   - Create a database called "research_dev"
   - Ensure you have a db running locally called "research_dev"

   ```bash
       flask db init
       flask db migrate
       flask db upgrade
   ```

7. Now we move on to installing the ReactJS frontend:

   - install dependencies with npm:

   ```bash
       cd research-react
       npm install
       npm run-script build
   ```

8. To run the project:
   ```bash
       flask run
   ```
