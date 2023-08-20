from sqlalchemy import select, update, delete, insert
from sqlalchemy.exc import InvalidRequestError, CompileError
from models.tables import User, Client, Contract, Event, Company, Address
import datetime
from views.display import View
from controllers.actions_utils import ask_values, select_obj_from_list
from controllers.actions_companies import read_company_by_name

view = View()


def read_clients(session, readonly=True, **kwargs):
    """
    User can choose between all clients or proceed by client's name.
    if readonly=False return either list of obj or single obj.
    """
    all_clients = view.user_input(detail="all?")
    if readonly:
        if all_clients in ["y", "ye", "yes"]:
            result = session.scalars(select(Client)).all()

            view.basic_list(result)
            session.close()
            return
        else:
            result = read_client_by_name(session, readonly)
            return
    else:
        if all_clients in ["y", "ye", "yes"]:
            result = session.scalars(select(Client)).all()
            # view.basic_list(result)
            return result
        else:
            result = read_client_by_name(session, readonly=False)
            return result


def read_client_by_name(session, readonly=True, **kwargs):
    """
    User can search by complete or partial client's name
    if readonly=False return either list of obj or single obj
    """
    client_name = view.user_input(detail="client's name")
    stmt = select(Client).where(Client.name.contains(client_name))
    result = session.scalars(stmt).all()
    if readonly:
        if len(result) > 1:
            view.basic_list(result)
            session.close()
            return
        else:
            view.basic(result[0])
            session.close()
            return
    else:
        if len(result) > 1:
            # view.basic_list(result)
            return result
        else:
            # view.basic(result[0])
            return result[0]


def update_client(session, **kwargs):
    clients = read_client_by_name(session, readonly=False)
    client_selected = None
    if type(clients) is list:
        client_selected = view.select_from(clients)
    else:
        client_selected = clients[0]
    view.basic(client_selected)
    values = ask_values()
    stmt = update(Client).where(Client.id == client_selected.id).values(values)
    try:
        session.execute(stmt)
        session.commit()
        view.basic(message="update successful")
    except CompileError as er:
        view.error_message(er)
        session.rollback()
    finally:
        return


def delete_client(session, **kwargs):
    clients = read_client_by_name(session, readonly=False)
    client_selected = view.select_from(clients)
    stmt = delete(Client).where(Client.id == client_selected.id)
    session.execute(stmt)
    session.commit()
    session.close()
    return


def create_client(session, user):
    values = {
        "name": None,
        "email": None,
        "phone": None,
        "contact_first": None,
        "contact_last": None,
        "company": None,
    }
    for k in values.keys():
        print(k)
        if k in ["contact_first", "contact_last"]:
            date = view.user_input("YYYY,MM,DD")
            date = [int(x) for x in date.split(",")]
            input_date = datetime.date(date[0], date[1], date[2])
            values[k] = input_date
        elif k in ["company"]:
            company = read_company_by_name(session, readonly=False)
            if type(company) is list:
                company = view.select_from(company)
            values[k] = company.id
        else:
            values[k] = view.user_input()
    values["commercial_id"] = user.id
    print(values)
    session.execute(insert(Client).values(values))
    session.commit()
    session.close()
    return
