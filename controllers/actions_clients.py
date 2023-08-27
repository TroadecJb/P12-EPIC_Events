from sqlalchemy import select, update, delete, insert
from sqlalchemy.exc import CompileError
from models.tables import Client
import datetime
from views.display import View
from controllers.actions_utils import ask_values
from sentry_sdk import capture_message

view = View()


def read_clients(session, readonly=True, **kwargs):
    """
    User can choose between all clients or proceed by client's name.
    if readonly=False return either list of obj or single obj.
    """
    all_clients = view.confirm(message="every client?")
    if readonly:
        if all_clients:
            result = session.scalars(select(Client)).all()
            if result:
                view.basic_list(result)
                session.close()
                return
            else:
                view.basic(message="No Client")
                return
        else:
            result = read_client_by_name(session, readonly)
            return
    else:
        if all_clients:
            result = session.scalars(select(Client)).all()
            if result:
                return result
            else:
                view.basic(message="No client")
                return False
        else:
            result = read_client_by_name(session, readonly=False)
            if result:
                return result
            else:
                view.basic(message="No client")
                return False


def read_client_by_name(session, readonly=True, **kwargs):
    """
    User can search by complete or partial client's name
    if readonly=False return either list of obj or single obj
    """
    client_name = view.user_input(detail="client's name")
    stmt = select(Client).where(Client.name.contains(client_name))
    result = session.scalars(stmt).all()
    if result:
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
            return result

    else:
        view.basic(message="No client")
        return False


def read_client_in_charge(session, readonly=True, user=None, **kwargs):
    """
    User can search by complete or partial client's name
    if readonly=False return either list of obj or single obj
    """
    stmt = select(Client).where(Client.commercial.id == user.id)
    result = session.scalars(stmt).all()
    if result:
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
                return result
    else:
        view.basic(message="No client")
        return


def update_client(session, user=None, **kwargs):
    clients = read_client_by_name(session, readonly=False)
    if clients:
        client_selected = view.select_obj_from_list(clients)
        view.basic(client_selected)
        values = ask_values()
        stmt = update(Client).where(Client.id == client_selected.id).values(values)
        try:
            session.execute(stmt)
            capture_message(
                f"user: {user.id} {user.name} {user.email} deleted {client_selected.id} {client_selected.name} with {values.items()}"
            )
            session.commit()
            view.success(message="update done")
        except CompileError as er:
            view.error_message(er)
            session.rollback()
        finally:
            return
    else:
        return


def update_client_in_charge(session, user=None, **kwargs):
    clients = read_client_in_charge(session, user=user, readonly=False)
    if clients:
        client_selected = view.select_obj_from_list(clients)
        view.basic(client_selected)
        values = ask_values()
        stmt = update(Client).where(Client.id == client_selected.id).values(values)
        try:
            session.execute(stmt)
            capture_message(
                f"user: {user.id} {user.name} {user.email} upated {client_selected.id} {client_selected.name} with {values.items()}"
            )
            session.commit()
            view.success(message="update done")
        except CompileError as er:
            view.error_message(er)
            session.rollback()
        finally:
            session.close()
            return
    else:
        return


def delete_client(session, user=None, **kwargs):
    clients = read_client_by_name(session, readonly=False)
    if clients:
        client_selected = view.select_obj_from_list(clients)
        stmt = delete(Client).where(Client.id == client_selected.id)
        try:
            session.execute(stmt)
            capture_message(
                f"user: {user.id} {user.name} {user.email} deleted {client_selected.id} {client_selected.name}"
            )
            session.commit()
            view.success(message="deletion done")
        except:
            session.rollback()
            view.error_message()
            session.close()
            return
        session.close()
        return
    else:
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
            capture_message(
                f"user: {user.id} {user.name} {user.email} added Client {values.items()}"
            )
            session.commit()
            view.success(message="creation done")
        except CompileError as er:
            session.rollback()
        finally:
            session.close()
            return
    else:
        return create_client(session=session, user=user)
