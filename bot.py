import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from random import randint
import logging

try:
	import settings
except ImportError:
	exit('DO cp settings.py.default settings.py and set TOKEN and GROUP_ID')

bot_logger = logging.getLogger('bot_logger')
bot_logger.setLevel(logging.DEBUG)


def configure_logging():
	console_formatter = logging.Formatter('%(levelname)s - %(message)s')
	stream_handler = logging.StreamHandler()
	stream_handler.setFormatter(console_formatter)
	stream_handler.setLevel(logging.INFO)
	bot_logger.addHandler(stream_handler)

	file_formatter = logging.Formatter('[%(asctime)s] - %(levelname)s - %(message)s', '%d-%m-%Y, %H:%M:%S')
	file_handler = logging.FileHandler('bot_log.log', mode='a', encoding='utf8')
	file_handler.setFormatter(file_formatter)
	file_handler.setLevel(logging.DEBUG)
	bot_logger.addHandler(file_handler)


class Bot:
	"""
	Echo bot для vk.com

	Use Python3.9.4
	"""

	def __init__(self, group_id, token):
		"""

		:param group_id: group id из группы vk.com
		:param token: Ключ api для группы vk.com
		"""
		self.token = token
		self.group_id = group_id
		self.vk = vk_api.VkApi(token=token)
		self.long_pool = VkBotLongPoll(self.vk, self.group_id)
		self.api = self.vk.get_api()

	def run(self):
		"""Запуск бота."""
		for event in self.long_pool.listen():
			try:
				self._on_event(event)
			except Exception:
				bot_logger.exception('Ошибка в обработке')

	def _on_event(self, event: VkBotEventType):
		"""
		Отправляет сообщение назад, если это текст.
		:param event: VkBotMessageEvent object
		:return: None
		"""
		if event.type == VkBotEventType.MESSAGE_NEW:
			response_message = f"Ты отправил -> {event.object.message['text']}"
			bot_logger.debug('Отправляем сообщение!')
			self.api.messages.send(
				message=response_message,
				random_id=randint(0, 2 ** 20),
				peer_id=event.object.message['peer_id']
			)
		else:
			bot_logger.info(f'Этот бот пока не умеет работать с такими событиями как {event.type}')


if __name__ == '__main__':
	configure_logging()
	vk_bot = Bot(group_id=settings.GROUP_ID, token=settings.TOKEN)
	vk_bot.run()
