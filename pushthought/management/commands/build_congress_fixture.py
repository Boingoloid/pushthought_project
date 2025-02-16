import urllib2
import json
from utils.geo import STATES
from django.conf import settings
from django.core.management.base import BaseCommand


DC_ZIP_CODES = (
    '20001',
    '20002',
    '20003',
    '20004',
    '20005',
    '20006',
    '20007',
    '20008',
    '20009',
    '20010',
    '20011',
    '20012',
    '20013',
    '20015',
    '20016',
    '20017',
    '20018',
    '20019',
    '20020',
    '20022',
    '20023',
    '20024',
    '20026',
    '20027',
    '20029',
    '20030',
    '20032',
    '20033',
    '20035',
    '20036',
    '20037',
    '20038',
    '20039',
    '20040',
    '20041',
    '20042',
    '20043',
    '20044',
    '20045',
    '20046',
    '20047',
    '20049',
    '20050',
    '20051',
    '20052',
    '20053',
    '20055',
    '20056',
    '20057',
    '20058',
    '20059',
    '20060',
    '20061',
    '20062',
    '20063',
    '20064',
    '20065',
    '20066',
    '20067',
    '20068',
    '20069',
    '20070',
    '20071',
    '20073',
    '20074',
    '20075',
    '20076',
    '20077',
    '20078',
    '20080',
    '20081',
    '20082',
    '20088',
    '20090',
    '20091',
    '20097',
    '20098',
    '20201',
    '20202',
    '20203',
    '20204',
    '20206',
    '20207',
    '20208',
    '20210',
    '20211',
    '20212',
    '20213',
    '20214',
    '20215',
    '20216',
    '20217',
    '20218',
    '20219',
    '20220',
    '20221',
    '20222',
    '20223',
    '20224',
    '20226',
    '20227',
    '20228',
    '20229',
    '20230',
    '20232',
    '20233',
    '20235',
    '20237',
    '20238',
    '20239',
    '20240',
    '20241',
    '20242',
    '20244',
    '20245',
    '20250',
    '20251',
    '20252',
    '20254',
    '20260',
    '20261',
    '20262',
    '20265',
    '20266',
    '20268',
    '20270',
    '20277',
    '20289',
    '20299',
    '20301',
    '20303',
    '20306',
    '20307',
    '20310',
    '20314',
    '20317',
    '20318',
    '20319',
    '20330',
    '20340',
    '20350',
    '20355',
    '20370',
    '20372',
    '20373',
    '20374',
    '20375',
    '20376',
    '20380',
    '20388',
    '20389',
    '20390',
    '20391',
    '20392',
    '20393',
    '20394',
    '20395',
    '20398',
    '20401',
    '20402',
    '20403',
    '20404',
    '20405',
    '20406',
    '20407',
    '20408',
    '20409',
    '20410',
    '20411',
    '20412',
    '20413',
    '20414',
    '20415',
    '20416',
    '20417',
    '20418',
    '20419',
    '20420',
    '20421',
    '20422',
    '20423',
    '20424',
    '20425',
    '20426',
    '20427',
    '20428',
    '20429',
    '20431',
    '20433',
    '20434',
    '20435',
    '20436',
    '20437',
    '20439',
    '20440',
    '20441',
    '20442',
    '20444',
    '20447',
    '20451',
    '20453',
    '20456',
    '20460',
    '20463',
    '20468',
    '20469',
    '20470',
    '20472',
    '20500',
    '20501',
    '20502',
    '20503',
    '20504',
    '20505',
    '20506',
    '20507',
    '20508',
    '20509',
    '20510',
    '20511',
    '20515',
    '20520',
    '20521',
    '20522',
    '20523',
    '20524',
    '20525',
    '20526',
    '20527',
    '20528',
    '20529',
    '20530',
    '20531',
    '20532',
    '20533',
    '20534',
    '20535',
    '20536',
    '20537',
    '20538',
    '20539',
    '20540',
    '20541',
    '20542',
    '20543',
    '20544',
    '20546',
    '20547',
    '20548',
    '20549',
    '20551',
    '20552',
    '20553',
    '20554',
    '20555',
    '20557',
    '20558',
    '20559',
    '20560',
    '20565',
    '20566',
    '20570',
    '20571',
    '20572',
    '20573',
    '20575',
    '20576',
    '20577',
    '20578',
    '20579',
    '20580',
    '20581',
    '20585',
    '20586',
    '20590',
    '20591',
    '20593',
    '20594',
    '20597',
    '20599',
    '56901',
    '56902',
    '56904',
    '56908',
    '56915',
    '56920',
    '56933',
    '56935',
    '56944',
    '56945',
    '56950',
    '56965',
    '56967',
    '56972',
    '56998',
    '56999',
)


class Command(BaseCommand):
    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        critters = json.load(
            urllib2.urlopen('https://theunitedstates.io/congress-legislators/'
                            'legislators-current.json'))
        socialMedia = json.load(
            urllib2.urlopen('https://theunitedstates.io/congress-legislators/'
                            'legislators-social-media.json'))
        zips_data_source = json.load(
            urllib2.urlopen('https://github.com/bpb27/contact_congress/raw/'
                            'master/data/zips.json'))

        CHAMBERS = {
            'rep': 'House',
            'sen': 'Senate'
        }

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

            for zipcode, state_and_districts in zips_data_source.items():
                state, districts = state_and_districts.split(' ', 1)
                districts = [int(district)
                             for district in districts.split(',')]
                if state == 'tennesee':
                    state = 'tennessee'
                assert newCritter['chamber'] in ('Senate', 'House')
                if (newCritter['state_name'].lower() == state.replace('_', ' ')
                        and (newCritter['chamber'] == 'Senate' or
                             # State-wide district.
                             newCritter['district'] == 0 or
                             newCritter['district'] in districts)):
                    newCritter['zips'].append(zipcode)
                elif newCritter['state_name'] == 'District of Columbia':
                    newCritter['zips'] = DC_ZIP_CODES

            newCritter['fec_ids'] = ",".join(newCritter['fec_ids'])
            newCritter['zips'] = ",".join(newCritter['zips'])
            outputItem = {}
            outputItem['model'] = 'congress.congress'
            outputItem['pk'] = newCritter['bioguide_id']
            outputItem['fields'] = newCritter

            output.append(outputItem)

        with open('{}/fixtures/congress.json'.format(settings.BASE_DIR), 'w') as outfile:
            json.dump(output, outfile, indent=4)
