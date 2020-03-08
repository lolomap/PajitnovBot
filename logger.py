import os
import logging
import datetime
import uuid
import smtplib
from pprint import pformat
from vk_api.bot_longpoll import VkBotEvent


class Log:

    def __init__(self, **var):
        self.action = ''
        self.sender = ''
        self.var = var
        self.status = ''
        self.time = str(datetime.datetime.now().time())
        self.id = str(uuid.uuid1())

    def get_string(self):
        res = ''
        res += 'UUID: ' + self.id + '\n'
        res += 'TIME  ' + self.time + '\n'
        res += 'Action: ' + self.action + '\n'
        if self.sender is not None:
            res += 'Object: ' + str(self.sender) + '\n'
        res += 'Status: ' + self.status + '\n'
        res += 'Variables:' + '\n'

        for key, value in self.var.items():
            if isinstance(value, VkBotEvent):
                str_event = pformat(value)
                print(str_event)
                self.var[key] = str_event
        res += pformat(self.var)
        # res += self.var
        '''
        for key, value in self.var.items():
            res += '{0}: {1}\n'.format(key, value)
        '''
        return res

    def log_var(self, **var):
        for key in var.keys():
            self.var[key] = var[key]


class Logger:

    def __init__(self, dir_name, level, notification=None):
        self.notification = notification
        self.smtp_obj = smtplib.SMTP('smtp.yandex.ru', 587)
        self.smtp_obj.starttls()
        self.smtp_obj.login('botlogger@yandex.ru', 'cool_0789123')

        self.crashlog_directory = 'logs/Crashlogs/'
        self.crashlogger = logging.getLogger('CRASHES')
        self.crashlogger.setLevel(logging.INFO)

        self.log_directory = 'logs/'+dir_name + '/'
        self.dir_name = dir_name
        self.logger = logging.getLogger(self.dir_name)
        self.level = level
        if self.level.lower() == 'info':
            self.logger.setLevel(logging.INFO)
        elif self.level.lower() == 'warning':
            self.logger.setLevel(logging.WARNING)
        elif self.level.lower() == 'error':
            self.logger.setLevel(logging.ERROR)
        elif self.level.lower() == 'critical':
            self.logger.setLevel(logging.CRITICAL)
        elif self.level.lower() == 'debug':
            self.logger.setLevel(logging.DEBUG)
        else:
            raise Exception('LogLevelNameException')

    def log_info(self, log):
        if self.level != 'info':
            raise Exception('LogLevelDoesNotMatch')
        fn = self.log_directory + str(datetime.datetime.now().date())+'.log'
        cfn = self.crashlog_directory + str(datetime.datetime.now().date())+'.log'
        file = logging.FileHandler(fn, encoding='utf-8')
        crash_file = logging.FileHandler(cfn, encoding='utf-8')
        self.logger.addHandler(file)
        self.crashlogger.addHandler(crash_file)

        self.logger.info('\n' + log.get_string())

        if log.status.lower() == 'exception':
            self.crashlogger.info('\n'+log.get_string())
            os.system('python logreader.py ' + fn + ' ' + log.id)
            # if self.notification is not None:
            # self.smtp_obj.sendmail('botlogger@yandex.ru', self.notification, 'EXCEPTION IN PROGRAM: '+log.id)

    def set_directory(self, directory):
        self.log_directory = directory

