import bcrypt
from sqlalchemy import select, update, delete, insert
from sqlalchemy.exc import CompileError
from models.tables import User
from sentry_sdk import capture_message
from views.display import View
from controllers.actions_utils import ask_values


from views.display import View

view = View()


def read_user(session, readonly=True, user=None, **kwargs):
    """
    User choose how to filter users: all , name, email, phone

    Args:
        readonly (bool) : True print the result / False return the result
    """
    filtering_options = {
        "all": read_user_all,
        "name": read_user_by_name,
        "email": read_user_by_email,
        "phone": read_user_by_phone,
        "-BACK-": "back",
    }
    action = view.select_action(message="", action_dict=filtering_options)
    if action == "back":
        return
    else:
        return action(session, readonly, **kwargs)


def read_user_all(session, readonly=True, user=None, **kwargs):
    """
    User retrieves every users in  the database

    Args:
        readonly (bool) : True print the result / False return the result
    """
    result = session.scalars(select(User)).all()
    if readonly:
        view.basic_list(result)
        session.close()
        return
    else:
        return result


def read_user_by_name(session, readonly=True, user=None, **kwargs):
    """
    User retrieves users with partial name match from string input

    Args:
        readonly (bool) : True print the result / False return the result
    """
    user_name = view.user_input(detail="users's name")
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


def read_user_by_email(session, readonly=True, user=None, **kwargs):
    """
    User retrieves users with partial email match from string input

    Args:
        readonly (bool) : True print the result / False return the result
    """
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


def read_user_by_phone(session, readonly=True, user=None, **kwargs):
    """
    User retrieves users with partial phone match from string input

    Args:
        readonly (bool) : True print the result / False return the result
    """
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


def create_user(session, readonly=True, user=None, **kwargs):
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
            role_dict = {"manager": 2, "sale": 3, "support": 4}
            role = view.select_action(action_dict=role_dict)
            values[k] = role
        else:
            values[k] = view.user_input(detail=k)
    stmt = insert(User).values(values)
    try:
        session.execute(stmt)
        session.commit()
        capture_message(f"user: {user.id} {user.name} {user.email} added {User}")
    except:
        session.rollback()
    session.close()
    return


def update_user(session, readonly=True, user=None, **kwargs):
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
        capture_message(f"user: {user.id} {user.name} {user.email} updated {User}")
    except CompileError as er:
        view.error_message(er)
        session.rollback()
    finally:
        return


def delete_user(session, readonly=True, user=None, **kwargs):
    users = read_user_by_name(session, readonly=False)
    user_selected = view.select_obj_from_list(users)
    stmt = delete(User).where(User.id == user_selected.id)

    try:
        session.execute(stmt)
        session.commit()
        capture_message(f"user: {user.id} {user.name} {user.email} deleted {User}")
    except:
        session.rollback()
    session.close()
    return


def change_password(session, readonly=False, user=None, **kwargs):
    stmt_original_password = select(User).where(User.id == user.id)
    result = session.execute(stmt_original_password).first()
    original_password = result.User.password
    new_password = view.change_password(original_password=original_password)
    new_password = bcrypt.hashpw(new_password, bcrypt.gensalt())
    stmt = update(User).where(User.id == user.id).values(password=new_password)
    try:
        session.execute(stmt)
        session.commit()
        view.basic(message="update successful")
        capture_message(
            f"user: {user.id} {user.name} {user.email} changed their password"
        )
    except CompileError as er:
        view.error_message(er)
        session.rollback()
    finally:
        return
