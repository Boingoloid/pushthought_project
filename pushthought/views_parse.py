import json,httplib, urllib
from django.contrib import messages

PARSE_APP_ID = 'lzb0o0wZHxbgyIHSyZLlooijAK9afoyN8RV4XwcM'
PARSE_REST_KEY = 'YTeYDL8DeSDNsmZT219Lp8iXgPZ24ZGu3ywUjo23'

def create_user(request):
    print "Create user method"
    print request.POST
    user_email = request.POST['user_email']
    user_password = request.POST['password']

    connection = httplib.HTTPSConnection('ptparse.herokuapp.com', 443)
    connection.connect()
    connection.request('POST', '/parse/classes/_User', json.dumps({
           "username": user_email,
           "password": user_password
         }), {
           "X-Parse-Application-Id": PARSE_APP_ID,
           "X-Parse-REST-API-Key": PARSE_REST_KEY,
           "X-Parse-Revocable-Session": "1",
           "Content-Type": "application/json"
         })
    result = json.loads(connection.getresponse().read())

    print "print callback value for user creation."
    print result

    return result

def login_user(request):
    print "login user method"
    print request.POST
    user_name = request.POST['user_email']
    password = request.POST['password']
    connection = httplib.HTTPSConnection('ptparse.herokuapp.com', 443)
    params = urllib.urlencode({"username":user_name,"password": password})
    connection.connect()
    connection.request('GET', '/parse/login?%s' % params, '', {
           "X-Parse-Application-Id": PARSE_APP_ID,
           "X-Parse-REST-API-Key": PARSE_REST_KEY,
           "X-Parse-Revocable-Session": "1"
         })
    result = json.loads(connection.getresponse().read())
    print "printing result of login:"
    print result

    return result