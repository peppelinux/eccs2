import json
import urllib

from authn_request import Saml2SPAuthnReq

CHECK_CERT = True

TEST_SP = [{'url': 'https://sp24-test.garr.it/Shibboleth.sso/Login',
            'qt': 'entityID={}'},
           {'url': 'https://attribute-viewer.aai.switch.ch/eds/',
            'qt': ''}]

# https://technical.edugain.org/api.php?action=list_eccs_idps
idps = json.loads(open('edugain_idps.json').read())


class Dict2obj:
    def __init__(self, sp_dict):
        for k,v in sp_dict.items():
            setattr(self, k, v)

def test_idp(sp, idp_eid):
    ua = Saml2SPAuthnReq(wayf=1, verify=True, debug=0, timeout=5)
    eid = urllib.parse.quote_plus(idp_eid)
    qt = sp.qt.format(eid) 
    target = '{}?{}'.format(sp.url, qt)
    result = ua.saml_request(target=target)
    return result


def test_login_form(html_page):
    presences = ('form', 'username', 'password')
    for i in presences:
        if i not in html_page:
            return
    return True


sp = Dict2obj(TEST_SP[0])
for i in idps[:]:
    eid = i['entityID']
    print('Testing: {}'.format(eid), end=', ')
    try:
        res = test_idp(sp, eid)
        if test_login_form(res):
            print('OK')
    except Exception as e:
        print('Failed: {}'.format(e))
