# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import json
import logging
from pprint import pformat

from django.http import HttpResponse, JsonResponse
from django.conf import settings
from django.views.generic import View

import requests

from congress.models import Congress
from actions.models import Action

from pushthought.views.views_email_congress import submit_congress_email


logger = logging.getLogger('congress_email')


def submit_congress_email_view(request):
    print "submit_congress_email_view firing"
    # send_response_object = submit_congress_email(request)
    # status = send_response_object['status']
    data = json.loads(request.body)
    congresses = Congress.objects.filter(bioguide_id__in=data['bio_ids'])
    send_response_object = {'success': True}
    status = 'success'
    data_dict = dict(
        congresses=congresses
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


class SubmitCongressEmail(View):
    """View for sending messages via Phantom DC."""

    def get_fields_for_bioguides(self, bioguides):
        """Return list of required fields for each bioguide.

        Args:
            bioguides: list of bioguides.

        Returns:
            Dict with bioguide as keys and list of names of required
            fields as values.
        """
        # TODO Make sure Phantom DC ignores spare fields and get rid of
        # requests to `settings.PHANTOM_DC_API_RETRIEVE_FORM_ELEMENTS`.
        response = requests.post(
            settings.PHANTOM_DC_API_BASE +
            settings.PHANTOM_DC_API_RETRIEVE_FORM_ELEMENTS,
            data=json.dumps({'bio_ids': bioguides}),
            headers={'content-type': 'application/json'})
        forms = {}
        for bioguide, form in json.loads(response.text).items():
            forms[bioguide] = [a['value'] for a in form['required_actions']]
        return forms

    def get_filled_out_fields(self, bioguide, field_names, data):
        """Fill out requested fields from the dict of all fields.

        Args:
            bioguide: bioguide of member for whom `field_names` are
                being filled.
            field_names: list of names of fields to fill.
            data: dict of all received fields and their values.
        Returns:
            Dict of only requested fields with data. As a rule isn't a
            subdict of `data`, as field "$TOPIC" and some others are
            named in `data` like "$TOPIC_`bioguide`".
        Raises:
            KeyError: Specified field not found in data.
        """
        fields = {}
        for field_name in field_names:
            field_value = data.get(
                field_name, data.get("{}_{}".format(field_name, bioguide)))
            if field_value is not None:
                fields[field_name] = field_value
            else:
                raise KeyError(field_name)
        return fields

    def send_message_via_phantom_dc(self, bioguide, filled_out_fields):
        """Request Phantom DC to send message to a member.

        Args:
            bioguide: bioguide identifying the member to send the
                message to.
            filled_out_fields: dict of fields with data to be used to
                fill out the message form.
        Returns:
            Boolean indicating whether Phantom DC reported a successful
            sending.
        """
        response = requests.post(
            settings.PHANTOM_DC_API_BASE +
            settings.PHANTOM_DC_API_FILL_OUT_FORM,
            data=json.dumps({'bio_id': bioguide, 'fields': filled_out_fields}),
            headers={'content-type': 'application/json'})
        logger.debug(
            "Message sending to {} status: {}\nMessage was: {}".format(
                bioguide, pformat(json.loads(response.text)),
                pformat(filled_out_fields)))
        return json.loads(response.text)['status'] == 'success'

    def post(self, request):
        """Send message via Phantom DC to each requested member.

        Args:
            request: django.http.HttpRequest. As payload should have
                JSON dictionary with items:
                `bio_id` - list of bioguides messages should be sent to.
                `fields` - dictionary of field names (in format
                    `$FIELD_NAME_bioguide` if the field can be repeated
                    for some mebers) and user-provided values for them.
        Returns:
            Empty instance of `HttpResponse`.
        """
        request_body = json.loads(request.body)
        logger.debug("SubmitCongressEmail POST request body:\n{}".format(
            pformat(request_body)))
        # TODO Potentially insecure. Process with Django Forms.
        bioguides = request_body['bio_ids']
        data = request_body['fields']
        for bioguide, field_names in self.get_fields_for_bioguides(
                bioguides).items():
            filled_out_fields = self.get_filled_out_fields(bioguide,
                                                           field_names, data)
            self.send_message_via_phantom_dc(bioguide, filled_out_fields)
        request.session['last_message'] = filled_out_fields['$MESSAGE']
        return HttpResponse()
