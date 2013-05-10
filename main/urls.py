from django.conf.urls.defaults import patterns, include, url
from django.views.generic.simple import redirect_to
from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.utils.translation import ugettext_lazy as _
from rest import views

import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()


# ---ACUA Custom URL's----

#These URLs contain translatable strings
urlpatterns = i18n_patterns('',
	
    # Webinars
    url(_(r'^(?P<course_prefix>[a-zA-Z0-9_-]+)/(?P<course_suffix>[a-zA-Z0-9_-]+)/webinar/?$'), 'courses.webinar.views.view'),
    url(_(r'^courses/webinar/get_recordings/?'), 'courses.webinar.views.get_recordings'),
    url(_(r'^courses/webinar/get_meetings/?'), 'courses.webinar.views.get_meetings'),

    url(_(r'^courses/webinar/start_meeting/?'), 'courses.webinar.actions.start_meeting'),
    url(_(r'^courses/webinar/join_meeting/?'), 'courses.webinar.actions.join_meeting'),
    
    # Google groups
    url(_(r'^(?P<course_prefix>[a-zA-Z0-9_-]+)/(?P<course_suffix>[a-zA-Z0-9_-]+)/google-groups/?$'), 'courses.google_groups.views.view'),
    url(_(r'^(?P<course_prefix>[a-zA-Z0-9_-]+)/(?P<course_suffix>[a-zA-Z0-9_-]+)/google-groups/update?$'), 'courses.google_groups.actions.update'),
    
    # SMF (Simple Machine Forum)
    url(_(r'^(?P<course_prefix>[a-zA-Z0-9_-]+)/(?P<course_suffix>[a-zA-Z0-9_-]+)/smf/?$'), 'courses.smf.views.view'),
)

urlpatterns += patterns('',

    # Health check endpoint.  Used by AWS load balancer.  Want something stable that
    # won't be redirected or change
    url(r'^_health$', 'c2g.views.healthcheck'),
                       
    # Testing the error pages (404 and 500)
    url(r'^_throw500$', 'c2g.views.throw500'),
    url(r'^_throw404$', 'c2g.views.throw404'),

    # REST Class2Go API
    url(r'^rest/login', 'rest.views.rest_login'),
    url(r'^rest/problemactivities', views.ProblemActivities.as_view()),
    url(r'^rest/courses', views.CourseList.as_view()),
    url(r'^rest/announcements', views.AnnouncementList.as_view()),                                              
    url(r'^rest/psets', views.ProblemSetList.as_view()),                                              
    url(r'^rest/psettoexercise', views.ProblemSetToExerciseList.as_view()),  
    url(r'^rest/exercise', views.ExerciseList.as_view()),  
    url(r'^rest/contentsection', views.ContentSectionList.as_view()),  
    url(r'^rest/videotoexercise', views.VideoToExerciseList.as_view()),  
    url(r'^rest/videoactivities', views.VideoActivities.as_view()),
    url(r'^rest/files', views.FilesList.as_view()),                         
    url(r'^rest/video', views.VideoList.as_view()),  
    url(r'^rest/exams', views.ExamList.as_view()),
    url(r'^rest/examrecords', views.ExamRecordList.as_view()),
    url(r'^rest/examscores', views.ExamScoreList.as_view()),
    url(r'^rest/examscorefields', views.ExamScoreFieldList.as_view()),
                    
    #Testing messages
    url(r'^_test_messages$', 'c2g.views.test_messages'),

    url(r'^test_xml$', 'courses.exams.views.show_test_xml'),
    url(r'^hiring/?$', 'courses.landing.views.hiring'),

    url(r'^maint$', 'c2g.views.maintenance'),

    # Get server epoch
    url(r'^server_epoch/?$', 'c2g.views.server_epoch'),
    
    # Get server time
    url(r'^server_time/?$', 'c2g.views.server_time'),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^c2g_admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^c2g_admin/?', include(admin.site.urls)),  
    
    # Landing Page
    url(r'^/?$', 'courses.landing.views.landing'),
)

