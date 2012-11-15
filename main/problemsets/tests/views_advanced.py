from c2g.models import ProblemSet
from datetime import datetime, timedelta
from problemsets.tests.test_base import SimpleTestBase

__all__ = ['InstructorDraftModeTestAdv']

class InstructorDraftModeTestAdv(SimpleTestBase):
    fixtures = ['pset_testdata.json']
    username = 'professor_0'
    password = 'class2go'
    coursePrefix = 'networking'
    courseSuffix = 'Fall2012'

    def test_create_problemset_action(self):
        """
        Tests the creation of a new problemset
        url(r'^createproblemsetaction/?',
            'problemsets.views.create_action'),
        """
        # Get the number of problemsets
        numProblemSets = len(ProblemSet.objects.all())
        self.assertEqual(numProblemSets,4)
        self.assertEqual( len(ProblemSet.objects.filter(mode='ready')), numProblemSets/2 )
        self.assertEqual( len(ProblemSet.objects.filter(mode='draft')), numProblemSets/2 )
    
        # Create a new problemset
        resp = self.client.post('/createproblemsetaction/',
                                {'course_prefix': self.coursePrefix,
                                 'course_suffix': self.courseSuffix,
                                 'title': 'XXXXXXXXXX This is a test XXXXXXXX',
                                 'slug':'testPS',
                                 'assessment_type': 'formative',
                                 'submissions_permitted': 5,
                                 'late_penalty': 10,
                                 'section': '1',
                                 'resubmission_penalty': 10,
                                 'grace_period': datetime.strftime(datetime.today(), '%m/%d/%Y %H:%M'),
                                 'partial_credit_deadline': datetime.strftime(datetime.today()+timedelta(21), '%m/%d/%Y %H:%M'),
                                 'due_date':  datetime.strftime(datetime.today()+timedelta(7), '%m/%d/%Y %H:%M'),
                                },
                                HTTP_USER_AGENT=self.userAgent )

        # assert that we got redirected to the manage_exercises page
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(resp['location'], 'http://testserver/networking/Fall2012/problemsets/testPS/manage_exercise')

        # assert that there are 2 more problemsets, one each for ready & draft
        self.assertEqual( len(ProblemSet.objects.all()), numProblemSets+2 )
        self.assertEqual( len(ProblemSet.objects.filter(mode='ready')), (numProblemSets/2)+1 )
        self.assertEqual( len(ProblemSet.objects.filter(mode='draft')), (numProblemSets/2)+1 )

