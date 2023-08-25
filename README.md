# P12-EPIC_Events

## Overview
This project is a CRM programm (CLI python) to manage a database and perform specific actions on its content.  
Users identified by their account can perform job's specific actions over four types of entities (User, Client, Contract, Event).  
Out of the box it uses a sqlite3 databse (comes with python), using SQLAlchemy to manage the database and setup to log with Sentry.

## Usage
Start the `main.py` file.  
Provide valid credentials (email and password to authenticate).  
Navigate the menus with arrow keys (InquirerPy is used to implement it) and follow the provided instructions.  
Each user can logout for another user to login using its own credentials.



## Config file
Edit `config.txt` to customize the default parameters (sqlite3 database location and name, Sentry DSN key, default admin credentials (only account at start)).  
to specify sqlite3 database location and its name.

section `CONFIG`:
- **Databse**  
By default the database will be created in the same folder as the `main.py` file under the name `epic_events.sqlite`.  
- **Sentry**  
Sentry DSN key is empty, it has to be provided.  
To create an account and get a Sentry DSN key, go to their [website](https://sentry.io/welcome/)

section `admin_basic`:
- The default account has admin permission level and comes with the following credentials  
**email =** `mail@ad.min`  
**password =** `ChangeMe`
- Those credentials can be change in the `config.txt` file before initializing the databse (done at first start).
- The password can also be change at any point in the programm even after the first start.


## Installation
Clone the repository  
`gh repo clone TroadecJb/P12-EPIC_Events`  

Create a virtual environment  
`python3 -m venv venv`  

Activate it:
- activation windows  
`$ ~<environment name>\Scripts\activate.bat`  
- activation macos / linux  
`$ ~source <environment name>/bin/activate`  

Install required depedencies  
`pip install -r requirements.txt`

## Requirements
bcrypt==4.0.1  
inquirerpy==0.3.4  
SQLAlchemy==2.0.19  
sentry-sdk==1.29.2

Sentry needs [sqlalchemy extra](https://docs.sentry.io/platforms/python/configuration/integrations/sqlalchemy/)

See `requirements.txt` for more informations.

## Examples
### Navigation
Menu navifation is done by using `arrow keys` and validating the choice with `enter`.  
Confirmation prompt is either confirmed or denied with `y` or `n`.

### Input
Inputs like text or numbers are sent after pressing `enter`.  

The creation of new entitiy (User, Client, Contract, Event) will prompt the field to fill in (email, address, price, etc).  

The modification of an entity (User, Client, Contract, Event) will ask the name of the field to modify, then the new value for this field. For example:
```
>>> ? name of the field to modify 
>>> name
>>> ? new value
>>> new name
>>> ? modify any other field?
>>> [y/n]
```

## Logging
If a valid Sentry DSN key is provided, from your dashboard errors from manipulation of the database will be visible.  
Event from valid database manipulation will be displayed too.  
Each event will have the `id` and the `name` of the user who mades the changes and details about them : `creation` `modification` `deletion`, and details about the entity itself.

## Database Diagram

![Diagram_epic_events_db](https://github.com/TroadecJb/P12-EPIC_Events/assets/110687346/8052f0bb-9ac6-4f04-9e55-c07b73ef3589)

