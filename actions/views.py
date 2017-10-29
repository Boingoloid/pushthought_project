# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import json
import logging
from pprint import pformat

from django.http import JsonResponse
from django.conf import settings
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin

import requests
from el_pagination.views import AjaxListView

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

    NAME_PLACEHOLDER = '[name will be inserted]'

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

    def get_filled_out_fields(self, bioguide, data):

        """Fill out requested fields from the dict of all fields.

        Args:
            bioguide: bioguide of member for whom `field_names` are
                being filled.
            data: dict of all received fields and their values.
        Returns:
            Dict of all available fields with data. It isn't supposed to
            be a subdict of `data`, as field "$TOPIC" and some others
            are named in `data` like "$TOPIC_`bioguide`".
        """
        fields = {}
        for k, v in data.items():
            bioguide_suffix = "_{}".format(bioguide)
            if k.endswith(bioguide_suffix):
                fields[k[:-len(bioguide_suffix)]] = v
            else:
                fields[k] = v
        return fields

    def preprocess_fields(self, bioguide, filled_out_fields):
        """Change values of fields.

        Currently replaces all occurences of value of `NAME_PLACEHOLDER`
        in field `$MESSAGE` with full name of a Congress member with the
        provided `bioguide`.

        Args:
            `bioguide`: int, bioguide of the member for whom
                `filled_out_fields` are filled.
            `filled_out_fields`: dict, field names and values.
        Returns:
            dict, modified field names and values.
        """
        fields = dict(filled_out_fields)
        if self.NAME_PLACEHOLDER in fields['$MESSAGE']:
            fields['$MESSAGE'] = fields['$MESSAGE'].replace(
                self.NAME_PLACEHOLDER,
                Congress.objects.get(bioguide_id=bioguide).full_name)
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
        filled_out_fields = self.preprocess_fields(bioguide, filled_out_fields)
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

    def save_email(self, bioguide, fields, is_sent):
        """Save e-mail data to DB as `Action` and it's related objects.

        Args:
            bioguide: bioguide identifying the member to send the
                message to.
            fields: dict of fields with data used to fill out the
                message form.
            is_sent: boolean indicating if the message was sent.
        """
        congress = Congress.objects.get(bioguide_id=bioguide)
        Action.emails.create(text=fields['$MESSAGE'], fields=fields,
                             is_sent=is_sent, congress=congress)

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
            Instance of `JsonResponse` with `{'status': 'success'}`.
            If code was executed, it's considered to be a successful
            send, an e-mails either were sent automatically, or will be
            sent manually later.
        """
        request_body = json.loads(request.body)
        logger.debug("SubmitCongressEmail POST request body:\n{}".format(
            pformat(request_body)))
        # TODO Potentially insecure. Process with Django Forms.
        bioguides = request_body['bio_ids']
        data = request_body['fields']
        for bioguide in bioguides:
            filled_out_fields = self.get_filled_out_fields(bioguide, data)
            is_send_successful = self.send_message_via_phantom_dc(
                bioguide, filled_out_fields)
            self.save_email(bioguide, filled_out_fields, is_send_successful)
        return JsonResponse({'status': 'success'})


class MyActivityView(LoginRequiredMixin, AjaxListView):
    """Show list of past user activities.

    Renders only list elements on AJAX request use tu use of
    `el_pagination`'s AjaxListView.

    Template name for non-AJAX is the default:
    `actions/action_list.html`. Template name for AJAX is the default:
    `actions/action_list_page.html`.
    """

    def get_queryset(self):
        """Return actions of requesting user, newest first."""
        return Action.objects.filter(user=self.request.user).order_by(
            '-created')

    def get_context_data(self, **kwargs):
        """Add total counts of emails and tweets sent by this user."""
        context = super(MyActivityView, self).get_context_data(**kwargs)
        queryset = self.get_queryset()
        context['email_count'] = queryset.filter(email__isnull=False).count()
        context['tweet_count'] = queryset.filter(tweet__isnull=False).count()
        return context
