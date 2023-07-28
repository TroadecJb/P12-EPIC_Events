import sqlite3
from sqlite3 import Error


def create_connection(db_file):
    """create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)

    return conn


def create_table(conn, create_table_sql):
    """create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)


def main():
    database = r"./epic_events.db"

    sql_create_users_table = """ CREATE TABLE IF NOT EXISTS users (
                                    id INTEGER PRIMARY KEY NOT NULL,
                                    name TEXT NOT NULL,
                                    email TEXT NOT NULL,
                                    password TEXT NOT NULL,
                                    role_id INTEGER NOT NULL,
                                    FOREIGN KEY (role_id) REFERENCES roles (id)
                                ); """

    sql_create_roles_table = """ CREATE TABLE IF NOT EXISTS roles (
                                        id INTEGER PRIMARY KEY NOT NULL,
                                        role TEXT NOT NULL
                                    ); """

    sql_create_clients_table = """ CREATE TABLE IF NOT EXISTS clients (
                                        id INTEGER PRIMARY KEY NOT NULL,
                                        name TEXT NOT NULL,
                                        email TEXT NOT NULL,
                                        phone TEXT NOT NULL,
                                        first_contact DATE NOT NULL,
                                        last_contact DATE NOT NULL,
                                        company_id INTEGER NOT NULL,
                                        commercial_id INTEGER NOT NULL,
                                        FOREIGN KEY (company_id) REFERENCES companies (id) ,                                       
                                        FOREIGN KEY (commercial_id) REFERENCES users (id)
                                    ); """

    sql_create_companies_table = """ CREATE TABLE IF NOT EXISTS companies (
                                        id INTEGER PRIMARY KEY NOT NULL,
                                        name TEXT NOT NULL,
                                        address_id INTEGER NOT NULL,
                                        FOREIGN KEY (address_id) REFERENCES addresses (id)
                                        ); """

    sql_create_contracts_table = """ CREATE TABLE IF NOT EXISTS contracts (
                                        id INTEGER PRIMARY KEY NOT NULL,
                                        client_id INTEGER NOT NULL,
                                        date_creation DATE NOT NULL,
                                        cost_total FLOAT NOT NULL,
                                        cost_reaining FLOAT NOT NULL,
                                        valid BOOLEAN NOT NULL,
                                        commercial_id INTEGER,
                                        FOREIGN KEY (client_id) REFERENCES clients (id),
                                        FOREIGN KEY (commercial_id) REFERENCES users (id)
                                        ); """

    sql_create_events_table = """ CREATE TABLE IF NOT EXISTS events (
                                    id INTEGER PRIMARY KEY NOT NULL,
                                    contract_id INTEGER NOT NULL,
                                    support_id INTEGER,
                                    date_begin DATE NOT NULL,
                                    date_end DATE NOT NULL,
                                    address_id INTEGER NOT NULL,
                                    number_attendee INTEGER,
                                    note TEXT,
                                    FOREIGN KEY (support_id) REFERENCES users (id),
                                    FOREIGN KEY (contract_id) REFERENCES contracts (id),
                                    FOREIGN KEY (address_id) REFERENCES addresses (id)
                                    ); """

    sql_create_addresses_table = """ CREATE TABLE IF NOT EXISTS addresses (
                                    id INTEGER PRIMARY KEY NOT NULL,
                                    number INTEGER,
                                    street TEXT,
                                    city TEXT NOT NULL,
                                    code INTEGER NOT NULL,
                                    additonnal_info TEXT
                                    ); """

    conn = create_connection(database)

    if conn is not None:
        create_table(conn, sql_create_users_table)
        create_table(conn, sql_create_roles_table)
        create_table(conn, sql_create_clients_table)
        create_table(conn, sql_create_companies_table)
        create_table(conn, sql_create_contracts_table)
        create_table(conn, sql_create_events_table)
        create_table(conn, sql_create_addresses_table)

    else:
        print("Error! Cannot create the database connection.")


if __name__ == "__main__":
    main()
