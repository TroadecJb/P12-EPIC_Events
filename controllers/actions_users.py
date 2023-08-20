from sqlalchemy import select, update, delete, insert
from sqlalchemy.exc import InvalidRequestError, CompileError
from models.tables import User, Client, Contract, Event, Company, Address
import datetime
import bcrypt
from views.display import View
from controllers.actions_utils import ask_values, select_obj_from_list

from views.display import View

view = View()


def read_user(session, readonly=True, **kwargs):
    """
    User can filter events by Date, Client, Support_id, number_attendee
    """
    filterting_options = {
        "all": read_user_all,
        "name": read_user_by_name,
        "email": read_user_by_email,
        "phone": read_user_by_phone,
    }
    view.basic(message="select the field to use")
    view.dict_k(filterting_options)
    choice = view.user_input()
    if choice in filterting_options.keys():
        return filterting_options[choice](session, readonly, **kwargs)
    else:
        view.error_input()
        return read_user(session, readonly, **kwargs)


def read_user_all(session, readonly=True, **kwargs):
    result = session.scalars(select(User)).all()
    if readonly:
        view.basic_list(result)
        session.close()
        return
    else:
        return result


def read_user_by_name(session, readonly=True, **kwargs):
    user_name = view.user_input(detail="user's name")
    stmt = select(User).where(User.name.contains(user_name))
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


def read_user_by_email(session, readonly=True, **kwargs):
    user_email = view.user_input(detail="user's email")
    stmt = select(User).where(User.email.contains(user_email))
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


def read_user_by_phone(session, readonly=True, **kwargs):
    user_phone = view.user_input(detail="user's phone")
    stmt = select(User).where(User.email.contains(user_phone))
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


def create_user(session, readonly=True, **kwargs):
    values = {
        "name": None,
        "email": None,
        "phone": None,
        "password": None,
    }
    for k in values.keys():
        print(k)
        if k in "password":
            pwd = view.user_input()
            pwd = bcrypt.hashpw(b"pwd", bcrypt.gensalt())
            values[k] = pwd
        else:
            values[k] = view.user_input()
    print(values)
    session.execute(insert(User).values(values))
    session.commit()
    session.close()
    return


def update_user(session, readonly=True, **kwargs):
    users = read_user_by_name(session, readonly=False)
    user_selected = None
    if type(users) is list:
        user_selected = view.select_from(users)
    else:
        user_selected = users[0]
    view.basic(user_selected)
    values = ask_values()
    stmt = update(User).where(User.id == user_selected.id).values(values)
    try:
        session.execute(stmt)
        session.commit()
        view.basic(message="update successful")
    except CompileError as er:
        view.error_message(er)
        session.rollback()
    finally:
        return


def delete_user(session, readonly=True, **kwargs):
    users = read_user_by_name(session, readonly=False)
    user_selected = view.select_from(users)
    stmt = delete(User).where(User.id == user_selected.id)
    session.execute(stmt)
    session.commit()
    session.close()
    return
