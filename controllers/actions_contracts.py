import datetime
from sqlalchemy import select, update, delete, insert
from sqlalchemy.exc import InvalidRequestError, CompileError
from models.tables import User, Client, Contract, Event  # , Company, Address

from views.display import View
from controllers.actions_utils import ask_values
from controllers import actions_clients, actions_users

view = View()


def read_contract(session, readonly=True, **kwargs):
    """
    User can filter the contracts by Date, Cost_total, Cost_Remaining, Commercial, Client, Status or All
    """
    filtering_options = {
        "all": read_contracts_all,
        "client": read_contract_by_client_name,
        "commercial": read_contract_by_commerical_name,
        "date": read_contract_by_date,
        "cost": read_contract_by_cost,
        "status": read_contract_by_status,
    }
    view.basic(message="select the field to search for the contract")
    view.dict_k(filtering_options)
    choice = view.user_input()
    if choice in filtering_options.keys():
        return filtering_options[choice](session, readonly, **kwargs)
    else:
        view.error_input()
        return read_contract(session, readonly=readonly, **kwargs)


def read_contracts_all(session, readonly=True, **kwargs):
    """
    User can choose between all contracts or by client's name associated.
    If readonly=False return either list of obj or signle obj.
    """
    result = session.scalars(select(Contract)).all()
    if readonly:
        view.basic_list(result)
        session.close()
        return
    else:
        return result


def read_contract_by_client_name(session, readonly=True, **kwargs):
    """
    User can search by complete or parital client's name.
    If readonly=False return either list of obj or single obj
    """
    client_name = view.user_input(detail="client's name")
    stmt = select(Contract).join(Client).where(Client.name.contains(client_name))
    result = session.scalars(stmt).all()

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


def read_contract_by_commerical_name(session, readonly=True, **kwargs):
    """
    User can search by complete or parital client's name.
    If readonly=False return either list of obj or single obj
    """
    commercial_name = view.user_input(detail="commercial's name")
    stmt = select(Contract).join(User).where(User.name.contains(commercial_name))
    result = session.execute(stmt).all()
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


def read_contract_by_status(session, readonly=True, **kwargs):
    """
    User can filter the contracts by their valid status.
    if readonly=False return either list of obj or signe obj.
    """
    status = view.user_input(detail="signed?")
    if status in ["y", "ye", "yes"]:
        status = True
    else:
        status = False
    stmt = select(Contract).where(Contract.valid == status)
    result = session.execute(stmt).all()

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


def read_contract_by_date(session, readonly=True, **kwargs):
    specific_date = view.user_input(detail="specific date?")
    if specific_date in ["y", "yes", "yes"]:
        date = view.user_input("YYYY,MM,DD")
        date = [int(x) for x in date.split(",")]
        date = datetime.date(date[0], date[1], date[2])
        stmt = select(Contract).where(Contract.date_creation == date)
        result = session.scalars(stmt).all()
    else:
        stmt = select(Contract).order_by(Contract.date_creation)
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


def read_contract_by_cost(session, readonly=True, **kwargs):
    field = view.user_input(detail="total or remaining")
    choice = view.user_input(detail="over/equal/under, amount")
    choice = choice.split(",")
    if field == "total":
        if "over" in choice:
            stmt = select(Contract).where(Contract.cost_total >= float(choice[1]))
        elif "equal" in choice:
            stmt = select(Contract).where(Contract.cost_total == float(choice[1]))
        else:
            stmt = select(Contract).where(Contract.cost_total <= float(choice[1]))
    elif field == "reamining":
        if "over" in choice:
            stmt = select(Contract).where(Contract.cost_remaining >= float(choice[1]))
        elif "equal" in choice:
            stmt = select(Contract).where(Contract.cost_remaining == float(choice[1]))
        else:
            stmt = select(Contract).where(Contract.cost_remaining <= float(choice[1]))
    else:
        view.error_input()
        return read_contract_by_cost(session, readonly, **kwargs)

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


def read_contract_in_charge(session, readonly=True, user=None, **kwargs):
    stmt = select(Contract).where(Contract.commercial.id == user.id)
    result = session.execute(stmt).all()
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


def update_contract(session, readonly=False, user=None, **kwargs):
    if user.role_id == 3:
        contracts = read_contract_in_charge(
            session, readonly=False, user=user, **kwargs
        )
    else:
        contracts = read_contract(session, readonly, **kwargs)
    selected_contract = None
    if type(contracts) is list:
        selected_contract = view.select_obj_from_list(contracts)
    else:
        selected_contract = contracts
    view.basic(selected_contract)
    values = ask_values()
    stmt = update(Contract).where(Contract.id == selected_contract.id).values(values)
    try:
        session.execute(stmt)
        session.commit()
        view.basic(message="update successful")
    except CompileError as er:
        view.error_message(er)
        session.rollback()
    finally:
        session.close()
        return


def delete_contract(session, readonly=False, **kwargs):
    contracts = read_contract(session, readonly, **kwargs)
    selected_contract = view.select_obj_from_list(contracts)
    stmt = delete(Contract).where(Contract.id == selected_contract.id)
    session.execute(stmt)
    session.commit()
    session.close()
    return


def create_contract(session, readonly=False, **kwargs):
    values = {
        "client_id": None,
        "date_creation": None,
        "cost_total": None,
        "cost_remaining": None,
        "valid": None,
        "commercial_id": None,
    }

    for k in values.keys():
        if k == "client_id":
            client = actions_clients.read_client_by_name(session, readonly=False)
            if type(client) is list:
                client = view.select_obj_from_list(client)
            values[k] = client.id
        elif k in "date_creation":
            date = view.user_input("YYYY,MM,DD")
            date = [int(x) for x in date.split(",")]
            input_date = datetime.date(date[0], date[1], date[2])
            values[k] = input_date
        elif k in ["cost_total", "cost_remaing"]:
            values[k] = float(view.user_input(detail=k))
        elif k == "valid":
            valid = view.user_input(detail="Signed: True or False").lower()
            choice = {"true": True, "false": False}
            values[k] = choice[valid]
        elif k == "commercial_id":
            commercial = actions_users.read_user_by_name(
                session, readonly=False, user_role="commercial"
            )
            if type(commercial) is list:
                commercial = view.select_obj_from_list(commercial)
            values[k] = commercial.id
        else:
            values[k] = view.user_input(detail=k)
    stmt = insert(Contract).values(values)
    try:
        session.execute(stmt)
        session.commit()
        view.basic(message="contract created")
    except CompileError as er:
        view.error_message(er)
        session.rollback()
    finally:
        session.close()
        return
