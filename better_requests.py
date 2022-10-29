import requests
from requests.adapters import HTTPAdapter
from urllib3 import Retry
    
def better_session(retries: int=4, headers: dict = None) -> requests.sessions.Session:
    session = requests.Session()
    if headers:
        session.headers.update(headers)
    adapter = HTTPAdapter(max_retries=Retry(total=retries, backoff_factor=1, allowed_methods=None, status_forcelist=[429, 500, 502, 503, 504]))
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    return session

def cmf_session():
    user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 Edg/107.0.1418.24'
    session = better_session(headers={'referer':'https://www.cmfchile.cl/', 'User-Agent':user_agent})
    return session


session = cmf_session()
r = session.get('http://www.cmfchile.cl/institucional/inc/deposito_fondos_mutuos.php')
print (r)