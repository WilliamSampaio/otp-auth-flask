from tinydb import TinyDB


def get_db_instance() -> TinyDB:
    return TinyDB('db.json')


def get_users_tbl() -> TinyDB:
    db = get_db_instance()
    db.default_table_name = 'users'
    return db
