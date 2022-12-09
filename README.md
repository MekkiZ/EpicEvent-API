# SoftDesk API
## Description
This API handle the enterprise structures, with client and contrat for events
## install and Create ddb Postgresql

### linux:
```angular2html
sudo apt-get update
sudo apt-get install python-pip python-dev libpq-dev postgresql postgresql-contrib
```

On macOS, you can install posgresql in the terminal with brew:
```angular2html
brew install postgresql
```
Now, you may start up postresql after its installation with the following command.
```angular2html
brew services start postgresql
```
```angular2html
sudo su - postgres
```
```angular2html
psql
```
```angular2html
CREATE DATABASE mydb;
```
```angular2html
CREATE USER myuser WITH PASSWORD 'password';
```
```angular2html
GRANT ALL PRIVILEGES ON DATABASE mydb TO myuser;
```
```angular2html
\q
```
```angular2html
exit
```

## Setup
Create a virtualenv for the project with Python 3.10

Copie the Git-Link and after  
```
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```
# Run the script

Run this command :
```
cd softdesk
```
And  :
```
python3 manage.py runserver
```

You will have :
```
System check identified no issues (0 silenced).
November 19, 2022 - 13:29:10
Django version 4.1.3, using settings 'softdesk.settings'
Starting development server at http://127.0.0.1:8000/
Quit the server with CONTROL-C.

```
Copy this link on your favorite browser :
http://127.0.0.1:8080/


After enjoy