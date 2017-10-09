"""Management command for updating local cache of Phantom DC forms.

`Member` refers to member of US government that can be contacted using
forms, data for which is provided by Phantom DC.

"""
import os
import os.path
import io
import itertools
import warnings
from decimal import Decimal
import json
import requests
from django.conf import settings
from django.core.management.base import BaseCommand


# EFF's API usually responds to the request for all current 607 members
# just fine, and it's sometimes a little bit faster, but just to make
# this command a bit less fragile we'll request by chunks.
DEFAULT_BIOGUIDES_CHUNK_SIZE = 100
YAML_LIST_URL = 'https://api.github.com/repos/unitedstates/' \
    'contact-congress/contents/members?ref=master'
PHANTOM_DC_FORM_RETRIEVAL_URL = \
    'https://congressforms.eff.org/retrieve-form-elements/'


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
            default=PHANTOM_DC_FORM_RETRIEVAL_URL,
            help='URL of Phantom DC API\'s resource for retrieving form'
            'elements',
        )

    def fetch_bioguide_ids(self):
        """Fetch bioguide IDs from remote list of YAML files.

        YAML files are located in `unitedstates/contact-congress` Github
        repository. Once every few days one of them gets updated, but
        the list itself probably doesn't change often (though more often
        then elections, as e.g. members that weren't supported yet may
        be added.

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

    def save_members(self, members, dest):
        """Save members in a JSON cache file.

        Writes in UTF-8, as (currently) two members (W000779 and
        C000542) have non-ASCII charactes in their `options_hash` lists.

        Args:
            members: list of members data dicts.
            dest: path to file to write to.

        """
        dump = json.dumps(members, sort_keys=True, ensure_ascii=False,
                          separators=(',', ':'))
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
        members = self.fetch_members(options['chunk_size'], options['source'])
        self.save_members(members, options['dest'])

        output_bytes = os.stat(options['dest']).st_size
        self.stdout.write(
            "Written {} members ({:g} MiB) to {}".format(
                len(members),
                round(output_bytes / Decimal(1024)**2, 2),
                options['dest']))
