from views_parse_user import *
from django.shortcuts import get_list_or_404, get_object_or_404, render

def user_signin_form(request):

    print "form request"
    print "currentUser"

    if request.method == 'POST':
        current_user = create_user(request)
        try:
            code = current_user['code']
            if current_user['code'] == 202:
                # User already exists, guide to login
                messages.info(request, 'Account already exists for this username.  Try logging in.')
                return render(request, 'user_signin_form.html')
        except:
            # User created, take to account_home
            messages.info(request, 'Success - you now have an account.')
            user_objectId = current_user['objectId']
            request.session['sessionToken'] = current_user['sessionToken']
            print "session token:" + request.session['sessionToken']
            account_home = "/account/" + user_objectId
            return HttpResponseRedirect(account_home)

            # return render(request, 'account_home.html',{'user_pk':current_user['objectId']})
    else:
        # Get request, send blank page
        return render(request, 'user_signin_form.html')


def login_form(request):

    print "login form request"

    if request.method == 'POST':
        current_user = login_user(request)
        try:
            code = current_user['code']
            if current_user['code'] == 101:
                messages.info(request, 'Invalid username/password')
                # User not found w email
                return render(request, 'login_form.html')
        except:
            # User created, take to account_home
            messages.info(request, 'Success: Logged In')
            user_objectId = current_user['objectId']
            request.session['sessionToken'] = current_user['sessionToken']
            print "session token:" + request.session['sessionToken']
            account_home = "http://127.0.0.1:8000/account/" + user_objectId
            return HttpResponseRedirect(account_home)

            # return render(request, 'account_home.html',{'user_pk':current_user['objectId']})
    else:
        # Get request, send blank page
        return render(request, 'login_form.html')