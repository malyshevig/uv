import telebot, logging
from typing import Optional, Callable, Any
from telebot.types import Document, Message
from loader import Download, Task
import sys
import threading, queue

# user = "397071083"
# name = "iml"
#token = "6610941656:AAHrCB_BSZsxnV-rouK8Zh0X4e3LSG8-FOo"
logging.basicConfig(stream=sys.stdout, encoding='utf-8', format='%(asctime)s %(levelname)s %(message)s',
                    level=logging.INFO)


class Bot:

    def __init__(self, token, output):
        self.task_num = 1
        self.q = queue.Queue()
        self.token = token
        self.output = output

        self.bot = telebot.TeleBot(f'{self.token}')
        text_handle: Callable[[Any], None] = lambda msg: self.get_text_message(msg)
        doc_handle: Callable[[Any], None] = lambda msg: self.get_doc(msg)

        self.bot.message_handler(content_types=['text'])(text_handle)
        self.bot.message_handler(content_types=['document'])(doc_handle)

    def queue(self) -> queue:
        return self.q

    def run(self):
        logging.info("Bot started polling")
        self.bot.polling(none_stop=True, interval=0)

    def get_text_message(self, message: Optional[Message]):
        try:
            logging.info(f" {message.from_user} recieved = {message}")
            # s = Download(message.text)
            t = self.task_num
            self.task_num = self.task_num + 1

            link = message.text
            self.q.put(Task(id=f"task {t}", link=link, msg=message, target=self.output))

            logging.info(f" queue: {self.q.qsize()}")
            #            if message.text.endswith(".torrent"):
            #                logging.info(f" {message.from_user} recieved torrent URL = {message.text}")
            #                self.hand.process_url(message.text)

            self.bot.send_message(message.from_user.id, f"added task {t} {link}")

        except Exception as err:
            logging.error(err)

    def get_doc(self, message: Optional[Document]):
        try:
            if not self.hand.auth(message.from_user.id):
                return
            logging.info(f" {message.from_user} recieved file {message.document}")

            file_name: str = message.document.file_name
            if not file_name.endswith(".torrent"):
                logging.info(f" {message.from_user} unknown type of file {message.document}")
                self.bot.send_message(message.from_user.id, f"Dont know file type of {file_name}")

            self.bot.send_message(message.from_user.id, "Processing started")

        except Exception as err:
            logging.error(err)


class Downloader(threading.Thread):
    def __init__(self, q: queue.Queue, bot: Bot):
        super().__init__()
        self.q = q
        self.bot = bot

    def run(self):
        while True:
            try:
                logging.info(f"queue {self.q.qsize()}")
                t: Task = self.q.get()
                msg: Message = t.msg
                logging.info(f"downloading {msg.text}")
                s = Download(msg.text,t.target)
                logging.info(f"downloading res {s}")
                self.bot.bot.send_message(msg.from_user.id, f"{t.id} {s} {msg.text}")
                logging.info(f"result task:{t} {s} {msg.text}")
            except BaseException as ex:
                logging.error(f"downloading error: {ex}")



