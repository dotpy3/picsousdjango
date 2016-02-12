import json
import requests

from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import User

from picsous.settings import NEMOPAY_API_URL, NEMOPAY_SYSTEM_ID, NEMOPAY_API_KEY, NEMOPAY_LOGIN_SERVICE,\
    NEMOPAY_CONNECTION_UID, NEMOPAY_CONNECTION_PIN

class NemopayClientException(Exception):
    pass

class Client:

    def __init__(self, param_session_id=None):
        self.SESSION_ID = param_session_id

    SESSION_ID = None

    app_login = False
    user_login = False

    def logged(self):
        return {
            'user': self.user_login,
            'app': self.app_login,
        }

    def loginCas(self, ticket, service):
        url = self._call_url(NEMOPAY_LOGIN_SERVICE, 'loginCas') + '?system_id=' + NEMOPAY_SYSTEM_ID
        r = requests.post(url, data={ 'ticket': ticket, 'service': service })
        sessionid = r.cookies.get('sessionid')
        return (str(r.text.strip('"')), sessionid)

    def loginApp(self, service=NEMOPAY_LOGIN_SERVICE):
        self.SESSION_ID = str(self.call(service, 'loginApp', key=NEMOPAY_API_KEY)['sessionid'])
        return self.SESSION_ID

    def loginBadge(self, badge_id=NEMOPAY_CONNECTION_UID, pin=NEMOPAY_CONNECTION_PIN):
        self.SESSION_ID = str(self.call('POSS3', 'loginBadge2', badge_id=badge_id, pin=pin)['sessionid'])
        return self.SESSION_ID

    def _call_url(self, service, method):
        return NEMOPAY_API_URL + service + '/' + method

    def call(self, service, method, params=None, **data):
        if params is None:
            params = { 'system_id': NEMOPAY_SYSTEM_ID }
        if self.SESSION_ID is not None:
            params['sessionid'] = self.SESSION_ID
        r = requests.post(self._call_url(service, method), params=params, data=data)
        if r.status_code != 200:
            raise NemopayClientException(r.text)
        return json.loads(r.text)


class PayUTCAuthBackend(ModelBackend):
    """Login to Django using just the user login
    """
    def authenticate(self, username=None):
        try:
            return User.objects.get(username=username)
        except User.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
