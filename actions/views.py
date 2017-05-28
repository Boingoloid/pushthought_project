# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import json

from django.http import JsonResponse

from congress.models import Fields, Congress
from actions.models import Action

from pushthought.views.views_email_congress import submit_congress_email


def submit_congress_email_view(request):
    print "submit_congress_email_view firing"
    send_response_object = submit_congress_email(request)
    status = send_response_object['status']
    data = json.loads(request.body)
    congress = Congress.objects.get(bioguide_id=data['bio_id'])
    if send_response_object:
        if status == 'success':
            print "email was sent"
            Action.emails.create(
                data['fields']['$MESSAGE'],
                request.body,
                user=request.user,
                program_id=data['program_id'],
                congress=congress
            )
        elif status == 'captcha_needed':
            # save email, needs captcha to true, then exclude them.  or save to different table
            print "captcha_needed"
            Fields.objects.update_or_create(congress=congress, defaults={'fields': request.body})
        elif status == 'error':
            print "ERROR submit congress failed: error message returned:" + send_response_object['message']
        return JsonResponse(send_response_object)
    else:
        print "ERROR: submit congress failed, no object returned from phantom congress"
        return JsonResponse({"status": "error", "message": "timeout, no response from phantom congress"})