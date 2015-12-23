from django.test import TestCase
from django.test.client import RequestFactory
from django.core.exceptions import PermissionDenied
from django.contrib.auth.models import User
from mock import patch, MagicMock

from map.models import adventures_info, Adventure
from coreapp.views import (profile, story, auth_view, logout, registration_submission,
                           registration, add_family_member, add_family_member_submission,
                           individual, usejson, get_adventure_detail)

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

@patch('coreapp.views.Game_saved.objects.create')
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
                                 auth_mock, login_mock, reg_mock, game_save_mock):
        user = User()
        filter_mock.return_value = []
        create_user_mock.return_value = user
        auth_mock.return_value = user
        response = registration_submission(self.request)

        create_user_mock.assert_called_with(username='testuser', email='test@test',
                                            password='testpass', first_name='testfname',
                                            last_name='testlname')
        create_level_mock.assert_called_with(user=user, user_point=0, user_level=1)
        game_save_mock.assert_called_with(user=user, adventure_saved='', task_saved='')
        auth_mock.assert_called_with(username='testuser', password='testpass')
        login_mock.assert_called_with(self.request, user)
        self.assertFalse(reg_mock.called)
        self.assertEqual(response.status_code, 302)

    def test_invalid_email(self, filter_mock, create_user_mock, create_level_mock,
                           auth_mock, login_mock, reg_mock, game_save_mock):
        filter_mock.side_effect = [[], [1]]
        registration_submission(self.request)
        reg_mock.assert_called_with(self.request, 'Try again, there is already an' \
                                    ' account with that email test@test.')
        self.assertFalse(create_user_mock.called)
        self.assertFalse(create_level_mock.called)
        self.assertFalse(game_save_mock.called)
        self.assertFalse(auth_mock.called)
        self.assertFalse(login_mock.called)

    def test_invalid_user(self, filter_mock, create_user_mock, create_level_mock,
                           auth_mock, login_mock, reg_mock, game_save_mock):

        filter_mock.return_value = [1]
        registration_submission(self.request)
        reg_mock.assert_called_with(self.request, 'Try again, the username testuser' \
                                    ' is already taken.')
        self.assertFalse(game_save_mock.called)
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

class AddFamilySubmissionTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    @patch('coreapp.views.User.character_set')
    @patch('coreapp.views.messages.success')
    def test_family_member_exist(self, message_mock, char_set_mock):
        request = self.factory.post('/add-family-member-submission/',
                                    {'member-name':'test', 'member-pin':'1234'})
        request.user = User()
        char_set_mock.filter = MagicMock(return_value=True)
        response = add_family_member_submission(request)

        char_set_mock.filter.assert_called_with(character_name='test')
        message_mock.assert_called_with(request, 'This member has already been' \
                                        ' added, try another name')
        self.assertEqual(response.status_code, 302)

    @patch('coreapp.views.messages.success')
    def test_bad_pin_input(self, message_mock):
        request = self.factory.post('/add-family-member-submission/',
                                    {'member-name':'test', 'member-pin':'123'})

        response = add_family_member_submission(request)

        message_mock.assert_called_with(request, 'Please enter 4 characters as your PIN number')
        self.assertEqual(response.status_code, 302)

    @patch('coreapp.views.User.character_set')
    @patch('coreapp.views.messages.success')
    def test_family_member_success(self, message_mock, char_set_mock):
        request = self.factory.post('/add-family-member-submission/',
                                    {'member-name':'test', 'member-pin':'1234'})
        request.user = User()
        char_set_mock.filter = MagicMock(return_value=False)
        char_set_mock.create = MagicMock()

        response = add_family_member_submission(request)

        char_set_mock.filter.assert_called_with(character_name='test')
        char_set_mock.create.assert_called_with(character_name='test',
                                                character_pin='1234')
        self.assertFalse(message_mock.called)
        self.assertEqual(response.status_code, 302)

@patch('coreapp.views.get_logged_in_char')
@patch('coreapp.views.get_all_characters')
class IndividualViewTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.request = self.factory.post('/individual/',
                                         {'character_name':'test', 'character_pin':'1234'})
        self.request.user = User()

    @patch('coreapp.views.profile')
    def test_family_member_change(self, prof_mock, get_char_mock, logged_char_mock):
        char = MagicMock()
        char.save = MagicMock()
        logged_char_mock.return_value = [char]
        get_char_mock.return_value = 'test'

        individual(self.request)

        get_char_mock.assert_called_with(self.request.user)
        logged_char_mock.assert_called_with('test')
        self.assertTrue(char.save.called)
        self.assertFalse(char.is_logged)
        prof_mock.assert_called_with(self.request)

    @patch('coreapp.views.User.character_set')
    def test_success_member_login(self, char_set_mock, get_char_mock, logged_char_mock):
        char = MagicMock()
        char.save = MagicMock()
        char_set_mock.filter = MagicMock(return_value=[char])
        logged_char_mock.return_value = False
        get_char_mock.return_value = 'test'

        response = individual(self.request)

        get_char_mock.assert_called_with(self.request.user)
        logged_char_mock.assert_called_with('test')
        char_set_mock.filter.assert_called_with(character_name='test', character_pin='1234')
        self.assertTrue(char.save.called)
        self.assertTrue(char.is_logged)
        self.assertEqual(response.status_code, 302)

    @patch('coreapp.views.User.character_set')
    @patch('coreapp.views.messages.success')
    def test_incorrect_input(self, message_mock, char_set_mock, get_char_mock, logged_char_mock):
        get_char_mock.return_value = 'testchar'
        logged_char_mock.return_value = False
        char_set_mock.filter = MagicMock()
        char_set_mock.filter.return_value = False

        response = individual(self.request)

        get_char_mock.assert_called_with(self.request.user)
        logged_char_mock.assert_called_with('testchar')
        char_set_mock.filter.assert_called_with(character_name='test', character_pin='1234')
        message_mock.assert_called_with(self.request, 'The PIN you entered is incorrect or did not'\
                                        ' select your family role, please try again!')
        self.assertEqual(response.status_code, 302)

class JsonTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.request = self.factory.get('/')

    @patch('coreapp.views.render')
    def test_use_json(self, render_mock):
        usejson(self.request)
        render_mock.assert_called_with(self.request, 'coreapp/getjson.html', {'usea':'hahah'})

    @patch('coreapp.views.adventures_info.objects')
    @patch('coreapp.views.Adventure.objects')
    @patch('coreapp.views.JsonResponse')
    def test_get_json_success(self, json_mock, adven_mock, adven_info_mock):
        self.request.is_ajax = MagicMock()
        self.request.is_ajax.return_value = True
        self.request.user = MagicMock()
        self.request.user.game_saved = MagicMock()
        self.request.user.game_saved.adventure_saved = 1

        adven_mock.get = MagicMock()
        adven = Adventure()
        adven.adventure_name = 'testname'
        adven_mock.get.return_value = adven

        adven_info = adventures_info()
        adven_info.items_needed = 2
        adven_info.expenses = 3
        adven_info.locations = "testlocation"
        adven_info.map_address = 4
        adven_info_mock.get = MagicMock()
        adven_info_mock.get.return_value = adven_info

        alist = [{"name" : 'testname',
                  "items" : '2',
                  "expenses" : '3',
                  "locations" : 'testlocation',
                  "mapaddress" : '4'}]

        get_adventure_detail(self.request)
        json_mock.assert_called_with(alist, safe=False)

    def test_get_json_exception(self):
        self.request.is_ajax = MagicMock()
        self.request.is_ajax.return_value = False
        with self.assertRaises(PermissionDenied):
            get_adventure_detail(self.request)


