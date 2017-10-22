import urllib2
from congress.models import Congress
import json
from utils.geo import STATES
from django.conf import settings
from django.forms import model_to_dict
import sqlite3

response1 = urllib2.urlopen('https://theunitedstates.io/congress-legislators/legislators-current.json')
critters = json.load(response1)

response2 = urllib2.urlopen('https://theunitedstates.io/congress-legislators/legislators-social-media.json')
socialMedia = json.load(response2)

CHAMBERS = {
    'rep': 'House',
    'sen': 'Senate'
}

zipsDB = sqlite3.connect('scripts/zips.sqlite')
cursor = zipsDB.cursor()

output = []

for critter in critters:
    newCritter = {
        'bioguide_id': critter['id']['bioguide'],
        'fec_ids': [],
        'zips': []
    }
    try:
        newCritter['thomas_id'] = critter['id']['thomas']
    except:
        pass
    try:
        newCritter['govtrack_id'] = critter['id']['govtrack']
    except:
        pass
    try:
        newCritter['ballotpedia_id'] = critter['id']['ballotpedia']
    except:
        pass
    try:
        newCritter['maplight_id'] = critter['id']['maplight']
    except:
        pass
    try:
        newCritter['icpsr_id'] = critter['id']['icpsr']
    except:
        pass
    try:
        newCritter['opensecrets_id'] = critter['id']['opensecrets']
    except:
        pass
    try:
        newCritter['lis_id'] = critter['id']['lis']
    except:
        pass
    try:
        newCritter['cspan_id'] = critter['id']['cspan']
    except:
        pass
    try:
        newCritter['wikipedia_id'] = critter['id']['wikipedia']
    except:
        pass
    try:
        newCritter['wikidata_id'] = critter['id']['wikidata']
    except:
        pass
    try:
        newCritter['google_entity_id'] = critter['id']['google_entity_id']
    except:
        pass
    try:
        newCritter['votesmart_id'] = critter['id']['votesmart']
    except:
        pass

    for fec_id in critter['id']['fec']:
        newCritter['fec_ids'].append(fec_id)
    newCritter['first_name'] = critter['name']['first']
    newCritter['last_name'] = critter['name']['last']
    try:
        newCritter['middle_name'] = critter['name']['middle']
    except:
        pass
    try:
        newCritter['name_suffix'] = critter['name']['suffix']
    except:
        pass
    try:
        newCritter['leadership_role'] = critter['leadership_roles']['title']
    except:
        pass

    term = critter['terms'][-1]
    # full_name = models.CharField(max_length=50)
    newCritter['chamber'] = CHAMBERS[term['type']]
    newCritter['full_address'] = term['address']
    newCritter['office_address'] = term['office']
    newCritter['state_name'] = STATES[term['state']]
    newCritter['state'] = term['state']
    newCritter['phone'] = term['phone']
    try:
        newCritter['fax'] = term['fax']
    except:
        pass
    try:
        newCritter['website'] = term['url']
    except:
        pass
    try:
        newCritter['rss_url'] = term['rss_url']
    except:
        pass
    try:
        newCritter['senate_class'] = term['class']
    except:
        pass
    try:
        newCritter['contact_form'] = term['contact_form']
    except:
        pass
    try:
        newCritter['district'] = term['district']
    except:
        pass

    if newCritter['chamber'] == 'Senate':
        newCritter['title'] = 'Senator'
    if newCritter['chamber'] == 'House':
        newCritter['title'] = 'Representative'

    newCritter['term_end'] = term['end']
    newCritter['party'] = term['party'][:1]
    newCritter['birthday'] = critter['bio']['birthday']
    newCritter['term_start'] = term['start']

    for item in socialMedia:
        socialBio = item['id']['bioguide']
        if newCritter['bioguide_id'] == socialBio:
            try:
                newCritter['twitter'] = item['social']['twitter']
            except:
                pass
            try:
                newCritter['twitter_id'] = item['social']['twitter_id']
            except:
                pass
            try:
                newCritter['instagram_id'] = item['social']['instagram_id']
            except:
                pass
            try:
                newCritter['instagram'] = item['social']['instagram']
            except:
                pass
            try:
                newCritter['youtube'] = item['social']['youtube']
            except:
                pass
            try:
                newCritter['youtube_id'] = item['social']['youtube_id']
            except:
                pass
            try:
                newCritter['facebook'] = item['social']['facebook']
            except:
                pass

    cursor.execute("select * from main")
    for row in cursor:
        if row[1] == newCritter['first_name'] and row[3] == newCritter['last_name'] and row[5] == newCritter['chamber']:
            zipcode = row[4]
            newCritter['zips'].append(zipcode)
            print "Adding {} for {}".format(zipcode, newCritter['bioguide_id'])

    newCritter['fec_ids'] = ",".join(newCritter['fec_ids'])
    newCritter['zips'] = ",".join(newCritter['zips'])
    outputItem = {}
    outputItem['model'] = 'congress.congress'
    outputItem['pk'] = newCritter['bioguide_id']
    outputItem['fields'] = newCritter

    output.append(outputItem)

with open('{}/fixtures/congress.json'.format(settings.BASE_DIR), 'w') as outfile:
    json.dump(output, outfile)
