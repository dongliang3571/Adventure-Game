from django.test import TestCase
from django.test.client import RequestFactory
from django.contrib.auth.models import User
from mock import patch, Mock, mock, MagicMock
from coreapp.views import profile, story

@patch('coreapp.views.render')
@patch('coreapp.views.get_logged_in_char')
@patch('coreapp.views.get_profile_context')
@patch('coreapp.views.get_all_characters')
class ProileViewTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.request = self.factory.get('/profile/')
        self.request.user = User()
        self.request.user.last_name = "test"
    def test_func_calls_logged_in(self, get_all_char_mock, get_prof_context_mock,
                                  get_logged_in_char_mock, render_mock):

        response = profile(self.request)

        self.assertTrue(get_all_char_mock.called)
        self.assertTrue(get_prof_context_mock.called)
        self.assertTrue(get_logged_in_char_mock.called)
        self.assertTrue(render_mock.called)
        self.assertEqual(render_mock.return_value, response)

    def test_func_call_not_logged_in(self, get_all_char_mock, get_prof_context_mock,
                                     get_logged_in_char_mock, render_mock):
        get_logged_in_char_mock.return_value = None
        response = profile(self.request)
        self.assertTrue(get_logged_in_char_mock.called)
        self.assertTrue(get_all_char_mock.call)
        self.assertFalse(get_prof_context_mock.called)
        self.assertTrue(render_mock.called)
        self.assertEqual(render_mock.return_value, response)

    def test_func_args_logged_in(self, get_all_char_mock, get_prof_context_mock,
                                 get_logged_in_char_mock, render_mock):

        context = {'test' : 'test'}
        get_prof_context_mock.return_value = context
        get_all_char_mock.return_value = "Test Character"
        profile(self.request)

        get_all_char_mock.assert_called_with(self.request.user)
        get_logged_in_char_mock.assert_called_with("Test Character")
        get_prof_context_mock.assert_called_with(self.request.user, "Test Character")
        render_mock.assert_called_with(self.request, 'coreapp/individual.html', context)

    def test_func_args__not_logged_in(self, get_all_char_mock, get_prof_context_mock,
                                      get_logged_in_char_mock, render_mock):

        get_all_char_mock.return_value = "Test Character"
        context = {'family_members' : 'Test Character', 'lastname' : 'test'}
        get_logged_in_char_mock.return_value = None
        profile(self.request)

        get_all_char_mock.assert_called_with(self.request.user)
        get_logged_in_char_mock.assert_called_with("Test Character")
        render_mock.assert_called_with(self.request, 'coreapp/profile.html', context)
        self.assertFalse(get_prof_context_mock.called)

class StoryViewTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.request = self.factory.get('/')

    @patch('coreapp.views.render')
    def test_story_view(self, render_mock):
        story(self.request)
        self.assertTrue(render_mock.called)
        render_mock.assert_called_with(self.request, 'coreapp/story.html')
