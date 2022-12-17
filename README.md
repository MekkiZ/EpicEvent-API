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
```
psql postgres
```
```angular2html
CREATE DATABASE epicevent;
```
```angular2html
CREATE USER mek WITH PASSWORD 'mekki';
```
```angular2html
GRANT ALL PRIVILEGES ON DATABASE epicevent TO mek;
```
```angular2html
\q
```
## Setup
Create a virtualenv for the project with Python 3.10

Copie the Git-Link and after (git clone ' git link project ' )

After on directory projet12:

```
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```
```
pip install --upgrade pip
```
```
 pip3 install psycopg2
```
# Run the script

Run this command :
```
cd Epicevent
```
And now you have to create SuperUSer, a manager of API;

```
python3 manage.py createsuperuser
```
###please Be carful, remember your username and password


and after this:
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

If the terminal told you to migrate on red script :
push at same time CONTROL-C and 

Past this :
```
python3 manage.py migrate
```

after that open postgresql :
```
psql postgres
```
copy that :
```angular2html
\connect epicevent
```
```angular2html
INSERT INTO epicevent.public.auth_group (id, name) VALUES (1, 'team_gestion'), (2, 'team_sales'), (3, 'team_support')
```
```angular2html
INSERT INTO epicevent.public.api_eventstatus (id, event_statu) VALUES (1, 'Begin'), (2, 'End')
```

and after this:
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
