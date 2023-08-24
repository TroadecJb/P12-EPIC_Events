import datetime
import bcrypt
from sqlalchemy import select, update, delete, insert
from sqlalchemy.exc import InvalidRequestError, CompileError
from models.tables import Role, User, Client, Contract, Event  # , Company, Address

from views.display import View
from controllers.actions_utils import ask_values, select_obj_from_list
from utils.basic_utils import pwd_hashed

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
    if "user_role" in kwargs:
        user_role = kwargs["user_role"]
        user_name = view.user_input(detail=f"{user_role}'s name")
    else:
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
        "role_id": None,
        "password": None,
    }
    for k in values.keys():
        if k == "password":
            pwd = view.user_input(detail=k).encode("utf-8")
            hashed_pwd = bcrypt.hashpw(pwd, bcrypt.gensalt())
            values[k] = hashed_pwd
        elif k == "role_id":
            role_dict = {"manager": 1, "sale": 3, "support": 4}
            role = view.user_input(detail="manager/sale/support")
            values[k] = role_dict[role]
        else:
            values[k] = view.user_input(detail=k)
    print(values)
    stmt = insert(User).values(values)
    session.execute(stmt)
    session.commit()
    session.close()
    return


def update_user(session, readonly=True, **kwargs):
    users = read_user_by_name(session, readonly=False)
    user_selected = None
    if type(users) is list:
        user_selected = view.select_obj_from_list(users)
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
    user_selected = view.select_obj_from_list(users)
    stmt = delete(User).where(User.id == user_selected.id)
    session.execute(stmt)
    session.commit()
    session.close()
    return


def change_password(session, readonly=False, user=None, **kwargs):
    new_pwd = view.user_input(detail="new password")
    new_pwd = pwd_hashed(new_pwd.encode("utf-8"))
    stmt = update(User).where(User.id == user.id).values(password=new_pwd)
    try:
        session.execute(stmt)
        session.commit()
        view.basic(message="update successful")
    except CompileError as er:
        view.error_message(er)
        session.rollback()
    finally:
        return
