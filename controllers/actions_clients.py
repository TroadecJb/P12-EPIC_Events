from sqlalchemy import select, update, delete, insert
from sqlalchemy.exc import InvalidRequestError, CompileError
from models.tables import User, Client, Contract, Event  # , Company, Address
import datetime
from views.display import View
from controllers.actions_utils import ask_values, select_obj_from_list
from sentry_sdk import capture_message

view = View()


def read_clients(session, readonly=True, **kwargs):
    """
    User can choose between all clients or proceed by client's name.
    if readonly=False return either list of obj or single obj.
    """
    # all_clients = view.user_input(detail="all?")
    all_clients = view.confirm(message="every client?")
    if readonly:
        if all_clients:
            result = session.scalars(select(Client)).all()
            view.basic_list(result)
            session.close()
            return
        else:
            result = read_client_by_name(session, readonly)
            return
    else:
        if all_clients:
            result = session.scalars(select(Client)).all()
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
            return result


def read_client_in_charge(session, readonly=True, user=None, **kwargs):
    """
    User can search by complete or partial client's name
    if readonly=False return either list of obj or single obj
    """
    stmt = select(Client).where(Client.commercial.id == user.id)
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
            return result
        else:
            return result[0]


def update_client(session, user=None, **kwargs):
    clients = read_client_by_name(session, readonly=False)
    client_selected = None
    if type(clients) is list:
        client_selected = view.select_obj_from_list(clients)
    else:
        client_selected = clients
    view.basic(client_selected)
    values = ask_values()
    stmt = update(Client).where(Client.id == client_selected.id).values(values)
    try:
        session.execute(stmt)
        session.commit()
        view.basic(message="update successful")
        capture_message(f"Client updated:{user}")
    except CompileError as er:
        view.error_message(er)
        session.rollback()
    finally:
        return


def update_client_in_charge(session, user=None, **kwargs):
    clients = read_client_in_charge(session, user=user, readonly=False)
    client_selected = None
    if type(clients) is list:
        client_selected = view.select_obj_from_list(clients)
    else:
        client_selected = clients[0]
    view.basic(client_selected)
    values = ask_values()
    stmt = update(Client).where(Client.id == client_selected.id).values(values)
    try:
        session.execute(stmt)
        session.commit()
        view.basic(message="update successful")
        capture_message(f"Client updated:{user}")
    except CompileError as er:
        view.error_message(er)
        session.rollback()
    finally:
        session.close()
        return


def delete_client(session, user=None, **kwargs):
    clients = read_client_by_name(session, readonly=False)
    client_selected = view.select_obj_from_list(clients)
    stmt = delete(Client).where(Client.id == client_selected.id)
    try:
        session.execute(stmt)
        session.commit()
    except:
        session.rollback()
        view.error_message()
        session.close()
    capture_message(f"Client deleted:{user}")
    view.basic(message="deletion succesful")
    session.close()
    return


def create_client(session, user=None):
    values = {
        "name": None,
        "email": None,
        "phone": None,
        "contact_first": None,
        "contact_last": None,
        "company": None,
        "address": None,
    }
    for k in values.keys():
        if k in ["contact_first", "contact_last"]:
            view.basic(message=k)
            date = view.user_input("YYYY,MM,DD")
            date = [int(x) for x in date.split(",")]
            input_date = datetime.date(date[0], date[1], date[2])
            values[k] = input_date
        else:
            values[k] = view.user_input(k)
    values["commercial_id"] = user.id
    view.basic(message=values)
    confirm = view.confirm("Confirm informations")
    if confirm:
        try:
            session.execute(insert(Client).values(values))
            capture_message(f"user: {user} added Client: {Client} {values}")
            capture_message(f"user: {user} added Client: {values}")
            capture_message(f"user: {user} added Client")
            capture_message(f"user: {user.id} {user.name} {user.email} added Client")
            print(user)
            session.commit()

            view.basic(message="creation succesful")
        except CompileError as er:
            session.rollback()
        finally:
            session.close()
            print(user)
            return
    else:
        return create_client(session=session, user=user)
