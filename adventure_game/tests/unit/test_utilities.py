from django.test import TestCase
from mock import patch, MagicMock
from coreapp.utilities import get_profile_context

class TestGetProfileContext(TestCase):
    def setUp(self):
        self.user = MagicMock()
        self.user.level_num = '1'

    @patch('coreapp.utilities.get_character_name')
    @patch('coreapp.utilities.load_game_save_id')
    @patch('coreapp.utilities.load_completed_adventures')
    @patch('coreapp.utilities.load_adventures')
    def test_get_profile_context(self, la_mock, lca_mock, lgsi_mock, get_char_mock):
        characters = MagicMock()
        get_char_mock.return_value = 'testchar'
        context = {'character_name' : 'testchar',
                   'level' : '1',
                   'game_saved' : [],
                   'zipped' : [],
                   'completed_list' : [],
                  }
        val = get_profile_context(self.user, characters)
        self.assertEqual(val, context)
        la_mock.assert_called_with([], [], [], [])
        lca_mock.assert_called_with([], self.user)
        lgsi_mock.assert_called_with([], self.user)
        get_char_mock.assert_called_with(characters)

