from views_email_congress import *
from views_user_forms import *
# from scrapex import *
import json
import re
import threading
from django.views.generic.base import TemplateView
from django.utils.decorators import method_decorator
from django.shortcuts import render_to_response
from el_pagination.views import AjaxListView
from el_pagination.decorators import page_template

from programs.models import Program
from campaigns.models import Campaign

PARSE_APP_ID = settings.PARSE_APP_ID
PARSE_REST_KEY = settings.PARSE_REST_KEY
TWITTER_CALLBACK_ROOT_URL = settings.TWITTER_CALLBACK_ROOT_URL
# TWITTER_CALLBACK_ROOT_URL = 'http://www.pushthought.com/verify_catch'

TWITTER_CONSUMER_KEY = settings.TWITTER_CONSUMER_KEY
TWITTER_CONSUMER_SECRET = settings.TWITTER_CONSUMER_SECRET

MONGODB_URI = settings.MONGODB_URI
# Create your views here.

# create scraping object


class HomeView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        context['programs'] = Program.objects.all()[:11]
        return context


class ContactImmediatelyView(TemplateView):
    template_name = 'contact_immediately.html'

    def get_context_data(self, **kwargs):
        context = super(ContactImmediatelyView, self).get_context_data(**kwargs)

        if self.request.session.get('alertList'):
            context['alertList'] = self.request.session['alertList']
            del self.request.session['alertList']
        return context


class CampaignLandingView(TemplateView):
    template_name = 'campaigns/detail.html'

    def get_context_data(self, **kwargs):

        context = super(CampaignLandingView, self).get_context_data(**kwargs)

        return context




@page_template('inserts/documentaries.html', key='documentaries')
@page_template('inserts/webvideos.html', key='webvideos')
def browse_view(request, template="browse.html", extra_context=None):
    query = Program.objects
    context = dict()
    context['all_programs'] = query.all().order_by('-counter')
    context['documentaries'] = query.documentaries().order_by('-counter')
    context['webvideos'] = query.webvideos().order_by('-counter')
    context['podcasts'] = query.podcasts().order_by('-counter')
    context['other'] = query.other().order_by('counter')

    if extra_context is not None:
        context.update(extra_context)
    return render(request, template, context)


@page_template("inserts/campaigns.html")
def browse_campaigns_view(request, template="browse_campaigns.html", extra_context=None):
    query = Campaign.objects
    print(query)
    context = dict()
    context['campaignList'] = query.filter(active=True).order_by('-counter')

    if extra_context is not None:
        context.update(extra_context)
    return render(request, template, context)


def handler404(request):
    response = render_to_response('404.html', {},context_instance=RequestContext(request))
    response.status_code = 404
    return response


def submit_congress_captcha_view(request):
    print "submit_congress_captcha_view firing"
    captcha_response_object = submit_congress_captcha(request)
    status = captcha_response_object['status']
    if captcha_response_object:
        if status == 'success':
            print "email was sent with OK captcha"
            save_congress_email_fields_to_user(request)
            save_email_congress_action(request)
    return HttpResponse(json.dumps(captcha_response_object), content_type="application/json")

def data_loop(request):
    print request.body
    result = request.body
    return HttpResponse(json.dumps(result), content_type="application/json")

def data_throw(request):
    print request.body
    result = request.body
    return HttpResponse(json.dumps(result), content_type="application/json")





def submit_email(request,email):
    # print email
    emailString = email.decode()
    connection2 = httplib.HTTPSConnection('ptparse.herokuapp.com', 443)
    connection2.connect()
    connection2.request('POST', '/parse/classes/EmailsSubmitted', json.dumps({
        "email": emailString
        }), {
        "X-Parse-Application-Id": PARSE_APP_ID,
        "X-Parse-REST-API-Key": PARSE_REST_KEY,
        "Content-Type": "application/json"
    })
    result = json.loads(connection2.getresponse().read())
    return HttpResponseRedirect('/home/')

def contact(request):
    context_instance=RequestContext(request)
    return render(request, 'contact.html')

def send_contact(request):
    print "send contact function!"
    print request.body
    print request.GET
    print request.POST
    print request.session
    print request.META
    context_instance=RequestContext(request)
    contact_data = json.loads(request.body)
    print contact_data

    client = pymongo.MongoClient(MONGODB_URI)
    db = client.get_default_database()
    saveReturn = db.contact_form.save(contact_data)
    print saveReturn

    return render(request, 'contact.html')

