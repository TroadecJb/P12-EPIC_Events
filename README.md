# P12-EPIC_Events

## Overview
This project is a CRM programm (CLI python) to manage a database and perform specific actions on its content.  
Users identified by their account can perform job's specific actions over four types of entities (User, Client, Contract, Event).  
Out of the box it uses a sqlite3 databse (comes with python), using SQLAlchemy to manage the database and setup to log with Sentry.

## Usage
Start the main.py file.  
Provide valid credentials (email and password to authenticate).  
Navigate the menus with arrow keys (inquirerpy is used to implement it) and follow the provided instructions.  
Each user can logout so that another user can login using its own credentials.



## Config file
Edit `config.txt` to customize the default parameters (sqlite3 database location and name, Sentry DSN key, default admin credentials (only account at start)).  
to specify sqlite3 database location and its name.

section `CONFIG`:
- **Databse**  
By default the database will be created in the same folder as the `main.py` file under the name `epic_events.sqlite`.  
- **Sentry**  
Sentry DSN key is empty, you will have to provide it.  
To create an account and your own Sentry DSN key go to their [website](https://sentry.io/welcome/)

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
Naviation in the menu is done by using `arrow keys` and validing the choice with `enter`.  
Confirmation prompt are either confirmed or denied with `y` or `n`.

### Input
Input like text or numbers are sent after pressing `enter`.  

The creation of new entities (User, Client, Contract, Event) will prompt you the field you are filling (name, address, etc).  

The modification of an entity will ask you the name of the field you want to modify and then asky you the new value of this field, for example:  
```
>>> ? name of the field to modify 
>>> name
>>> ? new value
>>> new name
>>> ? modify any other field?
>>> [y/n]
```

## Logging
If a valid Sentry DSN key is provided, from your dashboard errors from manipulation of the database will visible.  
Event from valid manipulation of the database will be displayed too.  
Each event will have `id` and  `name` from which user made the change and details about it: `creation` `modification` `deletion` and on which entity `id` and nature.  