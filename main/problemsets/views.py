from django.core.urlresolvers import reverse
from c2g.models import Course, ProblemActivity, ProblemSet, ContentSection, Exercise, ProblemSetToExercise, VideoToExercise, PageVisitLog
from django.http import HttpResponse, Http404
from django.shortcuts import render_to_response, HttpResponseRedirect, render
from django.template import RequestContext
from courses.common_page_data import get_common_page_data
from courses.course_materials import get_course_materials
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime, timedelta
from problemsets.forms import *
from django.db.models import Q
from courses.actions import auth_view_wrapper, auth_is_course_admin_view_wrapper
from django.views.decorators.http import require_POST
from courses.forms import *
from django.contrib import messages

# Filters all ProblemActivities by problem set and student. For each problem set, finds out how
# many questions there are and how many were completed to calculate progress on
# each problem set. Packages this information along with problem set
# information about deadlines into a dictionary and passes it to the template.


@auth_view_wrapper
def list(request, course_prefix, course_suffix):
    common_page_data = request.common_page_data
   

    section_structures = get_course_materials(common_page_data=common_page_data, get_video_content=False, get_pset_content=True)

    form = None
    if request.common_page_data['course_mode'] == "draft":
        form = LiveDateForm()

    return render_to_response('problemsets/'+common_page_data['course_mode']+'/list.html', {'common_page_data': common_page_data, 'section_structures':section_structures, 'context':'problemset_list', 'form': form}, context_instance=RequestContext(request))

@auth_view_wrapper
def show(request, course_prefix, course_suffix, pset_slug):
    
    common_page_data = request.common_page_data 
    try:
        ps = ProblemSet.objects.getByCourse(course=common_page_data['course']).get(slug=pset_slug)
    except ProblemSet.DoesNotExist:
        messages.add_message(request,messages.ERROR, 'This Problemset is not visible in the student view at this time. Please note that students will not see this message.')
        return HttpResponseRedirect(reverse('problemsets.views.list', args=(course_prefix, course_suffix)))
    except ProblemSet.MultipleObjectsReturned:
        messages.add_message(request,messages.ERROR, 'We found multiple problem sets with the same slug.  Please try to delete one.  This most likely happened due to copying content from another course.')
        return HttpResponseRedirect(reverse('problemsets.views.list', args=(course_prefix, course_suffix)))


    if not common_page_data['is_course_admin']:
        visit_log = PageVisitLog(
            course = common_page_data['ready_course'],
            user = request.user,
            page_type = 'problemset',
            object_id = str(ps.id),
        )
        visit_log.save()
        
    problem_activities = ProblemActivity.objects.select_related('problemset_to_exercise').filter(student=request.user, problemset_to_exercise__problemSet=ps)
    psetToExs = ProblemSetToExercise.objects.getByProblemset(ps)
    activity_list = []
    for psetToEx in psetToExs:
        #attempts = problem_activities.filter(problemset_to_exercise=psetToEx).order_by('-time_created')
        #attempts = problem_activities.filter(problemset_to_exercise=psetToEx).order_by('-complete', '-attempt_number')
        attempts = problem_activities.filter(problemset_to_exercise__exercise__fileName=psetToEx.exercise.fileName).order_by('-complete', '-attempt_number')  
        if attempts.exists():
            activity_list.append(attempts[0])
    return render_to_response('problemsets/problemset.html',
                              {'common_page_data':common_page_data,
                               'pset': ps,
                               'pset_url':ps.path,
                               'pset_type':ps.assessment_type,
                               'pset_penalty':ps.resubmission_penalty,
                               'pset_attempts_allowed':ps.submissions_permitted,
                               'activity_list': activity_list,
                              },
                              context_instance=RequestContext(request))



#CSRF Protected version, wrapped
@require_POST
#@auth_view_wrapper
def attempt_protect(request, problemId):
    return attempt(request, problemId)

