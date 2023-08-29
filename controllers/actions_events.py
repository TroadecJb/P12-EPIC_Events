import datetime
from sqlalchemy import select, update, delete, insert
from sqlalchemy.exc import CompileError
from models.tables import User, Client, Contract, Event

from views.display import View
from controllers.actions_utils import ask_values
from controllers import actions_users, actions_contracts
from sentry_sdk import capture_message

view = View()


def read_event(session, readonly=True, **kwargs):
    """
    User can filter events by Date, Client, Support_id, number_attendee
    """
    filterting_options = {
        "all": read_event_all,
        "client": read_event_by_client_name,
        "date": read_event_by_date,
        "support": read_event_by_support_name,
        "number_attendee": read_event_by_attendee,
    }
    action = view.select_action(message="", action_dict=filterting_options)
    if action == "back":
        return
    else:
        return action(session, readonly, **kwargs)


def read_event_all(session, readonly=True, **kwargs):
    result = session.scalars(select(Event)).all()
    if result:
        if readonly:
            view.basic_list(result)
            session.close()
            return
        else:
            return result
    else:
        view.basic(message="No event")
        if readonly:
            return False
        return


def read_event_by_client_name(session, readonly=True, **kwargs):
    client_name = view.user_input(detail="client's name")
    stmt = (
        select(Event)
        .join(Contract)
        .join(Client)
        .where(Client.name.contains(client_name))
    )
    result = session.execute(stmt).all()
    if len(result) > 1:
        if readonly:
            view.basic_list(result)
            session.close()
            return
        return result
    elif len(result) == 1:
        if readonly:
            view.basic(result[0])
            session.close()
            return
        return result[0]
    else:
        view.basic(message="no match")
        session.close()
        return


def read_event_by_date(session, readonly=True, **kwargs):
    specific_date = view.user_input(detail="specific date?")
    if specific_date in ["y", "yes", "yes"]:
        date = view.user_input("YYYY,MM,DD")
        date = [int(x) for x in date.split(",")]
        date = datetime.date(date[0], date[1], date[2])
        stmt = select(Event).where(Event.date_begin == date)
        result = session.scalars(stmt).all()
    else:
        stmt = select(Event).order_by(Event.date_begin)
        result = session.scalars(stmt).all()
    if len(result) < 1:
        view.basic(message="No match!")
        return
    else:
        if len(result) > 1:
            if readonly:
                view.basic_list(result)
                session.close()
                return
            return result
        else:
            if readonly:
                view.basic(result[0])
                session.close()
                return
            return result[0]


def read_event_by_support_name(session, readonly=True, **kwargs):
    """
    User can search by complete or parital client's name.
    If readonly=False return either list of obj or single obj
    """
    support_name = view.user_input(detail="commercial's name")
    stmt = select(Event).join(User).where(User.name.contains(support_name))
    result = session.execute(stmt).all()
    if len(result) > 1:
        if readonly:
            view.basic_list(result)
            session.close()
            return
        return result
    elif len(result) == 1:
        if readonly:
            view.basic(result[0])
            session.close()
            return
        return result[0]
    else:
        view.basic(message="No match")
        if readonly:
            return False
        return


def read_event_by_attendee(session, readonly=True, **kwargs):
    choice = view.user_input(detail="over/equal/under, amount")
    choice = choice.split(",")
    if "over" in choice:
        stmt = select(Event).where(Event.number_attendee >= int(choice[1]))
    elif "equal" in choice:
        stmt = select(Event).where(Event.number_attendee == int(choice[1]))
    elif "under" in choice:
        stmt = select(Event).where(Event.number_attendee <= int(choice[1]))
    else:
        view.error_input()
        return read_event_by_attendee(session, readonly, **kwargs)

    result = session.scalars(stmt).all()
    if len(result) < 1:
        view.basic(message="No match!")
        return
    else:
        if len(result) > 1:
            if readonly:
                view.basic_list(result)
                session.close()
                return
            else:
                return result
        else:
            if readonly:
                view.basic(result[0])
                session.close()
                return
            else:
                return result[0]


