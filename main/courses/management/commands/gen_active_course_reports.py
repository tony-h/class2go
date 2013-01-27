from django.core.management.base import BaseCommand, CommandError
from c2g.models import *
from django.contrib.auth.models import User,Group
from django.db import connection, transaction
from courses.reports.tasks import generate_and_email_reports
from datetime import datetime, timedelta


class Command(BaseCommand):
    help = "Generates course_dashboard and course_quizzes reports _for_courses_that_are_currently_active_. Syntax: manage.py gen_active_course_reports\n"
        
    def handle(self, *args, **options):
        now = datetime.now()
        active_courses = Course.objects.filter(mode='ready', calendar_end__gt=now)
        
        for ready_course in active_courses:
            email_title = "[Class2Go] Daily %s Reports" % ready_course.handle.replace('--', '-')
            email_message = "To generate or download any of Class2Go's report types, please visit your course's reports page from Course Administration->Reports, or by visiting https://class2go.auca.kg/%s/browse_reports." % ready_course.handle.replace('--', '/')
            generate_and_email_reports.delay('c2g_daily_report_mailer', ready_course.handle, [{'type':'dashboard'}, {'type':'course_quizzes'}], email_title, email_message)
