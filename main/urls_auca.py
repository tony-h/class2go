from django.conf.urls.defaults import patterns, include, url
from django.views.generic.simple import redirect_to

#---ACUA Custom URL's----

urlpatterns = patterns('',
	
    # Webinars
    url(r'^(?P<course_prefix>[a-zA-Z0-9_-]+)/(?P<course_suffix>[a-zA-Z0-9_-]+)/webinar/?$', 'courses.webinar.views.view'),
    url(r'^courses/webinar/get_recordings/?', 'courses.webinar.views.get_recordings'),
    url(r'^courses/webinar/get_meetings/?', 'courses.webinar.views.get_meetings'),

    url(r'^courses/webinar/start_meeting/?', 'courses.webinar.actions.start_meeting'),
    url(r'^courses/webinar/join_meeting/?', 'courses.webinar.actions.join_meeting'),
    
    # Google groups
    url(r'^(?P<course_prefix>[a-zA-Z0-9_-]+)/(?P<course_suffix>[a-zA-Z0-9_-]+)/google-groups/?$', 'courses.google_groups.views.view'),
    url(r'^(?P<course_prefix>[a-zA-Z0-9_-]+)/(?P<course_suffix>[a-zA-Z0-9_-]+)/google-groups/update?$', 'courses.google_groups.actions.update'),
)
