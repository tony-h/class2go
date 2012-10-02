import logging
from celery import task
from courses.reports.generation.course_dashboard import *
from courses.reports.generation.course_quizzes import *
from courses.reports.generation.quiz_data import *
from settings import SERVER_EMAIL

from django.core.mail import EmailMessage

logger = logging.getLogger(__name__)

#@task()
def generate_and_email_reports(username, course_handle, requested_reports, email_title, email_message):
    # Generates the list of reports in requested_reports, and sends it to the staff of the given course.
    ready_course = Course.objects.get(handle=course_handle, mode='ready')
    logger.info(requested_reports[0]['type'])
    # Generate requested reports
    reports = []
    for rr in requested_reports:
        if rr['type'] == 'dashboard':
            logger.info("User %s requested to generate dashboard report for course %s." % (username, course_handle))
            report = gen_course_dashboard_report(ready_course, save_to_s3=True)
            if report:
                reports.append(report)
                logger.info("Dashboard report for course %s generated successfully for user %s." % (course_handle, username))
            else:
                logger.info("Failed to generate dashboard report for course %s for user %s." % (course_handle, username))
            
        elif rr['type'] == 'course_quizzes':
            logger.info("User %s requested to generate course quizzes report for course %s." % (username, course_handle))
            report = gen_course_quizzes_report(ready_course, save_to_s3=True)
            if report:
                reports.append(report)
                logger.info("Course quizzes report for course %s generated successfully for user %s." % (course_handle, username))
            else:
                logger.info("Failed to generate course quizzes report for course %s for user %s." % (course_handle, username))
                
        elif rr['type'] == 'problemset':
            if (not 'slug' in rr) or (not rr['slug']):
                logger.info("Missing slug -- Failed to generate problem set report")
            else:
                slug = rr['slug']
                logger.info("User %s requested to generate problemset report for course %s problemset slug %s." % (username, course_handle, slug))
                
                # If instructors ask for a report for a quiz that doesn't have a live instance, pass the draft instance instead. The report generators will handle this special case
                try:
                    quiz = ProblemSet.objects.get(course=ready_course, slug=slug)
                except ProblemSet.DoesNotExist:
                    quiz = ProblemSet.objects.get(course=ready_course.image, slug=slug)
                    
                report = gen_quiz_data_report(ready_course, quiz, save_to_s3=True)
                if report:
                    reports.append(report)
                    logger.info("Problemset report for course %s problemset %s generated successfully for user %s." % (course_handle, slug, username))
                else:
                    logger.info("Failed to generate problemset report for course %s problemset %s for user %s." % (course_handle, slug, username))
            
        elif rr['type'] == 'video':
            if (not 'slug' in rr) or (not rr['slug']):
                logger.info("Missing slug -- Failed to generate video report")
            else:
                slug = rr['slug']
                logger.info("User %s requested to generate video report for course %s video slug %s." % (username, course_handle, slug))
                # If instructors ask for a report for a quiz that doesn't have a live instance, pass the draft instance instead. The report generators will handle this special case
                try:
                    quiz = Video.objects.get(course=ready_course, slug=slug)
                except Video.DoesNotExist:
                    quiz = Video.objects.get(course=ready_course.image, slug=slug)
                    
                report = gen_quiz_data_report(ready_course, quiz, save_to_s3=True)
                if report:
                    reports.append(report)
                    logger.info("Video report for course %s video %s generated successfully for user %s." % (course_handle, slug, username))
                else:
                    logger.info("Failed to generate video report for course %s video %s for user %s." % (course_handle, slug, username))
            
    # Email Generated Reports
    staff_email = ready_course.contact
    if not staff_email:
        logger.info("Failed to email reports for course %s -- Missing course contact email" % (course_handle))
    else:
        if len(reports) == 0:
            logger.info("Giving up send reports email to %s, because no reports were generated." % staff_email)
            return
            
        email = EmailMessage(
            email_title, # Title
            email_message, # Message
            SERVER_EMAIL, # From
            [staff_email, 'c2g-dev@cs.stanford.edu'], # To
        )
        for report in reports:
            email.attach(report['name'], report['content'], 'text/csv')
            
        email.send()
        