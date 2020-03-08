import newspaper
from logger import Log, Logger


class ParsingFile:

    def __init__(self, html=None):
        self.logger = Logger('Parsing', 'info')
        self.html = html

    def clean_html(self, url):
        log = Log()
        log.sender = self
        log.action = 'clean_html'
        res = None
        log.log_var(url=url, res=res)

        try:
            article = newspaper.Article(url)
            log.log_var(article=article)
            article.download()
            article.parse()
            cleaned = article.text
            res = cleaned
            log.log_var(res=res)
            log.status = 'OK'
        except newspaper.ArticleException as e:
            log.log_var(exception_info=e)
            log.status = 'Exception'

        self.logger.log_info(log)
        return res

    def get_text(self):
        pass

    def get_tags(self, tag):
        pass


