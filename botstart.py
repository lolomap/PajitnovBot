# -*- coding: utf-8 -*-
import VK_API
# import network
from logger import Logger, Log
import sys
from parsing import ParsingFile
import re


def main():
    regex = r'(?:https?:\/\/)?(?:[\w\.]+)\.(?:[a-z]{2,6}\.?)(?:\/[\w\.]*)*\/?'
    logger = Logger('Main', 'info', 'lolomap07@yandex.ru')
    api = VK_API.VK_API(sys.argv[1], sys.argv[2])
    cleaned = ''
    link = ''
    url = ''
    while True:
        for event in api.longpoll.listen():
            if api.get_event_type(event) == 'MESSAGE_NEW':
                log = Log(event=event)
                log.action = 'main'

                try:
                    msg_text = event.obj.text
                    log.log_var(msg_text=msg_text)
                    if 'attachments' in event.obj.keys():
                        if event.obj['attachments'][0]['type'] == 'link':
                            url = event.obj['attachments'][0]['link']['url']

                    if msg_text == sys.argv[3]:
                        log.log_var(action='STOP PROGRAM', sender='User')
                        log.status = 'OK'
                        logger.log_info(log)
                        # api.mark_msg_read(event.obj['id'], event.obj['peer_id'])
                        exit('Stopped by user')
                    # and event.obj['payload'] == "{\"button\": \"1\"}"
                    if msg_text == 'Читать дальше':
                        if len(cleaned) < 1401:
                            api.write_msg(event, cleaned)
                        else:
                            api.write_msg(event, cleaned[:1400]+'...',
                                          keyboard=api.create_keyboard('Читать полностью в источнике', url=link))
                        log.status = 'OK'
                        logger.log_info(log)
                        break

                    if url == '':
                        url_f = re.search(regex, msg_text)
                        if url_f is not None:
                            url = url_f.group(0)
                        else:
                            break

                        if url.find('http://') < 0:
                            url = 'http://'+url

                    parsing = ParsingFile()
                    log.log_var(parsing=parsing)
                    cleaned = parsing.clean_html(url)
                    if cleaned == '' or cleaned is None:
                        raise Exception('Cleaning error')
                    log.log_var(cleaned=cleaned)

                    if len(cleaned) < 501:
                        api.write_msg(event, cleaned)
                    else:
                        link = msg_text
                        api.write_msg(event, cleaned[:500]+'...', keyboard=api.create_keyboard('Читать дальше'))

                    log.status = 'OK'
                except Exception as e:
                    log.status = 'Exception'
                    log.log_var(exception_info=e)
                    # api.write_msg(event, 'Произошла ошибка на сервере.')

                logger.log_info(log)


if __name__ == '__main__':
    main()
