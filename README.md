# Research Project for 3rd Year Computer Science Module

## Aims

1. Improve upon the current system in place.
2. Increase our understanding of software engineering practices and procedures.
3. Learn about new frameworks and improve our understanding of technology we are familiar with.

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

## Installation guide

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

   - Should you already have tables setup via the above command from a previous pull, you must first delete those tables with a "drop tables" command or via your UI of choice
   - Ensure you have a db runing locally called "research_dev"
   - Then DELETE the migrations folder, and run the following commands (within virtual env)

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

## Conclusion

Should there be any queries please contact me
