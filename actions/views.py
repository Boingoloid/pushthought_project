# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import json

from django.http import JsonResponse

from congress.models import Congress
from actions.models import Action

from pushthought.views.views_email_congress import submit_congress_email


def submit_congress_email_view(request):
    print "submit_congress_email_view firing"
    # send_response_object = submit_congress_email(request)
    # status = send_response_object['status']
    data = json.loads(request.body)
    congress = Congress.objects.get(bioguide_id=data['bio_id'])
    send_response_object = {'success': True}
    status = 'success'
    data_dict = dict(
        congress=congress
    )

    if data.get('program_id'):
        data_dict['program_id'] = data.get('program_id')

    if request.user.is_authenticated():
        data_dict['user_id'] = request.user.pk

    if send_response_object:
        if status == 'success':
            print "email was sent"
            request.session['last_message'] = data['fields']['$MESSAGE']
            Action.emails.create(
                data['fields']['$MESSAGE'],
                data['fields'],
                **data_dict
            )
        elif status == 'captcha_needed':
            # save email, needs captcha to true, then exclude them.  or save to different table
            print "captcha_needed"
        elif status == 'error':
            print "ERROR submit congress failed: error message returned:" + send_response_object['message']
        return JsonResponse(send_response_object)
    else:
        print "ERROR: submit congress failed, no object returned from phantom congress"
        return JsonResponse({"status": "error", "message": "timeout, no response from phantom congress"})