from .celery import app
from celery.utils.log import get_task_logger
from .models import News
from .parser import YandexOzonParser, yandexLink, ozonLink
import requests
import httpx
from requests import post, get
import hashlib

logger = get_task_logger(__name__)

# Celery periodic task for update news in database
@app.task
def update_news():
    # Read html using http client and feed it to parser
    client = httpx.Client(http2=True)
    parser = YandexOzonParser(client)
    ozonData = client.post(ozonLink + "/news").text
    yandexData = client.get(yandexLink + "/partners/news").text
    parser.feed(str(ozonData))
    parser.feed(str(yandexData))
    news = parser.get_news()
    amount = 0
    # Calculate hash for each news and check for duplicates
    for n in news:
        n['id'] = hashlib.sha1(n['title'].encode('utf-8')).hexdigest()
        try:
            dup = News.objects.get(id = n['id'])
            if(dup is not None):
                continue
        except News.DoesNotExist:
            pass
        # Write new model in database
        new = News(**n)
        new.save()
        amount += 1
    news.clear()
    return amount