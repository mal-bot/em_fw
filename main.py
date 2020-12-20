# import pprint
import views
from em_fw import Application, render
from own_logging import Logger
from models import TrainingSite


site = TrainingSite()
logger = Logger('main')

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


def index_view(request):
    return '200 OK', render('index.html', smth=request.get('front_2', None))


def contacts_view(request):
    if request['method'] == 'POST':
        wsgi_input_params = request['wsgi_input_params']
        with open('fake_db.txt', 'a', encoding='utf-8') as f:
            f.write(f"{wsgi_input_params['email']}::"
                    f"{wsgi_input_params['title']}::"
                    f"{wsgi_input_params['text']}\n")
    return '200 OK', render('contacts.html')


def main_view(request):
    logger.log('Список курсов')
    return '200 OK', render('course_list.html', objects_list=site.courses)


def create_course(request):
    categories = site.categories
    if request['method'] == 'POST':
        data = request['wsgi_input_params']
        name = data['name']
        category_id = data.get('category_id')
        print(category_id)
        category = None
        if category_id:
            category = site.find_category_by_id(int(category_id))
            course = site.create_course('record', name, category)
            site.courses.append(course)
    return '200 OK', render('create_course.html')
    # else:
    #     categories = site.categories
    #     return '200 OK', render('create_course.html', categories=categories)


def create_category(request):
    if request['method'] == 'POST':
        # метод пост
        data = request['data']
        # print(data)
        name = data['name']
        category_id = data.get('category_id')

        category = None
        if category_id:
            category = site.find_category_by_id(int(category_id))

        new_category = site.create_category(name, category)
        site.categories.append(new_category)
        return '200 OK', render('create_category.html')
    else:
        categories = site.categories
        return '200 OK', render('create_category.html', categories=categories)


@application.add_route('/copy-course/')
def copy_course(request):
    request_params = request['request_params']
    # print(request_params)
    name = request_params['name']
    old_course = site.get_course(name)
    if old_course:
        new_name = f'copy_{name}'
        new_course = old_course.clone()
        new_course.name = new_name
        site.courses.append(new_course)
    return '200 OK', render('course_list.html', objects_list=site.courses)


@application.add_route('/category-list/')
def category_list(request):
    logger.log('Список категорий')
    return '200 OK', render('category_list.html', objects_list=site.categories)
