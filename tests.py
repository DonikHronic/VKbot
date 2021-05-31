from unittest import TestCase
from unittest.mock import patch, Mock, ANY

from vk_api.bot_longpoll import VkBotMessageEvent

from bot import Bot


class Tests1(TestCase):
	RAW_EVENT = {
		'type': 'message_new',
		'object': {
			'message': {
				'date': 1621011069,
				'from_id': 470235051,
				'id': 101,
				'out': 0,
				'peer_id': 470235051,
				'text': 'test message',
				'conversation_message_id': 99,
				'fwd_messages': [],
				'important': False,
				'random_id': 0,
				'attachments': [],
				'is_hidden': False
			},
			'client_info': {
				'button_actions': [
					'text',
					'vkpay',
					'open_app',
					'location',
					'open_link',
					'callback',
					'intent_subscribe',
					'intent_unsubscribe'
				],
				'keyboard': True,
				'inline_keyboard': True,
				'carousel': False,
				'lang_id': 0
			}
		},
		'group_id': 204370382,
		'event_id': '22978dd78298791b9244668c9f5a364566be695b'
	}

	def test_run(self):
		"""
		Тест для функции run()
		:return: None
		"""
		count = 5
		obj = {'a': 1}
		events = [obj] * count  # [obj, obj, ...]
		long_pool_listen_mock = Mock()
		long_pool_listen_mock.listen = Mock(return_value=events)

		with patch('bot.vk_api.VkApi'):
			with patch('bot.VkBotLongPoll', return_value=long_pool_listen_mock):
				bot = Bot('', '')
				bot._on_event = Mock()
				bot.run()

				bot._on_event.assert_called()
				bot._on_event.assert_any_call(obj)
				assert bot._on_event.call_count == count

	def test_on_event(self):
		event = VkBotMessageEvent(raw=self.RAW_EVENT)

		send_mock = Mock()

		with patch('bot.vk_api.VkApi'):
			with patch('bot.VkBotLongPoll'):
				bot = Bot('', '')
				bot.api = Mock()
				bot.api.messages.send = send_mock
				bot._on_event(event)

		send_mock.assert_called_once()
		send_mock.assert_called_once_with(
				message='Ты отправил -> ' + self.RAW_EVENT['object']['message']['text'],
				random_id=ANY,
				peer_id=self.RAW_EVENT['object']['message']['peer_id']
			)