#These URLs contain i18n/translatable strings
urlpatterns += i18n_patterns('',

    url(_(r'^honor_code$'), 'c2g.views.hc'),
    url(_(r'^terms_of_service$'), 'c2g.views.tos'),
    url(_(r'^privacy$'), 'c2g.views.privacy'),
    url(_(r'^contactus$'), 'c2g.views.contactus'),
    url(_(r'^faq$'), 'c2g.views.faq'),

    url(_(r'^(?P<course_prefix>[a-zA-Z0-9_-]+)/(?P<course_suffix>[a-zA-Z0-9_-]+)/unenroll/?$'), 'courses.views.unenroll'),    
    
    # general exam stuff--These endpoints are hidden from student users and do not have to be named (i.e. aliased for each exam subtype)
    url(_(r'^exams/parse_markdown/?$'), 'courses.exams.views.parse_markdown', name='parse_markdown'),
    url(_(r'^(?P<course_prefix>[a-zA-Z0-9_-]+)/(?P<course_suffix>[a-zA-Z0-9_-]+)/exams/create/?$'), 'courses.exams.views.create_exam'),
    url(_(r'^(?P<course_prefix>[a-zA-Z0-9_-]+)/(?P<course_suffix>[a-zA-Z0-9_-]+)/exams/save/?$'), 'courses.exams.views.save_exam_ajax'),
    url(_(r'^delete_exam/?'), 'courses.exams.actions.delete_exam'),
    url(_(r'^(?P<course_prefix>[a-zA-Z0-9_-]+)/(?P<course_suffix>[a-zA-Z0-9_-]+)/exams/check_metadata_xml/?$'), 'courses.exams.views.check_metadata_xml'),
    url(_(r'^(?P<course_prefix>[a-zA-Z0-9_-]+)/(?P<course_suffix>[a-zA-Z0-9_-]+)/exams/(?P<exam_slug>[a-zA-Z0-9_-]+)/edit/?$'), 'courses.exams.views.edit_exam'),
    url(_(r'^(?P<course_prefix>[a-zA-Z0-9_-]+)/(?P<course_suffix>[a-zA-Z0-9_-]+)/exams/(?P<exam_slug>[a-zA-Z0-9_-]+)/save/?$'), 'courses.exams.views.edit_exam_ajax_wrapper', name='save_edited_exam'),
    url(_(r'^(?P<course_prefix>[a-zA-Z0-9_-]+)/(?P<course_suffix>[a-zA-Z0-9_-]+)/exams/(?P<exam_slug>[a-zA-Z0-9_-]+)/submit/?$'), 'courses.exams.views.collect_data'),
    url(_(r'^(?P<course_prefix>[a-zA-Z0-9_-]+)/(?P<course_suffix>[a-zA-Z0-9_-]+)/exams/(?P<exam_slug>[a-zA-Z0-9_-]+)/all_submissions_to_grade/?$'), 'courses.exams.views.view_submissions_to_grade'),
    url(_(r'^(?P<course_prefix>[a-zA-Z0-9_-]+)/(?P<course_suffix>[a-zA-Z0-9_-]+)/exams/(?P<exam_slug>[a-zA-Z0-9_-]+)/post_csv_grades/?$'), 'courses.exams.views.post_csv_grades'),
    url(_(r'^(?P<course_prefix>[a-zA-Z0-9_-]+)/(?P<course_suffix>[a-zA-Z0-9_-]+)/exams/(?P<exam_slug>[a-zA-Z0-9_-]+)/get_csv_grades/?$'), 'courses.exams.views.view_csv_grades'),
    url(_(r'^(?P<course_prefix>[a-zA-Z0-9_-]+)/(?P<course_suffix>[a-zA-Z0-9_-]+)/exams/(?P<exam_slug>[a-zA-Z0-9_-]+)/save_student_progress/?$'), 'courses.exams.views.student_save_progress'),
    url(_(r'^(?P<course_prefix>[a-zA-Z0-9_-]+)/(?P<course_suffix>[a-zA-Z0-9_-]+)/exams/(?P<exam_slug>[a-zA-Z0-9_-]+)/confirm/?$'), 'courses.exams.views.confirm', name='confirm_exam_start'),


    #The rest of these URLs end up in the location bar of student users.  We should alias them for each exam subtype so that students do not get
    #confused.  Would love to make this DRY, because it's very repetitive, but I don't know how.
                      
    #Exam subtype of exam
    #All subtypes use the same views in this list, so any reversing should be done using the name, i.e. 'exam_list', otherwise it
    #will not return the right URL for the right type
    url(_(r'^(?P<course_prefix>[a-zA-Z0-9_-]+)/(?P<course_suffix>[a-zA-Z0-9_-]+)/exams/?$'), 'courses.exams.views.listAll', {'show_types':['exam',]}, name='exam_list'),
    url(_(r'^(?P<course_prefix>[a-zA-Z0-9_-]+)/(?P<course_suffix>[a-zA-Z0-9_-]+)/exams/(?P<exam_slug>[a-zA-Z0-9_-]+)/?$'), 'courses.exams.views.show_exam', name='exam_show'),
    url(_(r'^(?P<course_prefix>[a-zA-Z0-9_-]+)/(?P<course_suffix>[a-zA-Z0-9_-]+)/exams/(?P<exam_slug>[a-zA-Z0-9_-]+)/snapshot/?$'), 'courses.exams.views.show_populated_exam', name='exam_populated'),
    url(_(r'^(?P<course_prefix>[a-zA-Z0-9_-]+)/(?P<course_suffix>[a-zA-Z0-9_-]+)/exams/(?P<exam_slug>[a-zA-Z0-9_-]+)/graded/?$'), 'courses.exams.views.show_graded_exam', name='exam_graded'),
    url(_(r'^(?P<course_prefix>[a-zA-Z0-9_-]+)/(?P<course_suffix>[a-zA-Z0-9_-]+)/exams/(?P<exam_slug>[a-zA-Z0-9_-]+)/view_submissions/?$'), 'courses.exams.views.view_my_submissions', name='exam_my_submissions'),
    url(_(r'^(?P<course_prefix>[a-zA-Z0-9_-]+)/(?P<course_suffix>[a-zA-Z0-9_-]+)/exams/(?P<exam_slug>[a-zA-Z0-9_-]+)/record/(?P<record_id>[0-9]+)/?$'), 'courses.exams.views.show_graded_record', name='exam_record'),
    url(_(r'^(?P<course_prefix>[a-zA-Z0-9_-]+)/(?P<course_suffix>[a-zA-Z0-9_-]+)/exams/(?P<exam_slug>[a-zA-Z0-9_-]+)/feedback/?$'), 'courses.exams.views.exam_feedback'),

    #problemset subtype of exam
    #This and the exams list use the same view, so any reversing should be done using the name, i.e. 'survey_list', otherwise it
    #will be always return /exams/
    url(_(r'^(?P<course_prefix>[a-zA-Z0-9_-]+)/(?P<course_suffix>[a-zA-Z0-9_-]+)/problemsets/?$'), 'courses.exams.views.listAll', {'show_types':['problemset',]}, name='problemset_list'),
    url(_(r'^(?P<course_prefix>[a-zA-Z0-9_-]+)/(?P<course_suffix>[a-zA-Z0-9_-]+)/problemsets/(?P<exam_slug>[a-zA-Z0-9_-]+)/?$'), 'courses.exams.views.show_exam', name='problemset_show'),
    url(_(r'^(?P<course_prefix>[a-zA-Z0-9_-]+)/(?P<course_suffix>[a-zA-Z0-9_-]+)/problemsets/(?P<exam_slug>[a-zA-Z0-9_-]+)/snapshot/?$'), 'courses.exams.views.show_populated_exam', name='problemset_populated'),
    url(_(r'^(?P<course_prefix>[a-zA-Z0-9_-]+)/(?P<course_suffix>[a-zA-Z0-9_-]+)/problemsets/(?P<exam_slug>[a-zA-Z0-9_-]+)/graded/?$'), 'courses.exams.views.show_graded_exam', name='problemset_graded'),
    url(_(r'^(?P<course_prefix>[a-zA-Z0-9_-]+)/(?P<course_suffix>[a-zA-Z0-9_-]+)/problemsets/(?P<exam_slug>[a-zA-Z0-9_-]+)/view_submissions/?$'), 'courses.exams.views.view_my_submissions', name='problemset_my_submissions'),
    url(_(r'^(?P<course_prefix>[a-zA-Z0-9_-]+)/(?P<course_suffix>[a-zA-Z0-9_-]+)/problemsets/(?P<exam_slug>[a-zA-Z0-9_-]+)/record/(?P<record_id>[0-9]+)/?$'), 'courses.exams.views.show_graded_record', name='problemset_record'),

    
    #survey subtype of exam
    #This and the exams list use the same view, so any reversing should be done using the name, i.e. 'survey_list', otherwise it
    #will be always return /exams/
    url(_(r'^(?P<course_prefix>[a-zA-Z0-9_-]+)/(?P<course_suffix>[a-zA-Z0-9_-]+)/surveys/?$'), 'courses.exams.views.listAll', {'show_types':['survey',]}, name='survey_list'),
    url(_(r'^(?P<course_prefix>[a-zA-Z0-9_-]+)/(?P<course_suffix>[a-zA-Z0-9_-]+)/surveys/(?P<exam_slug>[a-zA-Z0-9_-]+)/?$'), 'courses.exams.views.show_exam', name='survey_show'),
    url(_(r'^(?P<course_prefix>[a-zA-Z0-9_-]+)/(?P<course_suffix>[a-zA-Z0-9_-]+)/surveys/(?P<exam_slug>[a-zA-Z0-9_-]+)/snapshot/?$'), 'courses.exams.views.show_populated_exam', name='survey_populated'),
    url(_(r'^(?P<course_prefix>[a-zA-Z0-9_-]+)/(?P<course_suffix>[a-zA-Z0-9_-]+)/surveys/(?P<exam_slug>[a-zA-Z0-9_-]+)/graded/?$'), 'courses.exams.views.show_graded_exam', name='surveys_graded'), #admittedly doesn't make sense, here for consistency
    url(_(r'^(?P<course_prefix>[a-zA-Z0-9_-]+)/(?P<course_suffix>[a-zA-Z0-9_-]+)/surveys/(?P<exam_slug>[a-zA-Z0-9_-]+)/view_submissions/?$'), 'courses.exams.views.view_my_submissions', name='survey_my_submissions'),
    url(_(r'^(?P<course_prefix>[a-zA-Z0-9_-]+)/(?P<course_suffix>[a-zA-Z0-9_-]+)/surveys/(?P<exam_slug>[a-zA-Z0-9_-]+)/record/(?P<record_id>[0-9]+)/?$'), 'courses.exams.views.show_graded_record', name='survey_record'),

    #interactive_exercise subtype of exam
    url(_(r'^(?P<course_prefix>[a-zA-Z0-9_-]+)/(?P<course_suffix>[a-zA-Z0-9_-]+)/interactive_exercises/?$'), 'courses.exams.views.listAll', {'show_types':['interactive_exercise',]}, name='interactive_exercise_list'),
    url(_(r'^(?P<course_prefix>[a-zA-Z0-9_-]+)/(?P<course_suffix>[a-zA-Z0-9_-]+)/interactive_exercises/(?P<exam_slug>[a-zA-Z0-9_-]+)/?$'), 'courses.exams.views.show_exam', name='interactive_exercise_show'),
    url(_(r'^(?P<course_prefix>[a-zA-Z0-9_-]+)/(?P<course_suffix>[a-zA-Z0-9_-]+)/interactive_exercises/(?P<exam_slug>[a-zA-Z0-9_-]+)/snapshot/?$'), 'courses.exams.views.show_populated_exam', name='interactive_exercise_populated'),
    url(_(r'^(?P<course_prefix>[a-zA-Z0-9_-]+)/(?P<course_suffix>[a-zA-Z0-9_-]+)/interactive_exercises/(?P<exam_slug>[a-zA-Z0-9_-]+)/graded/?$'), 'courses.exams.views.show_graded_exam', name='interactive_exercise_graded'),
    url(_(r'^(?P<course_prefix>[a-zA-Z0-9_-]+)/(?P<course_suffix>[a-zA-Z0-9_-]+)/interactive_exercises/(?P<exam_slug>[a-zA-Z0-9_-]+)/view_submissions/?$'), 'courses.exams.views.view_my_submissions', name='interactive_exercise_my_submissions'),
    url(_(r'^(?P<course_prefix>[a-zA-Z0-9_-]+)/(?P<course_suffix>[a-zA-Z0-9_-]+)/interactive_exercises/(?P<exam_slug>[a-zA-Z0-9_-]+)/record/(?P<record_id>[0-9]+)/?$'), 'courses.exams.views.show_graded_record', name='interactive_exercise_record'),

    #emailoptout
    url(_(r'^email_optout/(?P<code>[a-zA-Z0-9]+)/?$'), 'courses.email_members.views.optout', name='maillist_optout'),
    
    # Commented out the following 2 urls since point to a signup page which is
    # no longer required.
#    url(_(r'^courses/?$'), 'c2g.views.home', name='c2g_home'),
#    url(_(r'^courses/signup/?$'), 'courses.actions.signup'),

#    url(_(r'^class2go/'), include('class2go.foo.urls')),
   
    url(_(r'^default-login/?$'), 'accounts.views.default_login', name='default_login'),
    #shibboleth login
    url(_(r'^shib-login/?$'), 'accounts.views.shib_login', name='shib_login'),
                       
    
    #impersonate
    url(_(r'^impersonate/(?P<username>[\w.@+-]+)/?$'), 'accounts.views.impersonate', name='impersonate'),
                       
    #for data collection
    url(_(r'^videos/save/'), 'courses.videos.actions.save_video_progress'),
    url(_(r'^videos/record_download/'), 'courses.videos.actions.record_download'),
    url(_(r'^problemsets/attempt/(?P<problemId>\d+)/?$'), 'problemsets.views.attempt'),
    url(_(r'^problemsets/attempt_protect/(?P<problemId>\d+)/?$'), 'problemsets.views.attempt_protect'),

    # accounts app for user management
    url(_(r'^accounts/profile/?$'), 'accounts.views.profile', name='accounts_profile'),
    url(_(r'^accounts/profile/edit/?'), 'accounts.views.edit'),
    url(_(r'^accounts/profile/save_edits/?'), 'accounts.views.save_edits'),
    url(_(r'^accounts/profile/save_piazza_opts/?$'), 'accounts.views.save_piazza_opts'),

    url(_(r'^accounts/'), include('registration.backends.simple.urls')),

    #Course signup for students
    url(_(r'^(?P<course_prefix>[a-zA-Z0-9_-]+)/(?P<course_suffix>[a-zA-Z0-9_-]+)/signup/?$'), 'courses.actions.signup_with_course'),


    url(_(r'^courses/new/?'), 'courses.admin_views.new'),

    url(_(r'^(?P<course_prefix>[a-zA-Z0-9_-]+)/(?P<course_suffix>[a-zA-Z0-9_-]+)/?$'),
        'courses.views.main',
        name='course_main'),
    url(_(r'^(?P<course_prefix>[a-zA-Z0-9_-]+)/(?P<course_suffix>[a-zA-Z0-9_-]+)/materials/?$'),
        'courses.views.course_materials',
        name='course_materials'),
    url(_(r'^(?P<course_prefix>[a-zA-Z0-9_-]+)/(?P<course_suffix>[a-zA-Z0-9_-]+)/materials/(?P<section_id>[0-9]+)/?$'),
        'courses.views.course_materials',
        name='course_materials_by_section'),
    url(_(r'^(?P<course_prefix>[a-zA-Z0-9_-]+)/(?P<course_suffix>[a-zA-Z0-9_-]+)/admin/?'), 'courses.admin_views.admin'),
                       
                       
    url(_(r'^(?P<course_prefix>[a-zA-Z0-9_-]+)/(?P<course_suffix>[a-zA-Z0-9_-]+)/leftnav/?$'), 'courses.views.leftnav'),
    url(_(r'^(?P<course_prefix>[a-zA-Z0-9_-]+)/(?P<course_suffix>[a-zA-Z0-9_-]+)/rightnav/?$'), 'courses.views.rightnav'),

    url(_(r'^switch_mode'), 'courses.actions.switch_mode'),
    url(_(r'^add_section'), 'courses.actions.add_section'),

    url(_(r'^commit/?'), 'courses.actions.commit'),
    url(_(r'^revert/?$'), 'courses.actions.revert'),
    url(_(r'^change_live_datetime/?'), 'courses.actions.change_live_datetime'),

    url(_(r'^(?P<course_prefix>[a-zA-Z0-9_-]+)/(?P<course_suffix>[a-zA-Z0-9_-]+)/(?P<file_type>files|videos|problemsets)/check_filename/?'), 'courses.actions.check_filename'),

    # Additional Pages
    url(_(r'^(?P<course_prefix>[a-zA-Z0-9_-]+)/(?P<course_suffix>[a-zA-Z0-9_-]+)/pages/(?P<slug>[a-zA-Z0-9_-]+)/?$'), 'courses.additional_pages.views.main'),
    url(_(r'^(?P<course_prefix>[a-zA-Z0-9_-]+)/(?P<course_suffix>[a-zA-Z0-9_-]+)/manage_nav_menu/?$'), 'courses.additional_pages.views.manage_nav_menu'),
    url(_(r'^(?P<course_prefix>[a-zA-Z0-9_-]+)/(?P<course_suffix>[a-zA-Z0-9_-]+)/add_section_page/?$'), 'courses.additional_pages.views.add_section_page'),
    url(_(r'^delete_page'), 'courses.additional_pages.actions.delete'),
    url(_(r'^save_page'), 'courses.additional_pages.actions.save'),
    url(_(r'^save_order'), 'courses.additional_pages.actions.save_order'),
    url(_(r'^add_page'), 'courses.additional_pages.actions.add'),

    # Announcements
    url(_(r'^(?P<course_prefix>[a-zA-Z0-9_-]+)/(?P<course_suffix>[a-zA-Z0-9_-]+)/announcements/?$'), 'courses.announcements.views.list'),
    url(_(r'^(?P<course_prefix>[a-zA-Z0-9_-]+)/(?P<course_suffix>[a-zA-Z0-9_-]+)/announcements/admin/?$'), 'courses.announcements.views.admin'),
    url(_(r'^(?P<course_prefix>[a-zA-Z0-9_-]+)/(?P<course_suffix>[a-zA-Z0-9_-]+)/announcements/(?P<announcement_id>[0-9]+)/edit/?$'), 'courses.announcements.views.edit'),
    url(_(r'^save_announcement_order$'), 'courses.announcements.actions.save_announcement_order'),
    url(_(r'^save_announcement$'), 'courses.announcements.actions.save_announcement'),
    url(_(r'^add_announcement$'), 'courses.announcements.actions.add_announcement'),
    url(_(r'^delete_announcement$'), 'courses.announcements.actions.delete_announcement'),
    url(_(r'^email_announcement$'), 'courses.announcements.actions.email_announcement'),

    # Forums
    url(_(r'^(?P<course_prefix>[a-zA-Z0-9_-]+)/(?P<course_suffix>[a-zA-Z0-9_-]+)/forums/?$'), 'courses.forums.views.view'),

    
    # Sections
    url(_(r'^(?P<course_prefix>[a-zA-Z0-9_-]+)/(?P<course_suffix>[a-zA-Z0-9_-]+)/sections/reorder/?$'), 'courses.content_sections.views.reorder'),
    url(_(r'^(?P<course_prefix>[a-zA-Z0-9_-]+)/(?P<course_suffix>[a-zA-Z0-9_-]+)/sections/rename/(?P<section_id>[0-9]+)/?$'), 'courses.content_sections.views.rename'),
    url(_(r'^rename$'), 'courses.content_sections.actions.rename'),
    url(_(r'^save_content_section_order$'), 'courses.content_sections.actions.save_order'),
    url(_(r'^delete_content_section$'), 'courses.content_sections.actions.delete_content_section'),
    url(_(r'^save_content_section_content_order$'), 'courses.content_sections.actions.save_content_order'),
    url(_(r'^content_section/get_children/(?P<section_id>[0-9]+)/?$'), 'courses.content_sections.actions.get_children'),
    url(_(r'^content_section/get_children_as_contentgroup_parents/(?P<section_id>[0-9]+)/?$'), 'courses.content_sections.actions.get_children_as_contentgroup_parents'),

    # Videos
    url(_(r'^(?P<course_prefix>[a-zA-Z0-9_-]+)/(?P<course_suffix>[a-zA-Z0-9_-]+)/videos/?$'),
        'courses.videos.views.list',
        name='course_video_list'),
    url(_(r'^(?P<course_prefix>[a-zA-Z0-9_-]+)/(?P<course_suffix>[a-zA-Z0-9_-]+)/videos/upload$'), 'courses.videos.views.upload'),
    url(_(r'^switch_video_quiz_mode'), 'courses.videos.actions.switch_quiz_mode'),
    url(_(r'^(?P<course_prefix>[a-zA-Z0-9_-]+)/(?P<course_suffix>[a-zA-Z0-9_-]+)/videos/(?P<slug>[a-zA-Z0-9_-]+)/?$'),
        'courses.videos.views.view',
        name='course_video_view'),
    url(_(r'^(?P<course_prefix>[a-zA-Z0-9_-]+)/(?P<course_suffix>[a-zA-Z0-9_-]+)/videos/(?P<slug>[a-zA-Z0-9_-]+)/edit/?$'), 'courses.videos.views.edit'),
    url(_(r'^add_video/?$'), 'courses.videos.actions.add_video'),
    url(_(r'^(?P<course_prefix>[a-zA-Z0-9_-]+)/(?P<course_suffix>[a-zA-Z0-9_-]+)/videos/(?P<slug>[a-zA-Z0-9_-]+)/edit_video/?$'), 'courses.videos.actions.edit_video'),
    url(_(r'^(?P<course_prefix>[a-zA-Z0-9_-]+)/(?P<course_suffix>[a-zA-Z0-9_-]+)/videos/(?P<slug>[a-zA-Z0-9_-]+)/reset_video/?$'), 'courses.videos.actions.reset_video'),
    url(_(r'^delete_video/?$'), 'courses.videos.actions.delete_video'),
    url(_(r'^upload_video/?'), 'courses.videos.actions.upload'), ####ADDED BY KEVIN
    url(_(r'^oauth2callback/?'), 'courses.videos.actions.oauth'),
    url(_(r'^delete_video_exercise/?$'), 'courses.videos.views.delete_exercise'),
    url(_(r'^(?P<course_prefix>[a-zA-Z0-9_-]+)/(?P<course_suffix>[a-zA-Z0-9_-]+)/videos/(?P<video_id>[a-zA-Z0-9_-]+)/load_video_problem_set/?$'),
        'courses.videos.views.load_video_problem_set',
        name='course_video_pset'),
 
 
    # Video Exercises
    url(_(r'^(?P<course_prefix>[a-zA-Z0-9_-]+)/(?P<course_suffix>[a-zA-Z0-9_-]+)/video_exercises/(?P<video_id>[a-zA-Z0-9_-]+)/?$'), 'courses.video_exercises.views.view'),
    url(_(r'^(?P<course_prefix>[a-zA-Z0-9_-]+)/(?P<course_suffix>[a-zA-Z0-9_-]+)/videos/(?P<video_slug>[a-zA-Z0-9_-]+)/manage_exercises?$'), 'courses.videos.views.manage_exercises'),
    url(_(r'^add_video_exercise/?$'), 'courses.videos.views.add_exercise'),
    url(_(r'^add_existing_video_exercises/?$'), 'courses.videos.views.add_existing_exercises'),
    url(_(r'^save_video_exercises/?'), 'courses.videos.views.save_exercises'),
    url(_(r'^get_video_exercises/?$'), 'courses.videos.views.get_video_exercises'),

    #Problem Sets
    #These commented out ones are above
    url(_(r'^(?P<course_prefix>[a-zA-Z0-9_-]+)/(?P<course_suffix>[a-zA-Z0-9_-]+)/problemsets_old/?$'), 'problemsets.views.listAll'),
    url(_(r'^(?P<course_prefix>[a-zA-Z0-9_-]+)/(?P<course_suffix>[a-zA-Z0-9_-]+)/problemsets_old/(?P<pset_slug>[a-zA-Z0-9_-]+)?$'), 'problemsets.views.show'),
    url(_(r'^(?P<course_prefix>[a-zA-Z0-9_-]+)/(?P<course_suffix>[a-zA-Z0-9_-]+)/createproblemset/?$'), 'problemsets.views.create_form'),
    url(_(r'^createproblemsetaction/?'), 'problemsets.views.create_action'),
    url(_(r'^(?P<course_prefix>[a-zA-Z0-9_-]+)/(?P<course_suffix>[a-zA-Z0-9_-]+)/problemsets/(?P<pset_slug>[a-zA-Z0-9_-]+)/edit/?$'), 'problemsets.views.edit_form'),
    url(_(r'^editproblemsetaction/?'), 'problemsets.views.edit_action'),
    url(_(r'^(?P<course_prefix>[a-zA-Z0-9_-]+)/(?P<course_suffix>[a-zA-Z0-9_-]+)/problemsets/(?P<pset_slug>[a-zA-Z0-9_-]+)/manage_exercises?$'), 'problemsets.views.manage_exercises'),
    url(_(r'^add_existing_problemset_exercises/?$'), 'problemsets.views.add_existing_exercises'),
    url(_(r'^save_problemset_exercises/?'), 'problemsets.views.save_exercises'),
    url(_(r'^delete_exercise/?'), 'problemsets.views.delete_exercise'),
    url(_(r'^delete_problemset/?'), 'problemsets.actions.delete_problemset'),

    url(_(r'^(?P<course_prefix>[a-zA-Z0-9_-]+)/(?P<course_suffix>[a-zA-Z0-9_-]+)/exercises/(?P<filename>.+)/edit/?$'), 'courses.exercises.views.edit'),
    url(_(r'^(?P<course_prefix>[a-zA-Z0-9_-]+)/(?P<course_suffix>[a-zA-Z0-9_-]+)/exercises/(?P<filename>.+)/save/?$'), 'courses.exercises.views.save'),

    url(_(r'^(?P<course_prefix>[a-zA-Z0-9_-]+)/(?P<course_suffix>[a-zA-Z0-9_-]+)/exercises/(?P<exercise_name>.+)$'), 'problemsets.views.read_exercise'),
    url(_(r'^(?P<course_prefix>[a-zA-Z0-9_-]+)/(?P<course_suffix>[a-zA-Z0-9_-]+)/problemsets/(?P<pset_slug>[a-zA-Z0-9_-]+)/load_problem_set?$'), 'problemsets.views.load_problem_set'),


    #Files
    url(_(r'^(?P<course_prefix>[a-zA-Z0-9_-]+)/(?P<course_suffix>[a-zA-Z0-9_-]+)/files/upload$'), 'courses.files.views.upload'),
    url(_(r'^(?P<course_prefix>[a-zA-Z0-9_-]+)/(?P<course_suffix>[a-zA-Z0-9_-]+)/files/edit/(?P<file_id>[0-9]+)/?$'), 'courses.files.views.edit'),
    url(_(r'^upload_file/?'), 'courses.files.actions.upload'),
    url(_(r'^edit_file/?'), 'courses.files.actions.edit'),
    url(_(r'^delete_file/?'), 'courses.files.actions.delete_file'),
                       
    #Content Sharing
    url(_(r'^(?P<course_prefix>[a-zA-Z0-9_-]+)/(?P<course_suffix>[a-zA-Z0-9_-]+)/copy_section/?$'), 'courses.content_sections.views.copy_content_form'),
    url(_(r'^(?P<course_prefix>[a-zA-Z0-9_-]+)/(?P<course_suffix>[a-zA-Z0-9_-]+)/copy_section/send/?$'), 'courses.content_sections.views.copy_content'),

    #Preview
    url(_(r'^(?P<course_prefix>[a-zA-Z0-9_-]+)/(?P<course_suffix>[a-zA-Z0-9_-]+)/preview/$'), 'courses.preview.views.preview'),
    url(_(r'^(?P<course_prefix>[a-zA-Z0-9_-]+)/(?P<course_suffix>[a-zA-Z0-9_-]+)/preview_reg/$'), 'courses.preview.views.preview_reg'),
    # url(_(r'^(?P<course_prefix>[a-zA-Z0-9_-]+)/(?P<course_suffix>[a-zA-Z0-9_-]+)/preview_login/$'), 'courses.preview.views.preview_login'),
    url(_(r'^(?P<course_prefix>[a-zA-Z0-9_-]+)/(?P<course_suffix>[a-zA-Z0-9_-]+)/preview_login/$'), 'accounts.views.default_preview_login'),
    #Email
    url(_(r'^(?P<course_prefix>[a-zA-Z0-9_-]+)/(?P<course_suffix>[a-zA-Z0-9_-]+)/email_members/$'), 'courses.email_members.views.email_members'),             
    
    #Reports
    url(_(r'^(?P<course_prefix>[a-zA-Z0-9_-]+)/(?P<course_suffix>[a-zA-Z0-9_-]+)/browse_reports/?$'), 'courses.reports.views.main'),
    url(_(r'^generate_report$'), 'courses.reports.views.generate_report'),
    url(_(r'^(?P<course_prefix>[a-zA-Z0-9_-]+)/(?P<course_suffix>[a-zA-Z0-9_-]+)/reports/(?P<report_subfolder>[a-zA-Z0-9_-]+)/(?P<report_name>.+)$'), 'courses.reports.views.download_report'),
    
    #In-line Reports
    url(_(r'^(?P<course_prefix>[a-zA-Z0-9_-]+)/(?P<course_suffix>[a-zA-Z0-9_-]+)/generate_in_line_report/?$'), 'courses.reports.views.generate_in_line_report'),
    url(_(r'^(?P<course_prefix>[a-zA-Z0-9_-]+)/(?P<course_suffix>[a-zA-Z0-9_-]+)/summary_report/(?P<exam_slug>[a-zA-Z0-9_-]+)/?$'), 'courses.reports.views.summary_report'),

    #Current course redirects THIS SHOULD PROBABLY ALWAYS BE THE LAST ITEM THAT HAS TO DO WITH COURSES
    url(_(r'^(?P<course_prefix>[a-zA-Z0-9_-]+)/?$'), 'courses.views.current_redirects'),

)


# when testing we get a warning about favicon, silence it by mapping to
# the location of the file
if settings.DEBUG and settings.SITE_NAME_SHORT:
    site=settings.SITE_NAME_SHORT.lower()
    urlpatterns += patterns('', 
        url(r'^favicon\.ico$', 'django.views.generic.simple.redirect_to', 
            {'url': settings.STATIC_URL+'graphics/core/%s-favicon.ico' % site})
    )
   
