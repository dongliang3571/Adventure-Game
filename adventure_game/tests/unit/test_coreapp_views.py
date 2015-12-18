from django.test import TestCase
from django.test.client import RequestFactory
from django.contrib.auth.models import User
from mock import patch, Mock, mock, MagicMock
from coreapp.views import profile, story, auth_view, logout

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

    def test_func_logged_in(self, get_all_char_mock, get_prof_context_mock,
                            get_logged_in_char_mock, render_mock):

        context = {'test' : 'test'}
        get_prof_context_mock.return_value = context
        get_all_char_mock.return_value = "Test Character"
        profile(self.request)

        get_all_char_mock.assert_called_with(self.request.user)
        get_logged_in_char_mock.assert_called_with("Test Character")
        get_prof_context_mock.assert_called_with(self.request.user, "Test Character")
        render_mock.assert_called_with(self.request, 'coreapp/individual.html', context)

    def test_func_not_logged_in(self, get_all_char_mock, get_prof_context_mock,
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

@patch('coreapp.views.auth.authenticate')
@patch('coreapp.views.messages.success')
class AuthViewTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User()
        self.request = self.factory.post('/auth/', {'username':'testuser', 'password':'testpass'})

    @patch('coreapp.views.auth.login')
    def test_sucess_logged_in(self, login_mock, message_mock, auth_mock):
        self.user.is_active = True
        self.user.last_name = 'testlname'
        auth_mock.return_value = self.user
        response = auth_view(self.request)

        self.assertEqual(response.status_code, 302)
        auth_mock.assert_called_with(username='testuser', password='testpass')
        login_mock.assert_called_with(self.request, self.user)
        message_mock.assert_called_with(self.request,
                                        'Hi testlname, you have successfully logged in.')

    def test_banned(self, message_mock, auth_mock):
        self.user.is_active = False
        auth_mock.return_value = self.user
        response = auth_view(self.request)

        self.assertEqual(response.status_code, 302)
        message_mock.assert_called_with(self.request, 'Your account has been banned,' \
                                        ' please contact us to re-activate your account!')

    def test_failed_logged_in(self, message_mock, auth_mock):
        auth_mock.return_value = None
        response = auth_view(self.request)
        self.assertEqual(response.status_code, 302)
        message_mock.assert_called_with(self.request, 'The account you entered' \
                                        ' is invalid, please try again!')

class LogoutViewTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    @patch('coreapp.views.auth.logout')
    @patch('coreapp.views.messages.success')
    def test_func_args(self, message_mock, logout_mock):
        request = self.factory.get('/')
        logout(request)

        logout_mock.assert_called_with(request)
        message_mock.assert_called_with(request, 'You have successfully logged out.')