def about(request):
    return render(request, 'about.html')

def leaving(request):
    return HttpResponse("Watch function not in place yet, working on it. thanks :)")

def check_db_duplication(request):
    lists = []
    return lists

def browse(request):
    data_lists = check_db_duplication(request)

    if len(data_lists) == 0:
        print "No Database Data"

    program_list = get_program_list()
    program_stats = get_program_browse_stats()
    # program_list_with_stats = get_program_list_with_stats(program_list,program_stats)
    stats_list = get_program_browse_stats_user_count()
    program_list_with_stats = combine_programs_with_stats(program_list,stats_list)

    documentaryArray = []
    webVideoArray = []
    podcastArray = []
    otherArray = []

    # sort and divide
    for item in program_list_with_stats:
        category = item['tagCustom']
        if category == 'documentary':
            documentaryArray.append(item)
        elif category == 'webvideo':
            webVideoArray.append(item)
        elif category == 'podcast':
            podcastArray.append(item)
        else:
            otherArray.append(item)

    dataDict = {}
    dataDict['programList'] = program_list_with_stats
    dataDict['documentaryList'] = documentaryArray
    dataDict['webVideoList'] = webVideoArray
    dataDict['podcastList'] = podcastArray
    dataDict['otherList'] = otherArray

    return render(request, 'browse.html', dataDict)

def content_landing(request, segment_id):
    # get program and segment ID
    # store ID's in session
    program_id = segment_id
    try:
        request.session['programId'] = program_id
        request.session['segmentId'] = segment_id
    except:
        print "error in top of content landing saving request.session segment and program ids - passing on."

    program_result = fetch_program_data(segment_id)
    tweet_data = get_tweet_data(segment_id)
    hashtag_data = get_hashtag_data(segment_id)

    # get user and sentMessage list
    current_user = get_user_by_token_and_id(request)
    if current_user:
        request.session['currentUser'] = current_user
        message_list = get_segment_actions_for_user(segment_id,current_user['objectId'])
        #get email fields

    else:
        message_list = []


    # if location, load congress people (try user, then session)
    try:
        location = current_user['location']
        congress_data = current_user['congressData']
    except:
        try:
            location = request.session['location']
            congress_data = request.session['congressData']
        except:
            location = None
            congress_data = None

    # if zipcode, load congress people
    try:
        zip = current_user['zip']
    except:
        try:
            zip = request.session['zip']
        except:
            zip = None

    # these need
    if location:
        if congress_data:
            hasCongressData = True
            print "loading from location"
            segment_congress_stats = get_congress_stats_for_program(segment_id)
            add_congress_stats(congress_data, segment_congress_stats)
            if message_list:
                congress_data = add_user_touched_data(congress_data, message_list)
                # print message_list

    elif zip:
        hasCongressData = True
        congress_data_raw = get_congress_data(zip) #pulls from api or db
        print "loading from zip"
        congress_data_raw = add_title_and_full_name(congress_data_raw)
        congress_photos = get_congress_photos(congress_data_raw)
        congress_data = add_congress_photos(congress_data_raw, congress_photos)
        segment_congress_stats = get_congress_stats_for_program(segment_id)
        add_congress_stats(congress_data, segment_congress_stats)
        if message_list:
            congress_data = add_user_touched_data(congress_data, message_list)
            # print message_list
    else:
        hasCongressData = False
        congress_data = []


    # create dataDict to send with response.
    dataDict = {}
    # inclue alert list, if returning from an action, these alerts will display on load
    try:
        dataDict['alertList'] = request.session['alertList']
        del request.session['alertList']
        request.session.modified = True
    except:
        print "no alertList to display"

    dataDict['programId'] = program_id
    dataDict['segmentId'] = segment_id
    dataDict['program'] = program_result
    dataDict['currentUser'] = current_user
    dataDict['congressData'] = congress_data
    dataDict['tweetData'] = tweet_data
    dataDict['hashtagData'] = hashtag_data
    dataDict['hasCongressData'] = hasCongressData


    return render(request, 'content_landing.html',dataDict)

def content_landing_empty(request):
    # try:
        # programId = request.session['programId']
        # # del request.session['programId']
        # print "Content_landing_empty, passing on programId:", programId
        # dataDict = {}
        # dataDict['programId'] = programId
        # return render(request, 'content_landing_empty.html',dataDict)
    # except:
    return HttpResponseRedirect('/browse/')

