
from django.conf import settings
PARSE_APP_ID = settings.PARSE_APP_ID
PARSE_REST_KEY = settings.PARSE_REST_KEY
PARSE_SERVER_URL = 'https://ptparse.herokuapp.com/parse'

# import json, httplib
# connection = httplib.HTTPSConnection('ptparse.herokuapp.com', 443)
# connection.connect()
# connection.request('GET', '/parse/classes/CongressRequiredEmailFields','',
#                    {
#                        "X-Parse-Application-Id": PARSE_APP_ID,
#                        "X-Parse-REST-API-Key": PARSE_REST_KEY,
#                        "Content-Type": "application/json"
#                    })
# result = json.loads(connection.getresponse().read())
# field_list_objects = result['results']


def create_master_field_list(field_list_objects):
    #  Create array with fields for bioguide depending on who the field belongs to
    formatted_array = []
    for field_list_object in field_list_objects:
        bioguideId = field_list_object['bioguideId']
        for field in field_list_object['required_fields']:
            try:
                options_length = len(field['options_hash'])
            except:
                options_length = 0


            temp_dict = {
                "value": field['value'],
                "bioguideId": bioguideId,
                "maxlength": field['maxlength'],
                "options_hash": field['options_hash'],
                "options_length": options_length
                }
            formatted_array.append(temp_dict)

    # Sort the mother fucker
    import operator
    sorted_array = sorted(formatted_array, key=operator.itemgetter('value','options_length'))
    # print len(sorted_array)

    #  Strip out extra duplicates, group bioguide IDs
    count = 0
    length = len(sorted_array)
    sorted_clip = []
    previous_item = "A"
    for item in sorted_array:
        count = count + 1
        if count != length:
            if previous_item == "A":
                previous_item = item
            elif previous_item['value'] == 'TOPIC':
                sorted_clip.append(previous_item)
                previous_item = item
            elif item['value'] != previous_item['value']:
                sorted_clip.append(previous_item)
                previous_item = item
            elif item['value'] == previous_item['value']:
                previous_item['bioguideId'] = previous_item['bioguideId'] + ' ' + item['bioguideId']
        elif count == length: # behavior different if last in list
            if previous_item['value'] == 'TOPIC':
                sorted_clip.append(previous_item)
                sorted_clip.append(item)
            elif item['value'] != previous_item['value']:
                sorted_clip.append(previous_item)
                sorted_clip.append(item)
            elif item['value'] == previous_item['value']:
                sorted_clip.append(previous_item)

    # print len(sorted_clip)
    # print sorted_clip

    # master list showing order fields appear on form
    master_ordered_list = [
        "MESSAGE",
        "NAME_PREFIX",
        "NAME_FIRST",
        "NAME_LAST",
        "EMAIL",
        "PHONE",
        "ADDRESS_STREET",
        "ADDRESS_CITY",
        "ADDRESS_ZIP4",
        "ADDRESS_ZIP5",
        "SUBJECT",
        "TOPIC",
    ]

    # separate into those to order and those to put at end (thsoe not included in the ordered list above automatically get put at the end)
    objects_to_end = []
    objects_to_order = []
    for item in sorted_clip:
        found = False
        for list_item in master_ordered_list:
            if item['value'] == list_item:
                found = True
        if found:
            objects_to_order.append(item)
        elif not found:
            objects_to_end.append(item)

    # order the list to be ordered based on master list
    ordered_objects = []
    for list_item in master_ordered_list:
        # print list_item
        for object_item in objects_to_order:
            # print "testing against:", object_item['value']
            if object_item['value'] == list_item:
                ordered_objects.append(object_item)


    if len(ordered_objects) != 0:
        ordered_objects = ordered_objects + objects_to_end

    # print len(objects_to_order)
    # print len(ordered_objects)
    print ordered_objects
    return ordered_objects

