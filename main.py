# import pprint

from em_fw import Application, render, EmFwApplication
from own_logging import Logger
from models import TrainingSite


site = TrainingSite()
logger = Logger('main')


def front_1(request):
    request['front_1'] = 'front_1'


def front_2(request):
    request['front_2'] = 'front_2'


fronts = [front_1, front_2]
urls = {}

# application = Application(urls, fronts)
application = EmFwApplication(urls, fronts)