def read_event_in_charge(session, readonly=True, user=None, **kwargs):
    stmt = select(Event).where(Event.support.id == user.id)
    result = session.execute(stmt).all()
    if len(result) > 1:
        if readonly:
            view.basic_list(result)
            session.close()
            return
        return result
    elif len(result) == 1:
        if readonly:
            view.basic(result[0])
            session.close()
            return
        return result[0]
    else:
        view.basic(message="no match")
        session.close()
        return


def create_event(session, readonly=False, user=None, **kwargs):
    values = {
        "contract_id": None,
        "date_begin": None,
        "date_end": None,
        "attendee": None,
        "support_id": None,
        "note": None,
        "address": None,
    }
    for k in values.keys():
        if k == "contract_id":
            if user.role_id == 3:
                contracts = actions_contracts.read_contract_in_charge(
                    session, readonly=False, user=user, **kwargs
                )
            else:
                view.basic(message="Select client then contract to attach the event")
                contracts = actions_contracts.read_contract_by_client_name(
                    session, readonly=False
                )
            contract = view.select_obj_from_list(contracts)
            values[k] = contract.id
        elif k == "date_begin":
            date = view.user_input("start day: YYYY,MMM,DD")
            date = [int(x) for x in date.split(",")]
            input_date = datetime.date(date[0], date[1], date[2])
            values[k] = input_date
        elif k == "date_end":
            date = view.user_input("end day: YYYY,MMM,DD")
            date = [int(x) for x in date.split(",")]
            input_date = datetime.date(date[0], date[1], date[2])
            values[k] = input_date
        elif k == "support_id":
            view.basic(message="select support in charge")
            support = actions_users.read_user_by_name(session, readonly=False)
            if type(support) is list:
                support = view.select_obj_from_list(support)
            values[k] = support.id
        elif k == "attendee":
            attendee = view.user_input("number of attendees")
            values[k] = int(attendee)
        else:
            val = view.user_input(detail=k)
            values[k] = val
    print("bb", values)
    stmt = insert(Event).values(values)
    try:
        session.execute(stmt)
        session.commit()
        capture_message(
            f"user: {user.id} {user.name} {user.email} created Event {values}"
        )
        view.success(message="event created")
    except CompileError as er:
        view.error_message(er)
        session.rollback()
    finally:
        session.close()
        return


def update_event(session, readonly=True, user=None, **kwargs):
    events = read_event(session, readonly=False, **kwargs)
    if events:
        selected_event = view.select_obj_from_list(events)
        view.basic(selected_event)
        values = ask_values()
        stmt = update(Event).where(Event.id == selected_event.id).values(values)
        try:
            session.execute(stmt)
            session.commit()
            view.basic(message="update successful")
            capture_message(
                f"user: {user.id} {user.name} {user.email} deleted {selected_event}"
            )
        except CompileError as er:
            view.error_message(er)
            session.rollback()
        finally:
            session.close()
            return
    else:
        return


def update_event_in_charge(session, readonly=False, user=None, **kwargs):
    events = read_event_in_charge(session, readonly, user=user, **kwargs)
    if events:
        selected_event = view.select_obj_from_list(events)
        view.basic(selected_event)
        values = ask_values()
        stmt = update(Event).where(Event.id == selected_event.id).values(values)
        try:
            session.execute(stmt)
            session.commit()
            view.basic(message="update successful")
            capture_message(
                f"user: {user.id} {user.name} {user.email} updated {selected_event.id} with {values}"
            )
        except CompileError as er:
            view.error_message(er)
            session.rollback()
        finally:
            session.close()
            return
    return


def delete_event(session, readonly=True, user=None, **kwargs):
    events = read_event(session, readonly, **kwargs)
    if events:
        selected_event = view.select_obj_from_list(events)
        stmt = delete(Event).where(Event.id == selected_event.id)
        try:
            session.execute(stmt)
            session.commit()
            view.basic(message="update successful")
            capture_message(
                f"user: {user.id} {user.name} {user.email} deleted {selected_event.id} {selected_event}"
            )
        except:
            view.error_message()
            session.rollback()
            return
        finally:
            session.close()
            return
    else:
        return
