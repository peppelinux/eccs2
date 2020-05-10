import json
import urllib

from authn_request import Saml2SPAuthnReq


TEST_SP = [{'url': 'https://sp24-test.garr.it/secure',
            'qt': 'https://sp24-test.garr.it/Shibboleth.sso/Login?SAMLDS=1&target=ss%3Amem%3A21e885dd9223f734c8acd85f6871a7097e82fbb8a2c1ef63829e2a5470c71059&entityID={}'},
           {'url': 'https://attribute-viewer.aai.switch.ch/eds/',
            'qt': ''}]

# https://technical.edugain.org/api.php?action=list_eccs_idps
idps = json.loads(open('edugain_idps.json').read())


class Dict2obj:
    def __init__(self, sp_dict):
        for k,v in sp_dict.items():
            setattr(self, k, v)

def test_idp(sp, idp_eid):
    ua = Saml2SPAuthnReq(wayf=1, verify=0, debug=1, timeout=5)
    eid = urllib.parse.quote_plus(idp_eid)
    qt = sp.qt.format(eid) 
    target = '{}?{}'.format(sp.url, qt)
    result = ua.saml_request(target=target)

sp = Dict2obj(TEST_SP[0])
res = test_idp(sp, idps[0]['entityID'])
