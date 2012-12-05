"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""
import random
from django.test import TestCase
from courses.exams.autograder import *
from sets import Set


class SimpleTest(TestCase):
    def test_basic_addition(self):
        """
        Tests that 1 + 1 always equals 2.
        """
        self.assertEqual(1 + 1, 2)

    def test_multiple_choice_factory_normal(self):
        """
        Tests the multiple-choice autograder.
        """
        ag = AutoGrader("__testing_bypass")
            #Regular test case
        mc_fn = ag._MC_grader_factory(["a","b"])
        self.assertTrue(mc_fn(["a","b"]))
        self.assertTrue(mc_fn(("b","a"))) #note this input is a tuple
        self.assertTrue(mc_fn(("b","b","a","a"))) #and this one too
        self.assertFalse(mc_fn(["a","b","c"]))
        self.assertFalse(mc_fn(["a"]))
        self.assertFalse(mc_fn([]))           

    def test_multiple_choice_factory_empty(self):
        """
        Tests the multiple-choice autograder when initialized to empty list
        """
        ag = AutoGrader("__testing_bypass")
            #Empty case
        empty_fn = ag._MC_grader_factory([])
        self.assertTrue(empty_fn([]))
        self.assertFalse(empty_fn(["a"]))
        self.assertFalse(empty_fn(["a","b"]))

    def test_multiple_choice_factory_random(self):
        """
            Uses the random generator to make test cases for the multiple choice factory
            Tests 10 times
        """
        ag = AutoGrader("__testing_bypass")
        choicelist = "abcdefghijklmnopqrstuvwxyz"
        for i in range(10):
            numsolns = random.randint(1,26)
            solutions = random.sample(choicelist, numsolns)
            grader = ag._MC_grader_factory(solutions)
            wrongsub = random.sample(choicelist, random.randint(1,26))
            if Set(solutions) != Set(wrongsub):
                self.assertFalse(grader(wrongsub))
            random.shuffle(solutions)
            self.assertTrue(grader(solutions))

    def test_multiple_choice_metadata(self):
        """
        Tests basic functionality of multiple-choice input via metadata
        """
        xml = """
            <exam_metadata>
                <question_metadata id="problem_1" data-tag4humans="Apple Competitor Question">
                    <response name="q1d" answertype="multiplechoiceresponse" data-tag4humans="Apple Competitors">
                        <choice value="ipad" data-tag4humans="iPad" correct="false">
                            <explanation>Try again</explanation>
                        </choice>
                        <choice value="napster" data-tag4humans="Napster" correct="true">
                            <explanation>Try again</explanation>
                        </choice>
                        <choice value="ipod" data-tag4humans="iPod" correct="true">
                            <explanation>This is right!</explanation>
                        </choice>
                        <choice value="peeler" data-tag4humans="Vegetable Peeler" correct="false">
                            <explanation>Try again</explanation>
                        </choice>
                        <choice value="android" data-tag4humans="Android" correct="false">
                            <explanation>Try again</explanation>
                        </choice>
                        <choice value="beatles" data-tag4humans="The Beatles" correct="false">
                            <explanation>Try again</explanation>
                        </choice>
                    </response>
                </question_metadata>
                <question_metadata id="problem_2">
                    <response name="test2" answertype="multiplechoiceresponse">
                        <choice value="a" correct="False" />
                        <choice value="b" correct="True" />
                        <choice value="c" correct="True" />
                    </response>
                </question_metadata>
            </exam_metadata>
            """
        ag = AutoGrader(xml)
            #problem 1
        self.assertTrue(ag.grader_functions['q1d'](["napster", "ipod"]))
        self.assertTrue(ag.grader_functions['q1d'](["ipod", "napster"]))
        self.assertFalse(ag.grader_functions['q1d'](["ipad", "ipod", "napster"]))
        self.assertFalse(ag.grader_functions['q1d'](["ipo"]))
        self.assertFalse(ag.grader_functions['q1d'](["ipod"]))
        self.assertFalse(ag.grader_functions['q1d']([]))
        self.assertTrue(ag.grade('q1d', ["ipod", "napster"]))
        self.assertFalse(ag.grade('q1d', ["q1d_1"]))

            #problem 2
        self.assertTrue(ag.grader_functions['test2'](["b","c"]))
        self.assertTrue(ag.grader_functions['test2'](["c","b"]))
        self.assertFalse(ag.grader_functions['test2'](["a","b"]))
        self.assertFalse(ag.grader_functions['test2'](["a","b","c"]))
        self.assertFalse(ag.grader_functions['test2'](["a"]))
        self.assertFalse(ag.grader_functions['test2']([]))
        self.assertTrue(ag.grade('test2',["b","c"]))
        self.assertFalse(ag.grade('test2',["a"]))

            #exception due to using an undefined input name
        with self.assertRaisesRegexp(AutoGraderGradingException, 'Input/Response name="notDef" is not defined in grading template'):
            ag.grade('notDef', ['a','b'])


    def test_parse_xml_question_metadata_no_id(self):
        """Tests for exception when parsing question metadata with no id"""
        
        xml = """
            <exam_metadata>
            <question_metadata>
            </question_metadata>
            </exam_metadata>
            """
        with self.assertRaisesRegexp(AutoGraderMetadataException, 'A <question_metadata> tag has no "id" attribute!'):
            ag = AutoGrader(xml)


    def test_parse_xml_question_metadata_no_response(self):
        """Tests for exception when parsing question metadata with no responses"""
        
        xml = """
            <exam_metadata>
            <question_metadata id="q1">
            </question_metadata>
            </exam_metadata>
            """
        with self.assertRaisesRegexp(AutoGraderMetadataException, '<question_metadata id="q1"> has no <response> child tags!'):
            ag = AutoGrader(xml)

    def test_parse_xml_response_no_name(self):
        """Tests for exception when parsing response with no name"""
        
        xml = """
            <exam_metadata>
            <question_metadata id="q1">
                <response answertype="multiplechoiceresponse"/>
            </question_metadata>
            </exam_metadata>
            """
        with self.assertRaisesRegexp(AutoGraderMetadataException, '.*no name attribute.*'):
            ag = AutoGrader(xml)


    def test_parse_xml_question_response_no_type(self):
        """Tests for exception when parsing response with no answertype"""
        
        xml = """
            <exam_metadata>
            <question_metadata id="q1">
                <response name="foo" />
            </question_metadata>
            </exam_metadata>
            """
        with self.assertRaisesRegexp(AutoGraderMetadataException, '.*no "answertype" attribute.*'):
            ag = AutoGrader(xml)

    def test_parse_xml_question_dup_response(self):
        """
        Tests for exception when parsing XML with duplicate response names
        NOTE: This is not okay even across different questions.
        """
        
        xml = """
            <exam_metadata>
            <question_metadata id="q1">
                <response name="foo" answertype="multiplechoiceresponse">
                    <choice value="a" correct="true" />
                </response>
            </question_metadata>
            <question_metadata id="q2">
                <response name="foo" answertype="multiplechoiceresponse">
                    <choice value="a" correct="true" />
                </response>
            </question_metadata>
            </exam_metadata>
            """
        with self.assertRaisesRegexp(AutoGraderMetadataException, 'Duplicate name "foo".*<response>.*'):
            ag = AutoGrader(xml)


    def test_parse_xml_question_response_no_choices(self):
        """Tests for exception when parsing response with no choices"""
        
        xml = """
            <exam_metadata>
            <question_metadata id="q1">
                <response name="foo" answertype="multiplechoiceresponse" />
            </question_metadata>
            </exam_metadata>
            """
        with self.assertRaisesRegexp(AutoGraderMetadataException, '.*no <choice> descendants.*'):
            ag = AutoGrader(xml)

    def test_parse_xml_question_response_dup_choice(self):
        """
            Tests for exception when parsing response with duplicate choice id
            NOTE: it is okay to duplicate response ids across choices
        """
        
        xml = """
            <exam_metadata>
            <question_metadata id="q1">
                <response name="foo" answertype="multiplechoiceresponse">
                    <choice value="a" correct="true" />
                    <choice value="a" correct="false" />
                </response>
            </question_metadata>
            <question_metadata id="q2">
                <response name="foo2" answertype="multiplechoiceresponse">
                    <choice value="a" correct="true" />
                </response>
            </question_metadata>
            </exam_metadata>
            """
        with self.assertRaisesRegexp(AutoGraderMetadataException, '.*<choice> tags with duplicate value "a"'):
            ag = AutoGrader(xml)

    def test_parse_xml_question_response_no_choice_id(self):
        """
        Tests for exception when parsing choice with no id
        """
        
        xml = """
              <exam_metadata>
              <question_metadata id="q1">
                  <response name="foo" answertype="multiplechoiceresponse">
                      <choice value="a" correct="true"></choice>
                      <choice correct="false"></choice>
                  </response>
              </question_metadata>
              </exam_metadata>
              """
        with self.assertRaisesRegexp(AutoGraderMetadataException, '.*<choice> tag with no "value".*'):
            ag = AutoGrader(xml)

    def test_parse_numericresponse_metadata(self):
        """
        Testing driver for numerical response development
        """

        xml = """
            <exam_metadata>
            <question_metadata id="problem_4" data-tag4humans="Short-answer2">
                <response name="q4d" answertype="numericalresponse" answer="3.14159" data-tag4humans="Value of Pi">
                    <responseparam type="tolerance" default=".02"></responseparam>
                </response>
                <response name="q4e" answertype="numericalresponse" answer="4518"
                    data-tag4humans="value of 502*9">
                    <responseparam type="tolerance" default="15%"></responseparam>
                </response>
                <response name="q4f" answertype="numericalresponse" answer="5" data-tag4humans="number of fingers on a hand"></response>
            </question_metadata>
            </exam_metadata>
            """
        ag = AutoGrader(xml)
        self.assertTrue(ag.grade('q4d', 3.14159))
        self.assertTrue(ag.grade('q4d', 3.14159+0.02))
        self.assertTrue(ag.grade('q4d', 3.14159-0.02))
        self.assertFalse(ag.grade('q4d',3.5))
        self.assertFalse(ag.grade('q4d',3.0))
    
        self.assertTrue(ag.grade('q4e', 4518))
        self.assertTrue(ag.grade('q4e', 4518*1.149))
        self.assertTrue(ag.grade('q4e', 4518*0.851))
        self.assertFalse(ag.grade('q4e',4518*1.151))
        self.assertFalse(ag.grade('q4e',4518*1.849))

        self.assertTrue(ag.grade('q4f', 5))
        self.assertFalse(ag.grade('q4f', 4))
        self.assertFalse(ag.grade('q4f', 6))



