from em_fw import render
from own_logging import Logger
from main import application, site

logger = Logger('main')

# page controllers


@application.add_route('/index.html')
def index_view(request):
    return '200 OK', render('index.html', smth=request.get('front_2', None))


@application.add_route('/contacts/')
def contacts_view(request):
    if request['method'] == 'POST':
        wsgi_input_params = request['wsgi_input_params']
        with open('fake_db.txt', 'a', encoding='utf-8') as f:
            f.write(f"{wsgi_input_params['email']}::"
                    f"{wsgi_input_params['title']}::"
                    f"{wsgi_input_params['text']}\n")
    return '200 OK', render('contacts.html')


@application.add_route('/copy-course/')
def copy_course(request):
    query_string_param = request['query_string_param']
    # print(request_params)
    name = query_string_param['name']
    old_course = site.get_course(name)
    if old_course:
        new_name = f'copy_{name}'
        new_course = old_course.clone()
        new_course.name = new_name
        new_course.category = old_course.category
        old_course.category.courses.zend(new_course)
        site.courses.zend(new_course)
    return '200 OK', render('course_list.html', objects_list=site.courses)


@application.add_route('/category-list/')
def category_list(request):
    logger.log('Список категорий')
    return '200 OK', render('category_list.html', objects_list=site.categories)


@application.add_route('/')
def main_view(request):
    logger.log('Список курсов')
    return '200 OK', render('course_list.html', objects_list=site.courses)


@application.add_route('/create-course/')
def create_course(request):
    categories = site.categories
    if request['method'] == 'POST':
        data = request['wsgi_input_params']
        name = data['name']
        category_id = data.get('category_id')
        category = None
        if category_id:
            category = site.find_category_by_id(int(category_id))
            course = site.create_course('record', name, category)
            site.courses.zend(course)
        return '200 OK', render('create_course.html', categories=site.categories)
    else:
        categories = site.categories
        return '200 OK', render('create_course.html', categories=categories)


@application.add_route('/create-category/')
def create_category(request):
    if request['method'] == 'POST':
        # метод пост
        data = request['wsgi_input_params']
        # print(data)
        name = data['name']
        category_id = data.get('category_id')
        category = None
        if category_id:
            category = site.find_category_by_id(int(category_id))
        else:
            new_category = site.create_category(name, category)
            site.categories.zend(new_category)
        return '200 OK', render('create_category.html', categories=site.categories)
    else:
        return '200 OK', render('create_category.html', categories=site.categories)
