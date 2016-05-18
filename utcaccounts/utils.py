import json
import urllib2
from xml.etree import ElementTree

from django.contrib.auth import get_user_model

from constance import config as live_config

from picsous import settings as app_settings
from core.services import payutc
from settings import UTC_CAS_URL


class CASException(Exception):

    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message


class GingerException(Exception):

    def __init__(self, code, message):
        self.message = message
        self.code = code

    def __str__(self):
        return 'Ginger Exception (' + self.code + ') : ' + self.message


def get_ginger_info(login):
    response = urllib2.urlopen(live_config.GINGER_URL + login + '?key=' + live_config.GINGER_KEY)
    if response.getcode() != 200:
        raise GingerException(response.getcode(), response.read())
    return json.loads(response.read())


def nemopay_connection_active(request):
    cli = payutc.Client(param_session_id=request.COOKIES.get('nemopay_sessionid'))
    status = cli.call(app_settings.NEMOPAY_LOGIN_SERVICE, 'getStatus')
    if status['user'] is None:
        return False
    else:
        return True


def get_nemopay_info(ticket, service):
    conn = payutc.Client()
    return conn.loginCas(ticket, service)


class CASTicket:

    def __init__(self, uri, ticket):
        self.uri = uri
        self.ticket = str(ticket)
        if self.ticket is None or self.ticket == '':
            raise CASException('Empty ticket')

    def get_server_information(self):
        response = urllib2.urlopen(UTC_CAS_URL + 'serviceValidate?service=' + self.uri + '&ticket=' + self.ticket)
        return response.read()

    def parse_login(self, xml_info):
        serviceResponseNode = ElementTree.fromstring(xml_info)
        authentificationNode = serviceResponseNode.getchildren()[0]
        userNode = authentificationNode.getchildren()[0]
        return userNode.text

    def get_information(self):
        if app_settings.NEMOPAY_LOGIN_ACTIVATED:
            return get_nemopay_info(self.ticket, self.uri)
        else:
            xml_info = self.get_server_information()
            return (self.parse_login(xml_info), None)

def user_creation(login):
    ginger_answer = get_ginger_info(login)
    first_name = ginger_answer['prenom']
    last_name = ginger_answer['nom']
    email = ginger_answer['mail']
    user = get_user_model().objects.create(username=login, password=login, email=email, first_name=first_name,
                                           last_name=last_name)
    user.save()
    return get_user_model().objects.get(pk=user.pk)
