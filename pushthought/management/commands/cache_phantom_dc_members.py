"""Management command for updating local cache of Phantom DC forms.

`Member` refers to member of US government that can be contacted using
forms, data for which is provided by Phantom DC.

"""
import os
import os.path
import io
import itertools
import warnings
import json
from decimal import Decimal
from copy import deepcopy

from django.conf import settings
from django.core.management.base import BaseCommand

import requests


# EFF's API usually responds to the request for all current 607 members
# just fine, and it's sometimes a little bit faster, but just to make
# this command a bit less fragile we'll request by chunks.
DEFAULT_BIOGUIDES_CHUNK_SIZE = 100
YAML_LIST_URL = 'https://api.github.com/repos/unitedstates/' \
    'contact-congress/contents/members?ref=master'
# Note: for 5 forms EFF's API returns lists where values are not
# shortened (two characters), but full names of states. However all
# websites currently have forms with shortened names as option values.
# Bioguides of those forms are B001261, M001170, C000174, M000303,
# F000444.
# Keys of this dict are options' text, and values are options values.
# This is to keep compatibility with the data from Phantom DC.
OVERRIDEN_FIELD_OPTIONS_HASHES = {
    '$ADDRESS_STATE_POSTAL_ABBREV': {
        'Alaska': "AK",
        'Alabama': "AL",
        'Arkansas': "AR",
        'Arizona': "AZ",
        'California': "CA",
        'Colorado': "CO",
        'Connecticut': "CT",
        'District of Columbia': "DC",
        'Delaware': "DE",
        'Florida': "FL",
        'Georgia': "GA",
        'Hawaii': "HI",
        'Iowa': "IA",
        'Idaho': "ID",
        'Illinois': "IL",
        'Indiana': "IN",
        'Kansas': "KS",
        'Kentucky': "KY",
        'Louisiana': "LA",
        'Massachusetts': "MA",
        'Maryland': "MD",
        'Maine': "ME",
        'Michigan': "MI",
        'Minnesota': "MN",
        'Missouri': "MO",
        'Mississippi': "MS",
        'Montana': "MT",
        'North Carolina': "NC",
        'North Dakota': "ND",
        'Nebraska': "NE",
        'New Hampshire': "NH",
        'New Jersey': "NJ",
        'New Mexico': "NM",
        'Nevada': "NV",
        'New York': "NY",
        'Ohio': "OH",
        'Oklahoma': "OK",
        'Oregon': "OR",
        'Pennsylvania': "PA",
        'Rhode Island': "RI",
        'South Carolina': "SC",
        'South Dakota': "SD",
        'Tennessee': "TN",
        'Texas': "TX",
        'Utah': "UT",
        'Virginia': "VA",
        'Vermont': "VT",
        'Washington': "WA",
        'Wisconsin': "WI",
        'West Virginia': "WV",
        'Wyoming': "WY",
    },
    '$NAME_PREFIX': [
        'Mr.',
        'Mrs.',
        'Ms.',
    ],
}


def grouper(n, iterable):
    """Yield tuples with chuncks of `iterable` not longer than `n`.

    Overcomplicated with a hack to prevent encoding problems with
    Unicode characters in case the last chunk will be only one element
    long. Problem is described in the warning in `self.handle`.

    Simple and clean original taken from
    https://stackoverflow.com/a/8991553
    """
    it = iter(iterable)
    next_chunk = None
    get_next_chunk = lambda: tuple(itertools.islice(it, n))
    while True:
        if next_chunk is None:
            next_chunk = get_next_chunk()
        chunk = next_chunk
        next_chunk = get_next_chunk()
        if not chunk:
            return
        # Protect from encoding problem described in the warning in
        # `self.handle`.
        if n != 1 and len(next_chunk) == 1:
            chunk = chunk + next_chunk
            next_chunk = ()
        yield chunk