def get_congress_with_zip_view(request, zip):
    congress_data = get_congress_with_zip(request, zip)
    return HttpResponse(json.dumps({'congressData': congress_data}), content_type="application/json")

def get_congress_with_location_view(request):
    # define variables
    data = json.loads(request.body)
    lat = data['lat']
    long = data['long']
    location = {"lat": lat, "long": long}

    # Get congress data using location
    congress_data = get_congress_with_location(request, lat, long)

    # save data to session
    if congress_data:
        request.session['location'] = location
        request.session['congressData'] = congress_data
    # save congress data and location to user, if user available
    try:
        session_token = request.session['sessionToken']
        current_user = request.session['currentUser']
        objectId = request.session['currentUser']['objectId']
        if len(congress_data) != 0:
            save_result = save_location_to_user(location, congress_data, objectId, session_token)
    except:
        print "congress data not saved, either b/c no user, no session, or no data"

    return HttpResponse(json.dumps({'congressData': congress_data}), content_type="application/json")


def get_congress_email_fields_view(request):
    bioguideArray = json.loads(request.body)
    field_list = get_congress_email_fields(bioguideArray)
    return HttpResponse(json.dumps(field_list), content_type="application/json")

# OLD ----------------------------
# OLD ----------------------------
# OLD ----------------------------
# OLD ----------------------------# OLD ----------------------------





# OLD ----------------------------
def fed_rep_action_menu(request, programId, segmentId):

    # Get variables
    program_dict = fetch_program_data(programId)
    segment_dict = fetch_segment_data(segmentId)
    program_data = json.dumps(program_dict)
    segment_data = json.dumps(segment_dict)
    action_list = fetch_action_list(segmentId)

    zipCode = "94107"
    congress_data_raw = get_congress_data(zipCode)
    congress_data_raw = add_title_and_full_name(congress_data_raw)
    congress_photos = get_congress_photos(congress_data_raw)
    congress_data = add_congress_photos(congress_data_raw,congress_photos)

    hashtag_data = get_hashtag_data(segmentId)

    tweet_data = get_tweet_data(segmentId)

    # Store values in session
    source_url = request.build_absolute_uri()
    request.session['last_menu_url'] = source_url
    print "source_url saved in session:" + source_url
    request.session['programId'] = programId
    request.session['segmentId'] = segmentId

    dataDict = {}
    dataDict['actionList'] = action_list
    dataDict['hashtagData'] = hashtag_data
    dataDict['tweetData'] = tweet_data
    dataDict['congressData'] = congress_data

    dataDict['programId'] = programId
    dataDict['programTitle'] = program_dict['programTitle']
    dataDict['programData'] = program_data

    dataDict['segmentId'] = segmentId
    dataDict['segmentTitle'] = segment_dict['segmentTitle']
    dataDict['purposeSummary'] = segment_dict['purposeSummary']
    dataDict['segmentData'] = segment_data

    return render(request, 'fed_rep_action_menu.html', dataDict)


def program_detail(request,programId):

    # if documentary
    client = pymongo.MongoClient(MONGODB_URI)
    db = client.get_default_database()
    program = db.Programs.find_one({"_id":programId})
    # program_dict = fetch_program_data(programId)
    # segment_list = get_segment_list(programId)

    print "print program"
    print program

    dataDict = {}
    dataDict['program'] = program
    # dataDict['programDict'] = program_dict
    # dataDict['segmentList'] = segment_list
    # dataDict['programObjectId'] = program_dict['objectId']

    return render(request, 'program_detail.html',dataDict)

# Use the login_required() decorator to ensure only those logged in can access the view.
# @login_required

from django.core.urlresolvers import reverse
from django.shortcuts import redirect

def account_home(request, user_pk):


    dataDict = {}
    try:
        session_token = request.session['sessionToken']
        print "session token top of account home:" + session_token
        current_user = get_user_in_parse_only(request, user_pk)
        dataDict['current_user'] = current_user

        programs = get_program_list_for_user(user_pk)
        dataDict['programs'] = programs
        print programs

    except:
        print "no session token available on account home"
        print "no current user so redirecting to Sign In"
        return redirect(reverse('user_signin_form'))

    dataDict['user_pk'] = user_pk

    #programs = Program.objects.filter(user=user_pk)
    # dataDict['programs'] = programs

    return render(request, 'account_home.html', dataDict)




