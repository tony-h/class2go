from django.core.urlresolvers import reverse
from lxml import etree
from tests.test_base import AuthenticatedTestBase

class StudentVideoTest(AuthenticatedTestBase):
    course_name="Natural Language Processing"
    fixtures = ['db_snapshot_video_tests.json']

    def __init__(self, *arrgs, **kwargs):
        config = { 'username' : 'student_1',
                   'password' : 'class2go',
                   'course_prefix' :'networking',
                   'course_suffix' :'Fall2012',
                   'mode' : 'ready' }
        if kwargs != None:
            kwargs.update(config)
        else:
            kwargs = config
        super(StudentVideoTest, self).__init__(*arrgs, **kwargs)


    def test_course_video_list(self):
        """
        Tests the display of the course video list page
        """
        # build the url once
        test_url = reverse('course_video_list',
                           kwargs={'course_prefix' : self.coursePrefix,
                                   'course_suffix' : self.courseSuffix })

        # fetch the response
        response = self.client.get(test_url)
        self.assertEqual(response.status_code, 200)

        # ensure we got the correct page by matching the title
        course_title_search_string = "<title>Video | " + self.course_name + "</title>"
        self.assertRegexpMatches(response.content, 
                course_title_search_string,
                msg="Couldn't find the title %s in '%s'" % (course_title_search_string, test_url ))

        # parse the html into a tree and run an xpath for video list items.
        # there should be 3 live videos in the content
        tree = etree.HTML(response.content)
        result = tree.xpath('//*[contains(@class, "course-list-item")]')
        self.assertEqual(len(result), 3, msg="Wrong number of live videos.")

    def test_course_video(self):
        """
        Tests the display of an individual video
        """
        # check for the iframe with id=player and/or title=YouTube video player and/or src contains youtube.com
        pass
