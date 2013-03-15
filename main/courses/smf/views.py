from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import Context, loader
from django.template import RequestContext
from courses.actions import auth_view_wrapper
from c2g.models import PageVisitLog
from courses.common_page_data import get_common_page_data
import urllib, urllib2, random, string

#Address of the SMF API
def smf_api_baseurl():
    return 'http://class2go.auca.kg/forum/smf-rest-server/api/smf-api-webservice.php'

# Displays the SMF (Simple Machine Forum) page for the course 
@auth_view_wrapper
def view(request, course_prefix, course_suffix):
    
    common_page_data = request.common_page_data
    course = common_page_data['draft_course']

    #Register user if they don't exist in the forum
    if not user_exists(request.user):
        register_user(request.user)
     
    return render_to_response('smf/view.html', {
            'common_page_data': common_page_data,
            'forum_address': 'http://class2go.auca.kg/forum/index.php?board=2.0',
    }, context_instance=RequestContext(request))


# Determines if a user exists or is registered in the SMF forum
def user_exists(user):

    parameters = {  'action': 'user_exists',
                    'member_name': user.username,
                 }
    #Assemble the parms
    params = urllib.urlencode(parameters) 
    
    #Issue the POST request
    req = urllib2.Request(smf_api_baseurl(), params)
    response = urllib2.urlopen(req)
    response = response.read()
    if (response == "True"):
        return True
    else:
        return False

# Registers a new user on SMF
def register_user(user):
    
    #Randomly generate a password. Users can change it if they wish to login to the
    #forum independent of Class2Go
    length = 10
    chars = string.ascii_uppercase + string.ascii_lowercase + string.digits
    password = ''.join(random.choice(chars) for x in range(length))

    parameters = {	'action': 'register',
                    'member_name': user.username,
                    'password': password,
                    'email': user.email, 
                    'real_name': user.first_name + ' ' + user.last_name
                 }

    #Assemble the parms
    params = urllib.urlencode(parameters) 
    
    #Issue the registration POST request
    req = urllib2.Request(smf_api_baseurl(), params)
    response = urllib2.urlopen(req)
    returned_value = response.read()
    
    return returned_value

