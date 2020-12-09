# import pprint
from em_fw import Application
import views


urls = {
    '/': views.index_view,
    '/abc/': views.abc_view
}


def front_1(request):
    request['1'] = '1'


def front_2(request):
    request['2'] = '2'


fronts = [front_1, front_2]

application = Application(urls, fronts)

#
# uwsgi --http :8000 --wsgi-file app
