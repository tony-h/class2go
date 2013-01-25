from django.http import HttpResponse, Http404
from django.shortcuts import render, render_to_response, redirect, HttpResponseRedirect
from django.template import Context, loader
from django.template import RequestContext
from django.views.decorators.http import require_POST

# A POST request to save the updated name of the Google Group
@require_POST
def update(request, course_prefix, course_suffix):
  
    #Update the name of the Google Group in the course
    course = request.common_page_data['draft_course']
    course.google_group = request.POST.get("group_name")
    course.save()
    
    # If set to ready is requested, save to ready course
    if request.POST['action'] == "Save and Set as Ready":
        course = request.common_page_data['ready_course']
        course.google_group = request.POST.get("group_name")
        course.save()
     
    return redirect('courses.google_groups.views.view', course_prefix, course_suffix)
