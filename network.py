# -*- coding: utf-8 -*-
import requests
from logger import Logger, Log

logger = Logger('Network', 'info', 'lolomap07@yandex.ru')


def get_site(url):
    log = Log()
    log.action = 'get_site'
    log.log_var(url=url)
    response = None
    log.log_var(response=response)
    try:
        if url.find('http') < 0:
            url = 'http://'+url
        response = requests.get(url)
        log.log_var(response=response)
        log.status = 'OK'
    except requests.RequestException as e:
        log.status = 'Exception'
        log.log_var(exception_info=e)

    logger.log_info(log)
    return response
