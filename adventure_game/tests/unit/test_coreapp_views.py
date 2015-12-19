from django.test import TestCase
from django.test.client import RequestFactory
from django.contrib.auth.models import User
from mock import patch, MagicMock
from coreapp.views import (profile, story, auth_view, logout, registration_submission,
                           registration, add_family_member, add_family_member_submission)


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

@patch('coreapp.views.registration')
@patch('coreapp.views.auth.login')
@patch('coreapp.views.auth.authenticate')
@patch('coreapp.views.Level_num.objects.create')
@patch('coreapp.views.User.objects.create_user')
@patch('coreapp.views.User.objects.filter')
class CreateUserTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.request = self.factory.post('/registration-submission',
                                         {'username':'testuser', 'firstname':'testfname',
                                          'lastname':'testlname', 'email':'test@test',
                                          'password':'testpass'})

    def test_user_create_success(self, filter_mock, create_user_mock, create_level_mock,
                                 auth_mock, login_mock, reg_mock):
        user = User()
        filter_mock.return_value = []
        create_user_mock.return_value = user
        auth_mock.return_value = user
        response = registration_submission(self.request)

        create_user_mock.assert_called_with(username='testuser', email='test@test',
                                            password='testpass', first_name='testfname',
                                            last_name='testlname')
        create_level_mock.assert_called_with(user=user, user_point=0, user_level=1)
        auth_mock.assert_called_with(username='testuser', password='testpass')
        login_mock.assert_called_with(self.request, user)
        self.assertFalse(reg_mock.called)
        self.assertEqual(response.status_code, 302)

    def test_invalid_email(self, filter_mock, create_user_mock, create_level_mock,
                           auth_mock, login_mock, reg_mock):
        filter_mock.side_effect = [[], [1]]
        registration_submission(self.request)
        reg_mock.assert_called_with(self.request, 'Try again, there is already an' \
                                    ' account with that email test@test.')
        self.assertFalse(create_user_mock.called)
        self.assertFalse(create_level_mock.called)
        self.assertFalse(auth_mock.called)
        self.assertFalse(login_mock.called)

    def test_invalid_user(self, filter_mock, create_user_mock, create_level_mock,
                           auth_mock, login_mock, reg_mock):

        filter_mock.return_value = [1]
        registration_submission(self.request)
        reg_mock.assert_called_with(self.request, 'Try again, the username testuser' \
                                    ' is already taken.')
        self.assertFalse(create_user_mock.called)
        self.assertFalse(create_level_mock.called)
        self.assertFalse(auth_mock.called)
        self.assertFalse(login_mock.called)

@patch('coreapp.views.csrf')
@patch('coreapp.views.render')
class RegistrationViewTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.request = self.factory.get('/register/')

    def test_registration_view_with_message(self, render_mock, csrf_mock):
        message = "test"
        csrf_mock.return_value = {'csrf':'test'}
        context = {'message':'test', 'csrf':'test'}
        registration(self.request, message)

        csrf_mock.assert_called_with(self.request)
        render_mock.assert_called_with(self.request, 'auth/registration.html', context)

    def test_registration_view_without_message(self, render_mock, csrf_mock):
        csrf_mock.return_value = {'csrf':'test'}
        registration(self.request)
        context = {'csrf':'test'}
        render_mock.assert_called_with(self.request, 'auth/registration.html', context)


@patch('coreapp.views.csrf')
@patch('coreapp.views.render')
class AddFamilyMemberViewTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.request = self.factory.get('/add-family-member/')

    def test_add_fam_view_with_message(self, render_mock, csrf_mock):
        message = "test"
        csrf_mock.return_value = {'csrf':'test'}
        context = {'message':'test', 'csrf':'test'}
        add_family_member(self.request, message)

        csrf_mock.assert_called_with(self.request)
        render_mock.assert_called_with(self.request, 'auth/addfamily.html', context)

    def test_add_fam_view_without_message(self, render_mock, csrf_mock):
        csrf_mock.return_value = {'csrf':'test'}
        add_family_member(self.request)
        context = {'csrf':'test'}
        render_mock.assert_called_with(self.request, 'auth/addfamily.html', context)

#@patch('coreapp.views.User.character_set.filter')
#@patch('coreapp.views.messages.success')
class AddFamilySubmissionTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    @patch('coreapp.views.User.character_set')
    @patch('coreapp.views.messages.success')
    def test_family_member_exist(self, message_mock, filter_mock):
        request = self.factory.post('/add-family-member-submission/',
                                    {'member-name':'test', 'member-pin':'1234'})
        request.user = User()
        filter_mock.return_value = True
        filter_mock.filter = MagicMock(return_value=True)
        response = add_family_member_submission(request)

        filter_mock.filter.assert_called_with(character_name='test')
        message_mock.assert_called_with(request, 'This member has already been' \
                                        ' added, try another name')
        self.assertEqual(response.status_code, 302)

