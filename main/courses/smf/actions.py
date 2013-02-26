from django.http import HttpResponse, Http404
from django.shortcuts import render, render_to_response, redirect, HttpResponseRedirect
from django.template import Context, loader
from django.template import RequestContext
from django.views.decorators.http import require_POST
import urllib, urllib2
import base64

#Address of the SMF API
def smf_api_baseurl():
    return 'http://class2go.auca.kg/forum/smf-rest-server/api/smf-api-webservice.php'

# A POST request to get the username and the hashed password
# This is returned to automatically log the user in to the SMF forums
@require_POST   
def get_credentials(request, course_prefix, course_suffix):
   
    user = request.user
   
    #Encode the username and password to be sent to SMF API via AJAX
    encoded_user = base64.urlsafe_b64encode(user.username)
    encoded_pass = base64.urlsafe_b64encode(user.password)
    
    json_response = '{ "member_name":"' +  encoded_user
    json_response += '", "password":"' + encoded_pass
    json_response += '", "url":"' + smf_api_baseurl()
    json_response += '"}'

    return HttpResponse(json_response)
