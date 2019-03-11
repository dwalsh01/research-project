echo "Welcome to first time setup."
echo "Installing python dependencies"

pip install -r requirements.txt

echo "Please ensure you have a local postgres DB running with a database named \"research_dev\""
echo "Enter in your local postgres details below. They will then be saved in a .env file for ease of use."
echo "---"
echo "Please enter in your postgres username:"
read p_user

echo "Please enter your postgres password"
read p_password

cat > .env << EOF 
export DATABASE_URL='postgresql://$p_user:$p_password@localhost/research_dev'
EOF

echo ".env file created"

echo "Assuming git submodule research-react is cloned."
cd research-react

echo "Installing NPM dependencies"
npm install

echo "Building Javascript font-end"
npm run-script build

echo "Populating the database"

flask db migrate
flask db upgrade

source .env
cd sfi/tests
pytest > dev/null

echo "-----------------------------------------------------------------------"
echo "First time setup complete."
echo "execute the command 'flask run' to run the app"
echo "-----------------------------------------------------------------------"