# @login_required
def segment_list(request, user_pk, program_pk):
    program = get_object_or_404(Program, pk=program_pk)
    segments = Segment.objects.filter(program__pk=program_pk)

    # Entry.objects.filter(blog__name='Beatles Blog')
    #   get_list_or_404(Segment, program= program_pk)

    dataDict = {}
    dataDict['user_pk'] = user_pk
    dataDict['segments'] = segments
    dataDict['program'] = program
    return render(request, 'segment_list.html', dataDict)


# @login_required
# def segment_menu(request, user_pk, program_pk, segment_pk):
#     menuItems = MenuItem.objects.filter(segment__pk=segment_pk)
#     segment = get_object_or_404(Segment, pk=segment_pk)
#     program = get_object_or_404(Program, pk=program_pk)
#
#     dataDict = {}
#     dataDict['menuItems'] = menuItems
#     dataDict['segment'] = segment
#     dataDict['program'] = program
#
#     return render(request, 'segment_menu.html', dataDict)

    #NEW STUFF-----------------------------------------------------------------------------------------------







def action_menu(request, programId, segmentId):
    program_dict = fetch_program_data(programId)
    segment_dict = fetch_segment_data(segmentId)
    program_data = json.dumps(program_dict)
    segment_data = json.dumps(segment_dict)

    action_list = fetch_action_list(segmentId)
    formatted_action_list = format_action_list(action_list)  # make distinct and sort
    petition_url = get_petition_url(action_list)

    dataDict = {}
    dataDict['actionList'] = formatted_action_list
    dataDict['petitionURL'] = petition_url
    dataDict['programId'] = programId
    dataDict['programTitle'] = program_dict['programTitle']
    dataDict['programData'] = program_data

    dataDict['segmentId'] = segmentId
    dataDict['segmentTitle'] = segment_dict['segmentTitle']
    dataDict['purposeSummary'] = segment_dict['purposeSummary']
    dataDict['segmentData'] = segment_data

    return render(request, 'action_menu.html', dataDict)

def petition(request, programId, segmentId):
    redirect_url = "a"
    return HttpResponseRedirect(redirect_url)


# Twitter Verification and helper methods


    # def register(request):
    #
    #     # A boolean value for telling the template whether the registration was successful.
    #     # Set to False initially. Code changes value to True when registration succeeds.
    #     registered = False
    #
    #     # If it's a HTTP POST, we're interested in processing form data.
    #     if request.method == 'POST':
    #         # Attempt to grab information from the raw form information.
    #         # Note that we make use of both UserForm and UserProfileForm.
    #         user_form = UserForm(data=request.POST)
    #         profile_form = UserProfileForm(data=request.POST)
    #
    #         # If the two forms are valid...
    #         if user_form.is_valid() and profile_form.is_valid():
    #             # Save the user's form data to the database.
    #             user = user_form.save()
    #
    #             # Now we hash the password with the set_password method.
    #             # Once hashed, we can update the user object.
    #             user.set_password(user.password)
    #             user.save()
    #
    #             # Now sort out the UserProfile instance.
    #             # Since we need to set the user attribute ourselves, we set commit=False.
    #             # This delays saving the model until we're ready to avoid integrity problems.
    #             profile = profile_form.save(commit=False)
    #             profile.user = user
    #
    #             # Did the user provide a profile picture?
    #             # If so, we need to get it from the input form and put it in the UserProfile model.
    #             if 'picture' in request.FILES:
    #                 profile.picture = request.FILES['picture']
    #
    #             # Now we save the UserProfile model instance.
    #             profile.save()
    #
    #             # Update our variable to tell the template registration was successful.
    #             registered = True
    #
    #         # Invalid form or forms - mistakes or something else?
    #         # Print problems to the terminal.
    #         # They'll also be shown to the user.
    #         else:
    #             print user_form.errors, profile_form.errors
    #
    #     # Not a HTTP POST, so we render our form using two ModelForm instances.
    #     # These forms will be blank, ready for user input.
    #     else:
    #         user_form = UserForm()
    #         profile_form = UserProfileForm()
    #
    #     # Render the template depending on the context.
    #     return render(request,
    #             'registration_form.html',
    #             {'user_form': user_form, 'profile_form': profile_form, 'registered': registered} )

    # def user_login(request):
    #
    #     # If the request is a HTTP POST, try to pull out the relevant information.
    #     if request.method == 'POST':
    #         # Gather the username and password provided by the user.
    #         # This information is obtained from the login form.
    #                 # We use request.POST.get('<variable>') as opposed to request.POST['<variable>'],
    #                 # because the request.POST.get('<variable>') returns None, if the value does not exist,
    #                 # while the request.POST['<variable>'] will raise key error exception
    #         username = request.POST.get('username')
    #         password = request.POST.get('password')
    #
    #         # Use Django's machinery to attempt to see if the username/password
    #         # combination is valid - a User object is returned if it is.
    #         user = authenticate(username=username, password=password)
    #         print user
    #         # If we have a User object, the details are correct.
    #         # If None (Python's way of representing the absence of a value), no user
    #         # with matching credentials was found.
    #         if user:
    #             # Is the account active? It could have been disabled.
    #             if user.is_active:
    #                 # If the account is valid and active, we can log the user in.
    #                 # We'll send the user back to the homepage.
    #                 login(request, user)
    #                 return HttpResponseRedirect('/about/')
    #             else:
    #                 # An inactive account was used - no logging in!
    #                 return HttpResponse("Your Push Thought account is disabled.")
    #         else:
    #             # Bad login details were provided. So we can't log the user in.
    #             print "Invalid login details: {0}, {1}".format(username, password)
    #             return HttpResponse("Invalid login details supplied.")
    #
    #     # The request is not a HTTP POST, so display the login form.
    #     # This scenario would most likely be a HTTP GET.
    #     else:
    #         # No context variables to pass to the template system, hence the
    #         # blank dictionary object...
    #         return render(request, 'login.html', {})

