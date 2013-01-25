from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import Context, loader
from django.template import RequestContext
from courses.actions import auth_view_wrapper
from c2g.models import PageVisitLog

from courses.common_page_data import get_common_page_data

# Displays the Google Group page for the course 
@auth_view_wrapper
def view(request, course_prefix, course_suffix):
    
    common_page_data = request.common_page_data
    course = common_page_data['draft_course']
    
    #Construct the Google Group name for suggestion    
    institution = str(course.institution).lower()
    recommended_google_group_name = institution + "-" + course_prefix + "--" + course_suffix

    return render_to_response('google_groups/view.html', {
            'common_page_data': common_page_data,
            'recommended_google_group_name': recommended_google_group_name,
            'host': request.META["HTTP_HOST"]
        }, context_instance=RequestContext(request))
