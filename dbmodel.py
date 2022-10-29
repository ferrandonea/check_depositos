from pony import orm
from datetime import datetime

db = orm.Database()

class Deposit(db.Entity):
    register = orm.PrimaryKey(str)
    deposit_time = orm.Required(datetime) 
    fund_run = orm.Required(int)
    fund_name = orm.Required(str)
    fund_manager = orm.Required(str)
    last_modification = orm.Required(datetime)

db.bind(provider='sqlite', filename='database.sqlite', create_db=True)
db.generate_mapping(create_tables=True)

def query_datos(dato):
    with orm.db_session():
        datos = list(orm.select((p for p in Deposit if p.register == dato["register"])))
    return datos