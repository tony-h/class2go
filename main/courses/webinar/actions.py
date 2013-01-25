from django.http import HttpResponse, Http404
from django.shortcuts import render, render_to_response, redirect, HttpResponseRedirect
from django.template import Context, loader
from django.template import RequestContext
from django.views.decorators.http import require_POST

from c2g.models import *
from courses.common_page_data import get_common_page_data
from courses.actions import auth_view_wrapper, auth_is_course_admin_view_wrapper
import urllib, urllib2


# A POST request to start a new webinar
@require_POST
def start_meeting(request):

	#TODO: Add the following (course_prefix and course_suffix for categorizing the meetings
	#		(on get recorded meetings, only display the ones for the course
    # course_prefix = request.POST.get("course_prefix")
    # course_suffix = request.POST.get("course_suffix")
    # common_page_data = get_common_page_data(request, course_prefix, course_suffix)

    # if not common_page_data['is_course_admin']:
        # return redirect('courses.views.view', course_prefix, course_suffix)

	# request doc: https://docs.djangoproject.com/en/dev/ref/request-response/
	# Our web service is running on PHP, so doing a cross-system call to get it.
	
	meetingName = request.POST.get("meetingName")
	message = request.POST.get("message")
	#Get the user's display name
	name = request.user.first_name + " " + request.user.last_name
	
	#Encode the params for the POST request
	php_post_url = 'http://cec-online.auca.kg/bigbluebutton/create.php'
	parameters = {	'user': name, 
					'meetingName': meetingName, 
					'welcomeMsg': message
					}
	params = urllib.urlencode(parameters) 

	#Perform POST request
	req = urllib2.Request(php_post_url, params)
	response = urllib2.urlopen(req)
	returned_value = response.read()	
	
	# Instead of only returning the returned text, we should also trap for errors and
	#  return the same code as the web service. Otherwise, the data always looks validate
	return HttpResponse(returned_value)	
	
# A POST request to join a meeting
@require_POST
def join_meeting(request):

	meetingId = request.POST.get("meetingId")
	attendeePw = request.POST.get("attendeePw")
	#Get the user's display name
	name = request.user.first_name + " " + request.user.last_name
	
	#Encode the params for the POST request
	php_post_url = 'http://cec-online.auca.kg/bigbluebutton/invite.php'
	parameters = {'meetingId': meetingId, 'attendeePw': attendeePw, 'name': name, 'redirect': "false" }
	params = urllib.urlencode(parameters) 
	
	#Perform POST request
	req = urllib2.Request(php_post_url, params)
	response = urllib2.urlopen(req)
	returned_value = response.read()	
	
	#Return the URL to open. A direct redirect here will only show it
	#embedded in the current window
	return HttpResponse(returned_value)

	