@csrf_exempt
@require_POST
#@auth_view_wrapper
def attempt(request, problemId):
    user = request.user

    exercise_type = request.POST['exercise_type']
    if exercise_type == 'problemset':
        problemset_to_exercise = ProblemSetToExercise.objects.distinct().get(problemSet__id=request.POST['pset_id'], exercise__fileName=request.POST['exercise_filename'], is_deleted=False)
        attempts = ProblemActivity.objects.filter(problemset_to_exercise=problemset_to_exercise, student=request.user).exclude(attempt_content='hint').count()
        # Chokes if user_selection_val isn't provided, so set to blank
        post_selection_val = request.POST.get('user_selection_val', '')
        # Only increment attempts if it's not a hint request
        if request.POST['attempt_content'] != 'hint':
            attempts += 1
        problem_activity = ProblemActivity(student = user,
                                           problemset_to_exercise = problemset_to_exercise,
                                           complete = request.POST['complete'],
                                           attempt_content = request.POST['attempt_content'],
                                           count_hints = request.POST.get('count_hints', 0),
                                           time_taken = request.POST['time_taken'],
                                           seed = request.POST['seed'],
                                           attempt_number = attempts,
                                           problem_type = request.POST['problem_type'],
                                           user_selection_val = post_selection_val,
                                           user_choices = request.POST['user_choices'])

    elif exercise_type == 'video':
        video_to_exercise = VideoToExercise.objects.distinct().get(video__id=request.POST['video_id'], exercise__fileName=request.POST['exercise_filename'], is_deleted=False)
        attempts = ProblemActivity.objects.filter(video_to_exercise=video_to_exercise, student=request.user).exclude(attempt_content='hint').count()
        # Chokes if user_selection_val isn't provided, so set to blank
        post_selection_val = request.POST.get('user_selection_val', '')
        # Only increment attempts if it's not a hint request
        if request.POST['attempt_content'] != 'hint':
            attempts += 1
        problem_activity = ProblemActivity(student = user,
                                           video_to_exercise = video_to_exercise,
                                           complete = request.POST['complete'],
                                           attempt_content = request.POST['attempt_content'],
                                           count_hints = request.POST.get('count_hints', 0),
                                           time_taken = request.POST['time_taken'],
                                           seed = request.POST['seed'],
                                           attempt_number = attempts,
                                           problem_type = request.POST['problem_type'],
                                           user_selection_val = post_selection_val,
                                           user_choices = request.POST['user_choices'])

    problem_activity.save()
    if request.POST['complete'] == "1":
        activityConfirmation = '{"exercise_status":"complete", "attempt_num": ', problem_activity.attempt_number, '}'
    elif request.POST['attempt_content'] == "hint":
        activityConfirmation = '{"exercise_status":"hint", "attempt_num": ', problem_activity.attempt_number, '}'
    else:
        activityConfirmation = '{"exercise_status":"wrong", "attempt_num": ', problem_activity.attempt_number, '}'
    return HttpResponse(activityConfirmation)

@auth_is_course_admin_view_wrapper
def create_form(request, course_prefix, course_suffix):
    try:
        common_page_data = get_common_page_data(request, course_prefix, course_suffix)
    except:
        raise Http404

    data = {'common_page_data': common_page_data}
    form = CreateProblemSet(course=common_page_data['course'],
                            initial={'late_penalty':10,
                                    'assessment_type':'formative',
                                    'submissions_permitted':0,
                                    'resubmission_penalty':0,
                                    'due_date':(datetime.today()+timedelta(7)),
                                    'grace_period':(datetime.today()+timedelta(14)),
                                    'partial_credit_deadline':(datetime.today()+timedelta(21))
                                    })
    data['form'] = form
    data['course_prefix'] = course_prefix
    data['course_suffix'] = course_suffix
    return render_to_response('problemsets/create.html',
                              data,
                              context_instance=RequestContext(request))


@auth_is_course_admin_view_wrapper
def edit_form(request, course_prefix, course_suffix, pset_slug):
    try:
        common_page_data = get_common_page_data(request, course_prefix, course_suffix)
    except:
        raise Http404
    pset = ProblemSet.objects.get(course=common_page_data['course'], slug=pset_slug)
    data = {'common_page_data': common_page_data}
    form = CreateProblemSet(course=common_page_data['course'], instance=pset)
    data['form'] = form
    data['pset'] = pset
    data['course_prefix'] = course_prefix
    data['course_suffix'] = course_suffix
    return render_to_response('problemsets/edit.html', data, context_instance=RequestContext(request))

