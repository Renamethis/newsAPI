from html.parser import HTMLParser
from enum import Enum, auto
import datetime

# News page links
ozonLink = "https://seller.ozon.ru"
yandexLink = "https://market.yandex.ru"

# Content type enum
class ContentType(Enum):
    DATE = auto()
    TITLE = auto()
    DESCRIPTION = auto()
    MARK = auto()

# Yandex Ozon Parser
class YandexOzonParser(HTMLParser):

    __type = None
    __news = []
    __i = 0
    __mark_container = []
    __open = False
    __startCount = 0
    __endCount = 0
    __amount = 0

    def __init__(self, client):
        super().__init__()
        self.__client = client

    def feed(self, arg):
        self.__amount = 0
        super().feed(arg)

    # Handle opened html-tag
    def handle_starttag(self, tag, attrs):
        if(self.__amount < 10):
            if(self.__open):
                self.__startCount += 1
            if(len(attrs) and len(attrs[0])):
                if(tag == "a" and len(attrs) > 1):
                    # Handle news url and run page parser
                    if(attrs[1][1] == "news-card__link"):
                        self.__news[self.__i]["uri"] = attrs[0][1]
                        pageParser = PageParser()
                        data = self.__client.post(ozonLink + self.__news[self.__i]["uri"]).text
                        pageParser.feed(data)
                        content, _ = pageParser.get_data()
                        self.__news[self.__i]["content"] = content
                    elif(attrs[0][1] == "link link_theme_normal news-list__item-active i-bem"):
                        self.__news[self.__i]["uri"] = attrs[2][1]
                        pageParser = PageParser()
                        data = self.__client.get(yandexLink + self.__news[self.__i]["uri"]).text
                        pageParser.feed(data)
                        content, tags = pageParser.get_data()
                        self.__mark_container = self.__mark_container + tags
                        tags.clear()
                        self.__news[self.__i]["content"] = content
                else:
                    match attrs[0][1]:
                        # Handle start tag of news container item
                        case "news-card" | "news-list__item":
                            self.__startCount += 1
                            self.__open = True
                            self.__news.append({})
                            if(attrs[0][1] == "news-card"):
                                self.__mark_container.append('Ozon')
                            else:
                                self.__mark_container.append('Yandex')
                        # Handle date
                        case "news-card__date" | "news-list__item-date":
                            self.__type = ContentType.DATE
                        # Handle title
                        case "news-card__title" | "news-list__item-header":
                            self.__type = ContentType.TITLE
                        # Handle marks
                        case "news-card__mark":
                            self.__type = ContentType.MARK
                        case _:
                            self.__type = None

    # Handle data inside html tag
    def handle_data(self, data):
        if(self.__amount < 10):
            if(self.__type != None):
                match self.__type:
                    case ContentType.DATE:
                        # Convert date in datetime format
                        try:
                            self.__news[self.__i]["pdate"] = datetime.datetime.strptime(data, "%d %B %Y")
                        except ValueError:
                            t = datetime.datetime.strptime(data, "%d %B")
                            year = datetime.datetime.now().year
                            t = t.replace(year=year)
                            self.__news[self.__i]["pdate"] = t
                    case ContentType.TITLE:
                        # Read title
                        self.__news[self.__i]["title"] = data.strip()
                    case ContentType.MARK:
                        # Append tag
                        self.__mark_container.append(data)
            self.__type = None

    # Handle html tag closing
    def handle_endtag(self, tag):
        if(self.__amount < 10):
            if(self.__open):
                self.__endCount += 1
                # If item container tag was closed then model is written
                if(self.__startCount == self.__endCount and self.__startCount):
                    self.__news[self.__i]["tags"] = self.__mark_container.copy()
                    self.__mark_container.clear()
                    self.__i += 1
                    self.__amount += 1
                    self.__open = False
                    self.__startCount = 0
                    self.__endCount = 0

    # Return news
    def get_news(self):
        return self.__news

# News page parser
class PageParser(HTMLParser):

    __tagsFlag = False
    __contentFlag = False
    __tags = []
    __content = ""
    __startCount = 0
    __endCount = 0

    def handle_starttag(self, tag, attrs):
        if(len(attrs) and len(attrs[0])):
            match attrs[0][1]:
                # Handle content
                case "main-layout__middle" | "new-section html-content_Ol8P9":
                    self.__contentFlag = True
                # Handle tags for Yandex
                case 'link link_theme_light-gray news-info__tag i-bem':
                    self.__tagsFlag = True
        if(self.__contentFlag):
            self.__startCount += 1
                    
    def handle_data(self, data):
        if(self.__tagsFlag):
            self.__tags.append(data[1:])
            self.__tagsFlag = False
        if(self.__contentFlag):
            self.__content += self.__format_text(data)

    def handle_endtag(self, tag):
        if(self.__contentFlag):
            self.__endCount += 1
        if(self.__startCount == self.__endCount and self.__startCount):
            self.__contentFlag = False
            self.__startCount = 0
            self.__endCount = 0
            
    # Return content and tags
    def get_data(self):
        return self.__content, self.__tags

    # Remove all html tags from content text
    def __format_text(self, text):
        result = ""
        for i in range(len(text)):
            if(text[i] == "<"):
                while(text[i] != ">"):
                    i += 1
            result += text[i]
        return result