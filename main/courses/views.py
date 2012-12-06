from django.http import HttpResponse, Http404
from django.shortcuts import render_to_response
from django.template import Context, loader
from django.template import RequestContext
from c2g.models import *
from courses.course_materials import get_course_materials, group_data
from courses.common_page_data import get_common_page_data
import re
from django.contrib import messages
from django.shortcuts import redirect
from django.core.urlresolvers import reverse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_protect

from courses.forms import *

from courses.actions import auth_view_wrapper

from c2g.models import CurrentTermMap
import settings

def index(item): # define a index function for list items
 return item[1]


curTerm = 'Fall2012'

def current_redirects(request, course_prefix):
    try:
        suffix = CurrentTermMap.objects.get(course_prefix=course_prefix).course_suffix
    except CurrentTermMap.DoesNotExist:
        suffix = curTerm # Use this as default fallback

    if Course.objects.filter(handle=course_prefix+'--'+suffix).exists():
        return redirect(reverse('courses.views.main',args=[course_prefix, suffix]))
    else: 
        raise Http404
    

def main(request, course_prefix, course_suffix):
    #Common page data is already run in middleware
    #try:
    #    common_page_data = get_common_page_data(request, course_prefix, course_suffix)
    #except Course.DoesNotExist:
    #    raise Http404

    common_page_data=request.common_page_data
    ##JASON 9/5/12###
    ##For Launch, but I don't think it needs to be removed later##
    if common_page_data['course'].preview_only_mode:
        if not common_page_data['is_course_admin']:
            redir = reverse('courses.preview.views.preview',args=[course_prefix, course_suffix])
            if (settings.INSTANCE == 'stage' or settings.INSTANCE == 'prod'):
                redir = 'https://'+request.get_host()+redir
            return redirect(redir)

    
    announcement_list = Announcement.objects.getByCourse(course=common_page_data['course']).order_by('-time_created')[:11]
    if len(announcement_list) > 10:
        many_announcements = True
        announcement_list = announcement_list[0:10]
    else:
        many_announcements = False
    
    if request.user.is_authenticated():
        is_logged_in = 1
        news_list = common_page_data['ready_course'].newsevent_set.all().order_by('-time_created')[0:5]
    else:
        is_logged_in = 0
        news_list = []

    course = common_page_data['course']
    contentsection_list, video_list, pset_list, additional_pages, file_list, groups, exam_list, level2_items = get_left_nav_content(course)
    full_contentsection_list, full_index_list = get_full_contentsection_list(course, contentsection_list, video_list, pset_list, additional_pages, file_list, exam_list, level2_items)

    return render_to_response('courses/view.html',
            {'common_page_data': common_page_data,
             'announcement_list': announcement_list,
             'many_announcements':many_announcements,
             'news_list': news_list,
             'contentsection_list': full_contentsection_list,
             'video_list': video_list,
             'pset_list': pset_list,
             'full_index_list': full_index_list,
             'is_logged_in': is_logged_in
             },

            context_instance=RequestContext(request))

@auth_view_wrapper
def course_materials(request, course_prefix, course_suffix):


    section_structures = get_course_materials(common_page_data=request.common_page_data, get_video_content=True, get_pset_content=True, get_additional_page_content=True, get_file_content=True, get_exam_content=True)

    form = None
    if request.common_page_data['course_mode'] == "draft":
        form = LiveDateForm()
    
    return render_to_response('courses/'+request.common_page_data['course_mode']+'/course_materials.html', {'common_page_data': request.common_page_data, 'section_structures':section_structures, 'context':'course_materials', 'form':form}, context_instance=RequestContext(request))

@auth_view_wrapper
@require_POST
@csrf_protect
def unenroll(request, course_prefix, course_suffix):
    
    try:
        course = Course.objects.get(handle=course_prefix+'--'+course_suffix, mode='ready')
    except Course.DoesNotExist:
        raise Http404
            
    student_group = Group.objects.get(id=course.student_group_id)
    student_group.user_set.remove(request.user)
    
    return redirect(request.META['HTTP_REFERER'])


def get_full_contentsection_list(course, contentsection_list, video_list, pset_list, additional_pages, file_list, exam_list, level2_items):

    full_index_list = []
    full_contentsection_list=[]
    
    for contentsection in contentsection_list:
    
        index_list = []
        for video in video_list:
            if video.section_id == contentsection.id and not level2_items.has_key('video:' + str(video.id)):
                index_list.append(('video', video.index, video.id, contentsection.id, video.slug, video.title))

        for pset in pset_list:
            if pset.section_id == contentsection.id and not level2_items.has_key('pset:' + str(pset.id)):
                index_list.append(('pset', pset.index, pset.id, contentsection.id, pset.slug, pset.title))
                
        for page in additional_pages:
            if page.section_id == contentsection.id and not level2_items.has_key('page:' + str(page.id)):
                index_list.append(('additional_page', page.index, page.id, contentsection.id, page.slug, page.title))

        for file in file_list:
            if file.section_id == contentsection.id and not level2_items.has_key('file:' + str(file.id)):
                icon_type = file.get_icon_type()
                index_list.append(('file', file.index, file.id, contentsection.id, file.file.url, file.title, icon_type))

        for exam in exam_list:
            if exam.section_id == contentsection.id and not level2_items.has_key('exam:' + str(exam.id)):
                index_list.append(('exam', exam.index, exam.id, contentsection.id, exam.slug, exam.title))

        index_list.sort(key = index)
        
        full_index_list.append(index_list)

        # don't show empty sections
        if index_list:
            full_contentsection_list.append(contentsection)
        
    return full_contentsection_list, full_index_list


def get_left_nav_content(course):

    contentsection_list = ContentSection.objects.getByCourse(course=course)
    video_list = Video.objects.getByCourse(course=course)
    pset_list =  ProblemSet.objects.getByCourse(course=course)
    additional_pages =  AdditionalPage.objects.getSectionPagesByCourse(course=course)
    file_list = File.objects.getByCourse(course=course)
    groups = ContentGroup.objects.getByCourse(course=course)
    level1_items, level2_items = group_data(groups)
    exam_list = Exam.objects.getByCourse(course=course)
    
    return contentsection_list, video_list, pset_list, additional_pages, file_list, groups, exam_list, level2_items