@require_POST
@auth_is_course_admin_view_wrapper
def create_action(request):
    course_prefix = request.POST.get("course_prefix")
    course_suffix = request.POST.get("course_suffix")
    common_page_data = get_common_page_data(request, course_prefix, course_suffix)
    data = {'common_page_data': common_page_data, 'course_prefix': course_prefix, 'course_suffix': course_suffix}
    
    if request.method == 'POST':
        pset = ProblemSet(course = common_page_data['course'])
        form = CreateProblemSet(request.POST, request.FILES, course=common_page_data['course'], instance=pset)
        if form.is_valid():
            new_pset = form.save(commit=False)
            new_pset.course = common_page_data['course']
            new_pset.mode = 'draft'
            new_pset.handle = course_prefix + "--" + course_suffix
            new_pset.path = "/"+request.POST['course_prefix']+"/"+request.POST['course_suffix']+"/problemsets/"+new_pset.slug+"/load_problem_set"

            new_pset.save()
            section = new_pset.section
            new_pset.index = section.getNextIndex()
            new_pset.save()
            new_pset.create_ready_instance()
            return HttpResponseRedirect(reverse('problemsets.views.manage_exercises', args=(request.POST['course_prefix'], request.POST['course_suffix'], new_pset.slug,)))

    else:
        form = CreateProblemSet(course=common_page_data['course'])
    data['form'] = form
    return render_to_response('problemsets/create.html', data, context_instance=RequestContext(request))

@require_POST
@auth_is_course_admin_view_wrapper
def edit_action(request):
    course_prefix = request.POST.get("course_prefix")
    course_suffix = request.POST.get("course_suffix")
    common_page_data = get_common_page_data(request, course_prefix, course_suffix)
    data = {'common_page_data': common_page_data, 'course_prefix': course_prefix, 'course_suffix': course_suffix}
    pset_id = request.POST.get("pset_id")

    if not common_page_data['is_course_admin']:
        return redirect('courses.views.main', course_prefix, course_suffix)

    if request.method == 'POST':
        pset = ProblemSet.objects.get(id=pset_id)

        action = request.POST['action']
        if action == "Reset to Ready":
            pset.revert()
            form = CreateProblemSet(course=common_page_data['course'], instance=pset)
        else:
            form = CreateProblemSet(request.POST, course=common_page_data['course'], instance=pset)
            if form.is_valid():
                form.save()
                pset.path = "/"+course_prefix+"/"+course_suffix+"/problemsets/"+pset.slug+"/load_problem_set"
                pset.save()
                if action == "Save and Set as Ready":
                    pset.commit()

                #Make sure slug is same for draft and ready versions
                if pset.slug != pset.image.slug:
                    pset.image.slug = pset.slug
                    pset.image.path = pset.path
                    pset.image.save()
                return HttpResponseRedirect(reverse('problemsets.views.list', args=(course_prefix, course_suffix)))

    data['form'] = form
    data['pset'] = pset
    return render(request, 'problemsets/edit.html', data)

@auth_is_course_admin_view_wrapper
def manage_exercises(request, course_prefix, course_suffix, pset_slug):
    #Get all necessary information about the problemset
    
    common_page_data = request.common_page_data
    
    data = {'common_page_data': common_page_data}
    form = ManageExercisesForm(initial={'course':common_page_data['course'].id})
    pset = ProblemSet.objects.getByCourse(common_page_data['course']).get(slug=pset_slug)
    psetToExs = ProblemSetToExercise.objects.getByProblemset(pset).select_related('exercise', 'problemSet')
    used_exercises = []
    problemset_taken = False
    if ProblemActivity.objects.filter(problemset_to_exercise__problemSet=pset.image).exists():
        problemset_taken = True
    #Get the list of exercises currently in this problem set
    for psetToEx in psetToExs:
        used_exercises.append(psetToEx.exercise.id)
    #Get all the exercises in the course but not in this problem set to list in add from existing
    #Q objects allow queryset filters to be ORed together
    exercises = Exercise.objects.all().filter(Q(problemSet__course=common_page_data['course'])|Q(video__course=common_page_data['course'])).exclude(id__in=used_exercises).distinct()

    #Form processing action if form was submitted
    if request.method == 'POST':
        form = ManageExercisesForm(request.POST, request.FILES)
        if form.is_valid():
            pset = ProblemSet.objects.get(id=request.POST['pset_id'])
            file_content = request.FILES['file']
            file_name = file_content.name

            exercise = Exercise()
            exercise.handle = request.POST['course_prefix'] + '--' + request.POST['course_suffix']
            exercise.fileName = file_name
            exercise.file.save(file_name, file_content)
            exercise.save()

            index = ProblemSetToExercise.objects.getByProblemset(pset).count()
            psetToEx = ProblemSetToExercise(problemSet=pset, exercise=exercise, number=index, is_deleted=0, mode='draft')
            psetToEx.save()
            return HttpResponseRedirect(reverse('problemsets.views.manage_exercises', args=(request.POST['course_prefix'], request.POST['course_suffix'], pset.slug,)))

    #If form was not submitted then the form should be displayed or if there were errors the page needs to be rendered again
    data['form'] = form
    data['course_prefix'] = course_prefix
    data['course_suffix'] = course_suffix
    data['pset'] = pset
    data['psetToExs'] = psetToExs
    data['problemset_taken'] = problemset_taken
    data['exercises'] = exercises
    return render_to_response('problemsets/manage_exercises.html', data, context_instance=RequestContext(request))