# def get_scraping_start_urls(search_keyword):
#     s = Scraper(
#         use_cache=False,  # enable cache globally
#         retries=2,
#         delay=0.5,
#         timeout=60,
#         proxy_file='proxy.txt',
#         proxy_auth='silicons:1pRnQcg87F'
#     )
#
#     lock = threading.Lock()
#     logger = s.logger
#
#     youtube_url = 'http://www.youtube.com/results?search_query='
#     limit_top_url_count = 10
#     youtube_meta_list = []
#     youtube_scraping_url_list = []
#
#     url = youtube_url + search_keyword
#     logger.info('loading parent page...' + url)
#     html = s.load(youtube_url + search_keyword, use_cache = False)
#
#     proxy = html.response.request.get("proxy")
#     logger.info(proxy.host + ":" + str(proxy.port))
#
#     video_divs = html.q("//div[contains(@class, 'yt-lockup-thumbnail contains-addto')]/a")
#
#     href_links = []
#     if len(video_divs) > 0:
#         for i, row in enumerate(video_divs):
#             if i >= limit_top_url_count: break
#             href_links.append(row.x("@href"))
#
#     return href_links
#
# def get_youtube_urls(href_links):
#     threads = []
#     for i, url in enumerate(href_links):
#         thread_obj = threading.Thread(target = parse_youtube_webpage, args = (url,))
#         threads.append(thread_obj)
#         thread_obj.start()
#
# def parse_youtube_webpage(url):
#     html = s.load(url, use_cache=False)
#
#     proxy = html.response.request.get("proxy")
#     logger.info(proxy.host + ":" + str(proxy.port) + ", URL -> " + url)
#     get_youtube_meta_data(html, url)
#
# def get_youtube_meta_data(html, url):
#     lock.acquire()
#     meta_elements = html.q("//meta")
#
#     for row in meta_elements:
#         meta_name = row.x("@name")
#         meta_content = row.x("@content")
#         meta_property = row.x("@property")
#         meta_itemprop = row.x("@itemprop")
#
#         if meta_name != "":
#             attribute_type = "name"
#             attribute_value= meta_name
#         elif meta_property != "":
#             attribute_type = "property"
#             attribute_value= meta_property
#         elif meta_itemprop != "":
#             attribute_type = "itemprop"
#             attribute_value= meta_itemprop
#
#         meta_info = [   'attribute_type', attribute_type,
#                         'attribute_value', attribute_value,
#                         'meta_content', meta_content,
#                         'url', url]
#
#
#         youtube_meta_list.append(meta_info)
#
#     lock.release()
#     youtube_scraping_url_list.append(url)
