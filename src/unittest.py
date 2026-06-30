import re
import unittest
import json
import tempfile
import os
import shutil
from unittest.mock import Mock, patch, MagicMock

import pygame
pygame.init()
pygame.font.init()

import settings
import saves_parser
import stages_parser
import button
import commands_parser


class TestParameters(unittest.TestCase):
    def setUp(self):
        self.params = settings.parameters()

    def test_initial_values(self):
        self.assertEqual(self.params.getFrame(), 60)
        self.assertEqual(self.params.getVolume(), 0.0)

    def test_setFrame(self):
        self.params.setFrame(50)
        self.assertEqual(self.params.getFrame(), 87)
        self.params.setFrame(0)
        self.assertEqual(self.params.getFrame(), 30)
        self.params.setFrame(100)
        self.assertEqual(self.params.getFrame(), 144)

    def test_setVolume(self):
        self.params.setVolume(75)
        self.assertEqual(self.params.getVolume(), 0.75)
        self.params.setVolume(0)
        self.assertEqual(self.params.getVolume(), 0.0)
        self.params.setVolume(100)
        self.assertEqual(self.params.getVolume(), 1.0)


class TestSaveManager(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.stages_path = os.path.join(self.test_dir, "stages.json")
        self.machines_path = os.path.join(self.test_dir, "machines.json")
        self.saves_path = os.path.join(self.test_dir, "save.json")
        self.backup_machines = os.path.join(self.test_dir, "machines_backup.json")
        self.backup_stages = os.path.join(self.test_dir, "stages_backup.json")
        self.backup_saves = os.path.join(self.test_dir, "save_backup.json")

        stages_data = {
            "stage1": {"name": "stage1", "result": "False", "CLI": "PC-ADM"},
            "stage2": {"name": "stage2", "result": "False", "CLI": "PC-BOSS"},
            "stage3": {"name": "stage3", "result": "End"}
        }
        machines_data = {
            "stage1": {"name": "stage1", "result": "False"},
            "stage2": {"name": "stage2", "result": "False"},
            "stage3": {"name": "stage3", "result": "End"}
        }
        save_data = {"stage": "stage1"}

        with open(self.stages_path, 'w', encoding='utf-8') as f:
            json.dump(stages_data, f)
        with open(self.machines_path, 'w', encoding='utf-8') as f:
            json.dump(machines_data, f)
        with open(self.saves_path, 'w', encoding='utf-8') as f:
            json.dump(save_data, f)

        shutil.copy(self.stages_path, self.backup_stages)
        shutil.copy(self.machines_path, self.backup_machines)
        shutil.copy(self.saves_path, self.backup_saves)

        with patch.object(saves_parser.saveManager, '__init__', lambda self: None):
            self.manager = saves_parser.saveManager()
            self.manager.jsonPathStages = self.stages_path
            self.manager.jsonPathMachines = self.machines_path
            self.manager.jsonPathSaves = self.saves_path
            with open(self.stages_path, 'r', encoding='utf-8') as f:
                self.manager.nodesStages = json.load(f)
            with open(self.machines_path, 'r', encoding='utf-8') as f:
                self.manager.nodesMachines = json.load(f)
            with open(self.saves_path, 'r', encoding='utf-8') as f:
                self.manager.save = json.load(f)
            pattern = re.compile(r'^stage\d+$')
            self.manager.countStages = sum(1 for key in self.manager.nodesStages if pattern.match(key))

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def test_downloadSave_initial(self):
        self.assertEqual(self.manager.downloadSave(), "stage1")

    def test_loadSave_skips_true_stages(self):
        # stage1 имеет result False, поэтому он должен быть выбран
        self.manager._loadSave()
        self.assertEqual(self.manager.save["stage"], "stage1")

    def test_downloadGameEvent_dialog(self):
        # stage1 имеет result False -> диалог
        self.manager.stage = "stage1"
        self.manager.nodesStages["stage1"]["result"] = "False"
        self.manager.nodesMachines["stage1"]["result"] = "False"
        self.manager.save["stage"] = "stage1"
        event = self.manager.downloadGameEvent()
        self.assertEqual(event, "dialog")

    def test_downloadGameEvent_desktop(self):
        # stage1 имеет result True, но machines False -> desktop
        self.manager.stage = "stage1"
        self.manager.nodesStages["stage1"]["result"] = "True"
        self.manager.nodesMachines["stage1"]["result"] = "False"
        self.manager.save["stage"] = "stage1"
        event = self.manager.downloadGameEvent()
        self.assertEqual(event, "desktop")

    def test_downloadGameEvent_switches_stage(self):
        # Если оба True, должен переключиться на следующий (stage2)
        self.manager.stage = "stage1"
        self.manager.nodesStages["stage1"]["result"] = "True"
        self.manager.nodesMachines["stage1"]["result"] = "True"
        self.manager.nodesStages["stage2"]["result"] = "False"
        self.manager.nodesMachines["stage2"]["result"] = "False"
        self.manager.save["stage"] = "stage1"
        self.manager.downloadGameEvent()
        self.assertEqual(self.manager.save["stage"], "stage2")

    @patch('saves_parser.saveManager._resetSave')
    def test_resetSave_called_on_end(self, mock_reset):
        self.manager.stage = "stage3"
        self.manager.nodesStages["stage3"]["result"] = "End"
        self.manager.nodesMachines["stage3"]["result"] = "End"
        self.manager.save["stage"] = "stage3"
        self.manager._loadSave()
        mock_reset.assert_called_once()


class TestDialogueManager(unittest.TestCase):
    def setUp(self):
        # Инициализируем pygame для шрифтов (уже сделано в начале)
        self.mock_save = Mock()
        self.mock_save.downloadSave.return_value = "stage1"
        with patch('stages_parser.sp.saveManager', return_value=self.mock_save):
            self.screen_mock = Mock()
            self.dialog = stages_parser.dialogueManager(self.screen_mock)
            self.dialog.nodes = {
                "stage1": {
                    "name": "stage1",
                    "result": "False",
                    "speaker": "Test",
                    "text": "Hello",
                    "choices": [
                        {"text": "Option 1", "next_node": "node1"},
                        {"text": "Option 2", "next_node": "node2"}
                    ]
                },
                "node1": {"speaker": "Test", "text": "You chose 1", "choices": []},
                "node2": {"speaker": "Test", "text": "You chose 2", "choices": []}
            }
            self.dialog.stage = "stage1"
            self.dialog.current_node = self.dialog.nodes["stage1"]
            self.dialog.current_stage = "stage1"

    def test_handleEvent_up_choice(self):
        event = Mock()
        event.type = pygame.KEYDOWN
        event.key = pygame.K_UP
        self.dialog.selected_choice = 1
        self.dialog.handleEvent(event)
        self.assertEqual(self.dialog.selected_choice, 0)

    def test_handleEvent_down_choice(self):
        event = Mock()
        event.type = pygame.KEYDOWN
        event.key = pygame.K_DOWN
        self.dialog.selected_choice = 0
        self.dialog.handleEvent(event)
        self.assertEqual(self.dialog.selected_choice, 1)

    def test_handleEvent_right_choice(self):
        event = Mock()
        event.type = pygame.KEYDOWN
        event.key = pygame.K_RIGHT
        self.dialog.selected_choice = 1
        self.dialog.handleEvent(event)
        self.assertEqual(self.dialog.current_node, self.dialog.nodes["node2"])
        self.assertEqual(self.dialog.selected_choice, 0)

    def test_handleEvent_linear_dialog(self):
        self.dialog.current_node = {"speaker": "Test", "text": "Line1", "next_node": "node1"}
        event = Mock()
        event.type = pygame.KEYDOWN
        event.key = pygame.K_SPACE
        self.dialog.handleEvent(event)
        self.assertEqual(self.dialog.current_node, self.dialog.nodes["node1"])

    def test_restoringStage_sets_result(self):
        self.dialog.current_node = {"success": "True"}
        self.dialog.__restoringStage()
        self.assertEqual(self.dialog.result, "True")
        self.assertEqual(self.dialog.nodes[self.dialog.current_stage]["result"], "True")

    def test_current_CLI_returns_value(self):
        self.dialog.current_stage = "stage1"
        self.dialog.nodes["stage1"]["CLI"] = "PC-ADM"
        self.assertEqual(self.dialog.current_CLI(), "PC-ADM")


class TestButtonLink(unittest.TestCase):
    def setUp(self):
        # Создаём реальные изображения-заглушки с помощью pygame.Surface
        self.front_img = pygame.Surface((50, 30))
        self.back_img = pygame.Surface((50, 30))
        with patch('button.pygame.image.load', return_value=self.front_img):
            self.btn = button.link(10, 20, self.front_img, self.back_img)

    def test_collide_true(self):
        with patch('button.pygame.mouse.get_pos', return_value=(20, 30)):
            self.assertTrue(self.btn.collide())

    def test_collide_false(self):
        with patch('button.pygame.mouse.get_pos', return_value=(100, 100)):
            self.assertFalse(self.btn.collide())

    def test_press_sets_clicked(self):
        with patch('button.pygame.mouse.get_pos', return_value=(20, 30)):
            with patch('button.pygame.mouse.get_pressed', return_value=(1, 0, 0)):
                self.assertTrue(self.btn.press(Mock()))
                self.assertTrue(self.btn.clicked)
                self.assertFalse(self.btn.press(Mock()))

    def test_press_release_resets_clicked(self):
        with patch('button.pygame.mouse.get_pos', return_value=(20, 30)):
            with patch('button.pygame.mouse.get_pressed', return_value=(1, 0, 0)):
                self.btn.press(Mock())
            with patch('button.pygame.mouse.get_pressed', return_value=(0, 0, 0)):
                self.btn.press(Mock())
                self.assertFalse(self.btn.clicked)

    def test_move_sets_offset(self):
        with patch('button.pygame.mouse.get_pos', return_value=(20, 30)):
            with patch('button.pygame.mouse.get_pressed', return_value=(1, 0, 0)):
                self.btn.move(Mock())
                self.assertIsNotNone(self.btn.offset)


class TestCliParser(unittest.TestCase):
    def setUp(self):
        self.mock_save = Mock()
        self.mock_save.downloadSave.return_value = "stage1"
        with patch('commands_parser.sp.saveManager', return_value=self.mock_save):
            # Подменяем создание шрифта, чтобы избежать ошибок
            with patch('pygame.font.SysFont', return_value=Mock()):
                self.cli = commands_parser.cli("PC-ADM")
            self.cli.nodes = {
                "stage1": {
                    "machines": {
                        "PC-ADM": {
                            "config": {
                                "eth0": ["10.1.1.2/24"],
                                "routes": []
                            }
                        },
                        "SW-ADM": {
                            "config": {
                                "vl0": ["10.1.1.253/24"],
                                "routes": ["10.1.1.0/24"]
                            }
                        }
                    }
                }
            }
            self.cli.stage = "stage1"
            self.cli.machine = "PC-ADM"
            self.cli.lines = []
            self.cli.history = []

    def test_commands_help(self):
        self.cli._commands("help")
        self.assertIn("ip ping help history clear", self.cli.lines)

    def test_commands_ip_address(self):
        self.cli.ipAddresses = ["eth0", "10.1.1.2/24"]
        self.cli._commands("ip address")
        self.assertIn("ip address: eth0 10.1.1.2/24", self.cli.lines)

    def test_commands_ip_route(self):
        self.cli.ipRoutes = ["10.1.1.0/24"]
        self.cli._commands("ip route")
        self.assertIn("ip route: 10.1.1.0/24", self.cli.lines)

    def test_commands_ping_success(self):
        with patch.object(self.cli, '___ping', return_value=True):
            self.cli._commands("ping 10.1.1.253")
            self.assertIn("64 bytes from 10.1.1.253: icmp_seq=1 ttl=55 time=269 ms", self.cli.lines[0])

    def test_commands_ping_failure(self):
        with patch.object(self.cli, '___ping', return_value=False):
            self.cli._commands("ping 10.1.1.254")
            self.assertIn("From 10.1.1.254 icmp_seq=1 Destination Host Unreachable", self.cli.lines[0])

    def test_commands_clear(self):
        self.cli.lines = ["some line"]
        self.cli.history = ["cmd1"]
        self.cli._commands("clear")
        self.assertEqual(self.cli.lines, [])
        self.assertEqual(self.cli.history, [])

    def test_commands_unknown(self):
        self.cli._commands("unknown")
        self.assertIn("Error unknown", self.cli.lines)

    def test_restoringStage_checks_ping(self):
        self.cli.ipAddressList = ["10.1.1.2/24", "10.1.1.253/24"]
        self.cli.ipAddresses = ["eth0", "10.1.1.2/24"]
        with patch.object(self.cli, '___ping', return_value=True):
            self.cli.__restoringStage()
            self.assertEqual(self.cli.result, "True")
        with patch.object(self.cli, '___ping', return_value=False):
            self.cli.__restoringStage()
            self.assertEqual(self.cli.result, "False")


if __name__ == '__main__':
    unittest.main()