# import pprint
from em_fw import Application
import views


urls = {
    '/': views.index_view,
    '/contacts/': views.contacts_view,
}


def front_1(request):
    request['front_1'] = 'front_1'


def front_2(request):
    request['front_2'] = 'front_2'


fronts = [front_1, front_2]

application = Application(urls, fronts)

#
# uwsgi --http :8000 --wsgi-file app
