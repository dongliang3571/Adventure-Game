from django.test import TestCase
from mock import patch, MagicMock
from coreapp.queries import (load_adventures, load_completed_adventures,
                             get_logged_in_char, load_game_save_id,
                             get_character_name, get_all_characters)

class CoreappQueryTest(TestCase):
    def setUp(self):
        pass

    @patch('coreapp.queries.Adventure')
    def test_load_adventures(self, adventure_mock):
        adventure_mock.objects.all = MagicMock()
        testadv1 = MagicMock()
        testadv1.adventure_name = 'testname'
        testadv1.adventure_img_url = 'testurl'
        testadv1.adventure_id = 'testid'
        testadv1.adventure_description = 'testdescription'
        adventure_mock.objects.all.return_value = [testadv1]

        adventure_name_list = []
        adventure_img_url_list = []
        adventure_id_list = []
        adventure_description_list = []

        load_adventures(adventure_name_list, adventure_img_url_list, adventure_id_list, adventure_description_list)
        self.assertEqual(adventure_name_list[0], 'testname')
        self.assertEqual(adventure_img_url_list[0], 'testurl')
        self.assertEqual(adventure_id_list[0], 'testid')
        self.assertEqual(adventure_description_list[0], 'testdescription')

    @patch('coreapp.queries.Track')
    def test_load_completed_adventures(self, track_mock):
        adventure_complete_list = []
        user = MagicMock()

        track_mock.objects.filter = MagicMock()
        testtrack = MagicMock()
        testtrack.adventure_done = 'test'
        track_mock.objects.filter.return_value = [testtrack]

        load_completed_adventures(adventure_complete_list, user)
        track_mock.objects.filter.assert_called_with(user=user)
        self.assertEqual(adventure_complete_list[0], 'test')

    def test_get_logged_in_char(self):
        character = MagicMock()
        character.filter = MagicMock()
        character.filter.return_value = 'test'

        test = get_logged_in_char(character)
        character.filter.assert_called_with(is_logged=True)
        self.assertEqual(test, 'test')

    @patch('coreapp.queries.Game_saved.objects')
    def test_load_game_save_id(self, game_saved_mock):
        game_saved_id_list = []
        game_saved_mock.filter = MagicMock()
        user = MagicMock()
        game_saved = MagicMock()
        game_saved.adventure_saved = 1
        game_saved_mock.filter.return_value = [game_saved]
        load_game_save_id(game_saved_id_list, user)
        self.assertEquals(game_saved_id_list[0], '1')
        game_saved_mock.filter.assert_called_with(user=user)

    def test_get_character_name(self):
        characters = MagicMock()
        char = MagicMock()
        char.character_name = 'testname'
        characters.filter = MagicMock()
        characters.filter.return_value = [char]
        test = get_character_name(characters)
        characters.filter.assert_called_with(is_logged=True)
        self.assertEquals(test, 'testname')

    def test_get_all_characters(self):
        user = MagicMock()
        user.character_set.all = MagicMock()
        user.character_set.all.return_value = 'test'
        self.assertEquals(get_all_characters(user), 'test')



