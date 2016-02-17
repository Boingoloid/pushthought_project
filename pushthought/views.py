from django.shortcuts import get_list_or_404, get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import authenticate, login
from pushthought.forms import UserForm, UserProfileForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from .models import Program
from .models import Segment
from .models import MenuItem
from .forms import SegmentForm

import json
import jsonpickle

# Create your views here.

def home(request):
    userDict = dict()
    userDict['users'] = User.objects.all()
    return render(request, 'home.html',userDict)

def about(request):

    return render(request,'about.html')

def api(request):

    obj = Program.objects.all()
    frozen = jsonpickle.encode(obj)
    return HttpResponse(obj, content_type='application/json')


# @login_required
def account_home(request,user_pk):
    programs = Program.objects.filter(user = user_pk)
    dataDict = {}
    dataDict['user_pk'] = user_pk
    dataDict['programs'] = programs

    return render(request, 'account_home.html',dataDict)

# @login_required
def segment_list(request,user_pk,program_pk):
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
def segment_menu(request,user_pk, program_pk,segment_pk):
    menuItems = MenuItem.objects.filter(segment__pk=segment_pk)
    segment = get_object_or_404(Segment, pk = segment_pk)
    program = get_object_or_404(Program, pk = program_pk)

    dataDict = {}
    dataDict['menuItems'] = menuItems
    dataDict['segment'] = segment
    dataDict['program'] = program

    return render(request, 'segment_menu.html', dataDict)

# @login_required
def add_segment(request,user_pk,program_pk):

    program = get_object_or_404(Program, pk = program_pk)

    # A HTTP POST?
    if request.method == 'POST':
        form = SegmentForm(request.POST)

        # Have we been provided with a valid form?
        if form.is_valid():
            # Save the new category to the database.
            form.save(commit=True)

            # Now call the index() view.
            # The user will be shown the homepage.
            return home(request)
        else:
            # The supplied form contained errors - just print them to the terminal.
            print form.errors
    else:
        # If the request was not a POST, display the form to enter details.
        form = SegmentForm(initial={'program': program})

    # Bad form (or form details), no form supplied...
    # Render the form with error messages (if any).
    return render(request,'add_segment.html', {'form': form, 'program': program})



def contact(request):
    return render(request,'contact.html')

def register(request):

    # A boolean value for telling the template whether the registration was successful.
    # Set to False initially. Code changes value to True when registration succeeds.
    registered = False

    # If it's a HTTP POST, we're interested in processing form data.
    if request.method == 'POST':
        # Attempt to grab information from the raw form information.
        # Note that we make use of both UserForm and UserProfileForm.
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)

        # If the two forms are valid...
        if user_form.is_valid() and profile_form.is_valid():
            # Save the user's form data to the database.
            user = user_form.save()

            # Now we hash the password with the set_password method.
            # Once hashed, we can update the user object.
            user.set_password(user.password)
            user.save()

            # Now sort out the UserProfile instance.
            # Since we need to set the user attribute ourselves, we set commit=False.
            # This delays saving the model until we're ready to avoid integrity problems.
            profile = profile_form.save(commit=False)
            profile.user = user

            # Did the user provide a profile picture?
            # If so, we need to get it from the input form and put it in the UserProfile model.
            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']

            # Now we save the UserProfile model instance.
            profile.save()

            # Update our variable to tell the template registration was successful.
            registered = True

        # Invalid form or forms - mistakes or something else?
        # Print problems to the terminal.
        # They'll also be shown to the user.
        else:
            print user_form.errors, profile_form.errors

    # Not a HTTP POST, so we render our form using two ModelForm instances.
    # These forms will be blank, ready for user input.
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    # Render the template depending on the context.
    return render(request,
            'registration_form.html',
            {'user_form': user_form, 'profile_form': profile_form, 'registered': registered} )

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


from django.contrib.auth import logout

# Use the login_required() decorator to ensure only those logged in can access the view.
# @login_required
def user_logout(request):
    # Since we know the user is logged in, we can now just log them out.
    logout(request)

    # Take the user back to the homepage.
    return HttpResponseRedirect('/home/')