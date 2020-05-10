import json
import urllib

from authn_request import Saml2SPAuthnReq
from multiprocessing import Pool


class Dict2obj:
    def __init__(self, sp_dict):
        for k,v in sp_dict.items():
            setattr(self, k, v)


CHECK_CERT = True
WORKERS = 30
TEST_SP = [{'url': 'https://sp24-test.garr.it/Shibboleth.sso/Login',
            'qt': 'entityID={}'},
           #{'url': 'https://attribute-viewer.aai.switch.ch/Shibboleth.sso/Login',
            #'qt': 'entityID={}'}
            ]
TEST_SP_OBJ = [Dict2obj(i) for i in TEST_SP]
LOG_FILE = open('./log.json', 'w')

# https://technical.edugain.org/api.php?action=list_eccs_idps
idps = json.loads(open('edugain_idps.json').read())


def test_idp(idp):
    test = None
    eid = idp['entityID']
    LOG_FILE.write('Testing: {}'.format(eid))
    for sp in TEST_SP_OBJ:
        ua = Saml2SPAuthnReq(wayf=1, verify=CHECK_CERT, debug=0, timeout=5)
        eid = urllib.parse.quote_plus(eid)
        qt = sp.qt.format(eid) 
        target = '{}?{}'.format(sp.url, qt)
        try:
            result = ua.saml_request(target=target)
            test = test_login_form(result)
        except Exception as e:
            test = False
            LOG_FILE.write(', {}, '.format(e))
        if not test:
                LOG_FILE.write(', Failed\n')
                LOG_FILE.flush()
                return
    if test:
        LOG_FILE.write(', OK\n')
        LOG_FILE.flush()

def test_login_form(html_page):
    presences = ('form', 'username', 'password')
    for i in presences:
        if i not in html_page:
            return
    return True


def serial():
    for i in idps[:]:
        res = test_idp(i)
            
    
def parallel():
    with Pool(WORKERS) as p:
        p.map(test_idp, idps)

if __name__ == '__main__':
    parallel()
    #serial()
