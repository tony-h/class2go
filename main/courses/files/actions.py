from django.http import Http404
from django.shortcuts import render, redirect

from courses.actions import auth_is_course_admin_view_wrapper
from courses.common_page_data import get_common_page_data
from courses.files.forms import *


@auth_is_course_admin_view_wrapper
def upload(request):
    course_prefix = request.POST.get("course_prefix")
    course_suffix = request.POST.get("course_suffix")
    common_page_data = get_common_page_data(request, course_prefix, course_suffix)

    if request.method == "POST":
        form = FileUploadForm(request.POST, request.FILES, course=common_page_data['course'])
        if form.is_valid():
            new_file = form.save(commit=False)
            new_file.course = common_page_data['course']
            new_file.index = new_file.section.getNextIndex()
            new_file.mode = 'draft'
            new_file.handle = course_prefix + "--" + course_suffix

            new_file.save()
            new_file.create_ready_instance()

            parent_type = request.POST.get('parent')
            if parent_type and parent_type[:4] != 'none':
                parent_type, parent_id = parent_type.split(',')
            else:
                parent_type, parent_id = None, None

            if parent_type:
                parent_ref = ContentGroupGroupFactory.groupable_types[parent_type].objects.get(id=long(parent_id)).image
                print "DEBUG: creating parent/child relationship between", parent_type, parent_ref.id, "and file", new_file.image.id
                content_group_groupid = ContentGroupGroupFactory.add_parent(common_page_data['course'], parent_type, parent_ref)
                ContentGroupGroupFactory.add_child(content_group_groupid, 'file', new_file.image)

            return redirect('courses.views.course_materials', course_prefix, course_suffix)
    else:
        form = FileUploadForm(course=common_page_data['course'])

    return render(request, 'files/upload.html',
            {'common_page_data': common_page_data,
             'form': form,
             })

@auth_is_course_admin_view_wrapper
def delete_file(request):
    try:
        common_page_data = get_common_page_data(request, request.POST.get("course_prefix"), request.POST.get("course_suffix"))
    except:
        raise Http404

    file = File.objects.get(id=request.POST.get("file_id"))
    file.delete()
    file.image.delete()

    return redirect(request.META['HTTP_REFERER'])
