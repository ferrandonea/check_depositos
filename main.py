from datetime import datetime

from bs4 import BeautifulSoup

from better_requests import cmf_session
from dbmodel import orm, db, Deposit, query_datos

def str_to_datetime(input:str) -> datetime:
    format = "%d/%m/%Y"
    return datetime.strptime(input, format)

def get_depositos():
    # baja toda la información de una
    # es un pelo más lento pero esto se corre poco
    url = "https://www.cmfchile.cl/institucional/inc/deposito_fondos_mutuos.php"
    session = cmf_session()
    r = session.get(url)
    soup = BeautifulSoup(r.content, "html.parser")

    # no encontré que lograra con los selectores, esto funciona
    rows = soup.find_all("table")[1].find_all("tr")

    list_data = list()
    for row in rows:
        data = {}
        columns = row.find_all("td")
        try:
            #es mas legible sin un for, aunque es bien repetido esto
            data["register"] = columns[0].text.strip()
            data["deposit_time"] = str_to_datetime(columns[1].text.strip())
            data["fund_run"] = columns[2].text.strip()
            data["fund_name"] = columns[3].text.strip()
            data["fund_manager"] = columns[4].text.strip()
            data["last_modification"] = str_to_datetime(columns[5].text.strip())
        except IndexError as e:
            # los headers fallan, que fallen silenciosamente
            # esto puede generar problemas, pero no creo
            pass
        list_data.append(data)
    return list_data

def add_data_db(data:dict) -> None:
    #agrega una linea de datos de la lista
    with orm.db_session():
        NewDeposit = Deposit(**data)
 
def check_new_data() -> None:
    lista_datos = get_depositos()
    for dato in reversed([x for x in lista_datos if x]):
        try:
            add_data_db(dato)
            print ("NEW DATA")
            print ("========")
            print (dict(dato))
            
        except orm.core.TransactionIntegrityError as e:
            #esto si existe
            pass
    
if __name__ == "__main__":
    check_new_data()
    
    
    
    #for datos in lista_datos:
    #    print (len(datos))
    