@require_POST
@auth_is_course_admin_view_wrapper
def add_existing_exercises(request):
    pset = ProblemSet.objects.get(id=request.POST['pset_id'])
    exercise_ids = request.POST.getlist('exercise')
    exercises = Exercise.objects.filter(id__in=exercise_ids)
    for exercise in exercises:
        psetToEx = ProblemSetToExercise(problemSet=pset, exercise=exercise, number=ProblemSetToExercise.objects.getByProblemset(pset).count(), is_deleted=0, mode='draft')
        psetToEx.save()
    return HttpResponseRedirect(reverse('problemsets.views.manage_exercises', args=(request.POST['course_prefix'], request.POST['course_suffix'], pset.slug,)))

@require_POST
@auth_is_course_admin_view_wrapper
def delete_exercise(request):
    toDelete = ProblemSetToExercise.objects.get(id=request.POST['exercise_id'])
    toDelete.delete()
    toDelete.save()
    pset = toDelete.problemSet
    psetToExs = ProblemSetToExercise.objects.getByProblemset(pset)
    #Renumber exercise relationships
    index = 0
    for psetToEx in psetToExs:
        psetToEx.number = index
        psetToEx.save()
        index += 1
    return HttpResponseRedirect(reverse('problemsets.views.manage_exercises', args=(request.POST['course_prefix'], request.POST['course_suffix'], pset.slug,)))

@require_POST
@auth_is_course_admin_view_wrapper
def save_exercises(request):
    #Function should only be accessed from submitting a form
    if request.method != 'POST':
        return redirect(request.META['HTTP_REFERER'])

    course_prefix = request.POST['course_prefix']
    course_suffix = request.POST['course_suffix']
    common_page_data = get_common_page_data(request, course_prefix, course_suffix)
    pset = ProblemSet.objects.get(id=request.POST['pset_id'])
    action = request.POST['action']
    if action == 'Reset to Ready':
        pset.revert()
        return HttpResponseRedirect(reverse('problemsets.views.manage_exercises', args=(request.POST['course_prefix'], request.POST['course_suffix'], pset.slug,)))
    else:
        psetToExs = ProblemSetToExercise.objects.getByProblemset(pset)
        for n in range(0,psetToExs.count()):
            listName = "exercise_order[" + str(n) + "]"
            psetToExs[n].number = request.POST[listName]
            psetToExs[n].save()
        if action == 'Save and Set as Ready':
            pset.commit()
        return HttpResponseRedirect(reverse('problemsets.views.list', args=(request.POST['course_prefix'], request.POST['course_suffix'])))


@auth_view_wrapper
def read_exercise(request, course_prefix, course_suffix, exercise_name):
    try:
        common_page_data = get_common_page_data(request, course_prefix, course_suffix)
    except:
        raise Http404

    
    try:
        exercise = Exercise.objects.distinct().get(problemSet__course=common_page_data["course"], fileName=exercise_name)
    except Exercise.DoesNotExist:
        exercise = Exercise.objects.distinct().get(video__course=common_page_data["course"], fileName=exercise_name)
    # return the contents of the file as an HTTP response.  Trust that it's there.
    #
    # TODO: put exception handling around this, figure out how to handle S3 errors
    # (file not there...)
    return HttpResponse(exercise.file.file)


@auth_view_wrapper
def load_problem_set(request, course_prefix, course_suffix, pset_slug):
    try:
        common_page_data = get_common_page_data(request, course_prefix, course_suffix)
    except:
        raise Http404
    pset = ProblemSet.objects.get(course=common_page_data['course'], slug=pset_slug)
    psetToExs = ProblemSetToExercise.objects.getByProblemset(pset).select_related('exercise', 'problemSet')
    file_names = []
    for psetToEx in psetToExs:
        #Remove the .html from the end of the file name
        file_names.append(psetToEx.exercise.fileName[:-5])
    return render_to_response('problemsets/load_problem_set.html',{'file_names': file_names, 'assessment_type': pset.assessment_type},context_instance=RequestContext(request))