class Command(BaseCommand):
    """Command for updating local cache of Phantom DC forms."""

    def add_arguments(self, parser):
        """Add optional arguments to the command.

        Arguments are:
            --chunk-size - int, default `DEFAULT_BIOGUIDES_CHUNK_SIZE`.
            --dest - str, path to the cache file that will be written.
            --source - str, URL of Phantom DC API resource for
                retrieveing form elements.
            --no-preprocess - doesn't accept a value, turn off
                preprocessing data from Phantom DC, keeping the data as
                it was.
            --no-minify - doesn't accept a value, turns off production
                minified JSON, and instead produces a pretty-printed
                one.

        Args:
            parser: instance of `argparse.ArgumentParser`.
        """
        parser.add_argument(
            '--chunk-size',
            dest='chunk_size',
            type=int,
            default=DEFAULT_BIOGUIDES_CHUNK_SIZE,
            help='Number of bioguide IDs to query Phantom DC in one request',
        )
        parser.add_argument(
            '--dest',
            dest='dest',
            default=os.path.join(settings.BASE_DIR, 'static', 'js',
                                 'phantom-dc-members.min.json'),
            help='URL of Phantom DC',
        )
        parser.add_argument(
            '--source',
            dest='source',
            default=settings.PHANTOM_DC_API_BASE +
            settings.PHANTOM_DC_API_RETRIEVE_FORM_ELEMENTS,
            help='URL of Phantom DC API\'s resource for retrieving form'
            'elements',
        )
        parser.add_argument(
            '--no-preprocess',
            dest='preprocess',
            action='store_false',
            help='Write non-modified data obtained from the source.',
        )
        parser.add_argument(
            '--no-minify',
            dest='minify',
            action='store_false',
            help='Produce pretty-printed non-minifield JSON. Those are'
            ' more than two times bigger than minified ones.',
        )

    def fetch_bioguide_ids(self):
        """Fetch bioguide IDs from remote list of YAML files.

        YAML files are located in `unitedstates/contact-congress` Github
        repository. Once every few days one of them gets updated, but
        the list itself probably doesn't change often (though more often
        then elections, as e.g. members that weren't supported yet may
        be added.

        Returns:
            List of bioguide IDs.
        """
        response = requests.get(YAML_LIST_URL)
        members_list = json.loads(response.text)
        return [member['name'].rsplit('.', 1)[0] for member in members_list]

    def fetch_members(self, chunk_size, source):
        """Fetch members from a Phantom DC instance.

        Args:
            chunk_size: maximum number of members to fetch in one
                request.
            source: URL of Phantom DC APIs resource for retrieving form
                elements.
        Returns:
            Dict of members, with bioguide IDs as keys and data as
                values.
        """
        fetched_members = {}
        for bioguides_chunk in grouper(chunk_size,
                                       self.fetch_bioguide_ids()):
            response = requests.post(
                source,
                data=json.dumps({'bio_ids': bioguides_chunk}),
                headers={'content-type': 'application/json'})
            for new_bioguide, new_fetched_member in \
                    json.loads(response.text).items():
                fetched_members[new_bioguide] = new_fetched_member
        return fetched_members

    def preprocess_member_data(self, member_data):
        """Change member data.

        Replace values for key `options_hash` with values from
        `OVERRIDEN_FIELD_OPTIONS_HASHES` for member data fields
        which names are in `OVERRIDEN_FIELD_OPTIONS_HASHES`'s keys.

        Args:
            member_data: dict of data for a member. Won't be modified.
        Returns:
            Updated dict of data for the member.
        """
        # TODO We can save a lot of space in the JSON dump by moving
        # this hardcoded data to a place where it won't be reapeated
        # hundreds of times.
        processed_member_data = deepcopy(member_data)
        for field in processed_member_data['required_actions']:
            if field['value'] in OVERRIDEN_FIELD_OPTIONS_HASHES:
                field['options_hash'] = \
                    OVERRIDEN_FIELD_OPTIONS_HASHES[field['value']]
        return processed_member_data

    def save_members(self, members, dest, minify):
        """Save members in a JSON cache file.

        Writes in UTF-8, as (currently) two members (W000779 and
        C000542) have non-ASCII charactes in their `options_hash` lists.

        Args:
            members: list of members data dicts.
            dest: path to file to write to.
            minify: boolean indicating whether to minify the JSON file.
                Minified ones are more than twice smaller than
                pretty-printed ones.
        """
        if minify:
            dump_kwargs = {'separators': (',', ':')}
        else:
            dump_kwargs = {'indent': 4}
        dump = json.dumps(members, sort_keys=True, ensure_ascii=False,
                          **dump_kwargs)
        with io.open(dest, 'w', encoding='utf8') as file_:
            file_.write(unicode(dump))
            file_.write(u'\n')

    def handle(self, *args, **options):
        """Handle the command execution.

        Args:
            args: positional arguments.
            options: options described in `self.add_arguments`.
        """
        if options['chunk_size'] == 1:
            warnings.warn("Encoding problem spotted when the Phantom DC"
                          " server is queried for only one bioguide ID"
                          " at a time. Known affected members: C000542"
                          " and W000779")
        members_dict = self.fetch_members(
            options['chunk_size'], options['source'])
        if options['preprocess']:
            members_dict = {bioguide: self.process_member_data(data)
                            for bioguide, data in members_dict.items()}
        self.save_members(members_dict, options['dest'],
                          options['minify'])

        output_bytes = os.stat(options['dest']).st_size
        self.stdout.write(
            "Written {} members ({:g} MiB) to {}".format(
                len(members_dict),
                round(output_bytes / Decimal(1024)**2, 2),
                options['dest']))
