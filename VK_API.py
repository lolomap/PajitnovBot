# -*- coding: utf-8 -*-

import requests

from logger import Logger, Log

import vk_api
import vk_api.bot_longpoll as api_longpoll


class VK_API:

    def __init__(self, group_token, group_id=None):
        self.vk_session = None
        self.longpoll = None
        self.class_logger = Logger('VK_API', 'info', 'lolomap07@yandex.ru')
        if group_token is not None and group_id is not None:
            self.create_session(group_token, group_id)

    def create_session(self, group_token, group_id):
        log = Log()
        log.sender = self
        log.action = 'create_session'
        log.log_var(group_id=group_id)

        try:
            api = vk_api.VkApi(token=group_token)
            log.log_var(api=api)

            self.longpoll = api_longpoll.VkBotLongPoll(api, group_id)
            self.vk_session = api.get_api()
            log.log_var(longpoll=self.longpoll, vk_session=self.vk_session)

            log.status = 'OK'
        except vk_api.VkApiError as e:
            log.status = 'Exception'
            log.log_var(exception_info=e)

        self.class_logger.log_info(log)

    def get_user(self, user_id):
        log = Log()
        log.action = 'get_user'
        log.sender = self
        log.log_var(user_id=user_id)
        res = None
        log.log_var(res=res)
        try:
            res = self.vk_session.users.get(user_ids=user_id)
            log.log_var(res=res)
            log.status = 'OK'
        except vk_api.VkApiError as e:
            log.status = 'Exception'
            log.log_var(exception_info=e)

        self.class_logger.log_info(log)
        return res

    def get_conversation(self, peer_id):
        log = Log()
        log.action = 'get_conversation'
        log.sender = self
        log.log_var(peer_id=peer_id)
        res = None
        log.log_var(res=res)

        try:
            res = self.vk_session.messages.getConversationsById(peer_id=peer_id)['items']
            log.log_var(res=res)
            log.status = 'OK'
        except vk_api.VkApiError as e:
            log.status = 'Exception'
            log.log_var(exception_info=e)

        self.class_logger.log_info(log)
        return res

    def get_conversation_members(self, peer_id):
        log = Log()
        log.action = 'get_conversation_members'
        log.sender = self
        log.log_var(peer_id=peer_id)
        res = None
        log.log_var(res=res)

        try:
            res = self.vk_session.messages.getConversationMembers(peer_id=peer_id)['profiles']
            log.log_var(res=res)
            log.status = 'OK'
        except vk_api.VkApiError as e:
            log.status = 'Exception'
            log.log_var(exception_info=e)

        self.class_logger.log_info(log)
        return res

    def get_conversations(self):
        log = Log()
        log.action = 'get_conversations'
        log.sender = self
        res = None
        log.log_var(res=res)
        try:
            res = self.vk_session.messages.getConversations()['items']
            log.log_var(res=res)
            log.status = 'OK'
        except vk_api.VkApiError as e:
            log.status = 'Exception'
            log.log_var(exception_var=e)

        self.class_logger.log_info(log)
        return res

    def get_event_type(self, event):
        log = Log()
        log.action = 'get_event_type'
        log.sender = self
        log.log_var(event=event)
        res = None
        log.log_var(res=res)

        try:
            if event.type == api_longpoll.VkBotEventType.MESSAGE_NEW:
                res = 'MESSAGE_NEW'
            elif event.type == api_longpoll.VkBotEventType.MESSAGE_TYPING_STATE:
                res = 'MESSAGE_TYPING_STATE'
            else:
                res = 'UNKNOWN'
            log.log_var(res=res)
            log.status = 'OK'
        except vk_api.VkApiError as e:
            log.status = 'Exception'
            log.log_var(exception_ifo=e)

        self.class_logger.log_info(log)
        return res

    def write_msg(self, session_event, text, sticker_id=None, picture=None, keyboard=None):
        log = Log()
        log.action = 'write_msg'
        log.sender = self
        log.log_var(event=session_event, text=text, sticker_id=sticker_id, picture=picture, keyboard=keyboard)
        res = None
        log.log_var(res=res)

        try:
            data = {'peer_id': session_event.obj['peer_id'], 'random_id': session_event.obj['random_id']}

            if text and picture is None:
                data['message'] = text
            if sticker_id is not None:
                data['sticker_id'] = sticker_id
            if picture is not None:
                photo_file = self.vk_session.photos.getMessagesUploadServer(
                    peer_id=session_event.obj['peer_id'])
                log.log_var(photo_file=photo_file)

                r_data = {'photo': open('images/pitivo.jpg', 'rb')}
                log.log_var(r_data=r_data)

                photo_data = requests.post(photo_file['upload_url'], files=r_data).json()
                log.log_var(photo_data=photo_data)

                photo = self.vk_session.photos.saveMessagesPhoto(server=photo_data['server'],
                                                                 photo=photo_data['photo'],
                                                                 hash=photo_data['hash'])[0]
                log.log_var(photo=photo)

                data['attachment'] = 'photo{0}_{1}'.format(photo['owner_id'], photo['id'])
                data['message'] = text
            if keyboard is not None:
                data['keyboard'] = keyboard

            # res = self.vk_session.messages.send(data)
            if keyboard is None:
                res = self.vk_session.messages.send(peer_id=data['peer_id'], message=data['message'],
                                                    random_id=data['random_id'])
            else:
                res = self.vk_session.messages.send(peer_id=data['peer_id'], message=data['message'],
                                                    keyboard=data['keyboard'], random=data, random_id=data['random_id'])

            log.log_var(res=res)
            log.status = 'OK'
        except vk_api.VkApiError as e:
            log.status = 'Exception'
            log.log_var(exception_info=e)

        self.class_logger.log_info(log)
        return res

    def create_keyboard(self, button_text, url=None):
        log = Log(button_text=button_text)
        log.action = 'create_keyboard'
        log.sender = self
        '''
        keyboard = "{\"inline\": true, " \
                   "\"buttons\": [[{\"action\": {\"type\": \"text\"," \
                   " \"payload\": \"{\"button\": \"1\"}\"," \
                   "\"label\": \""+button_text+"\"}, \"color\": \"positive\"}]]}"
        '''
        if url is None:
            keyboard = "{\"inline\": true, " \
                       "\"buttons\": [[{\"action\": {\"type\": \"text\"," \
                       "\"label\": \"" + button_text + "\"}, \"color\": \"positive\"}]]}"
        else:
            keyboard = "{\"inline\": true, " \
                       "\"buttons\": [[{\"action\": {\"type\": \"open_link\"," \
                       "\"label\": \"" + button_text + "\", \"link\": \""+url+"\"}}]]}"
        log.log_var(keyboard=keyboard)
        log.status = 'OK'
        self.class_logger.log_info(log)
        return keyboard

    def edit_msg(self, session_event, msg_id, text):
        log = Log()
        log.action = 'edit_msg'
        log.sender = self
        log.log_var(event=session_event, msg_id=msg_id, text=text)

        try:
            try:
                self.vk_session.messages.edit(
                    peer_id=session_event.obj['peer_id'],
                    message=text,
                    message_id=msg_id
                )
            except vk_api.VkApiError:
                self.write_msg(session_event, text)
            log.status = 'OK'
        except vk_api.VkApiError as e:
            log.status = 'Exception'
            log.log_var(exception_info=e)

        self.class_logger.log_info(log)

    def mark_msg_read(self, msg_id, peer_id):
        log = Log()
        log.action = 'mark_msg_read'
        log.sender = self
        log.log_var(msg_id=msg_id, peer_id=peer_id)
        res = 0
        log.log_var(res=res)
        try:
            res = self.vk_session.messages.markAsRead(msg_id, peer_id)
            log.log_var(res=res)
            log.status = 'OK'
        except vk_api.VkApiError as e:
            log.status = 'Exception'
            log.log_var(exception_info=e)
        self.class_logger.log_info(log)
        return res
