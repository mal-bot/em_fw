# import pprint

from em_fw import Application, EmFwApplication, render
from own_logging import Logger
from models import TrainingSite, BaseSerializer, EmailNotifier, SmsNotifier
from em_fw.cbv import ListView, CreateView
from em_fw_orm import UnitOfWork
from mappers import MapperRegistry

site = TrainingSite()
logger = Logger('main')
email_notifier = EmailNotifier()
sms_notifier = SmsNotifier()
UnitOfWork.new_current()
UnitOfWork.get_current().set_mapper_registry(MapperRegistry)

site.students = MapperRegistry.get_current_mapper('student').all()
site.categories = MapperRegistry.get_current_mapper('category').all()
site.courses = MapperRegistry.get_current_mapper('course').all()


def front_1(request):
    request['front_1'] = 'front_1'


def front_2(request):
    request['front_2'] = 'front_2'


class CategoryCreateView(CreateView):
    template_name = 'create_category.html'

    def get_context_data(self):
        context = super().get_context_data()
        context['categories'] = site.categories
        return context

    def create_obj(self, data: dict):
        name = data['name']
        category_id = data.get('category_id')
        category = None
        if category_id:
            mapper = MapperRegistry.get_current_mapper('category')
            category = mapper.find_by_id(category_id)
            # category = site.find_category_by_id(int(category_id))
        new_category = site.create_category(name, category)
        site.categories.append(new_category)
        new_category.mark_new()
        UnitOfWork.get_current().commit()


class CategoryListView(ListView):
    # queryset = site.categories
    template_name = 'category_list.html'

    def get_queryset(self):
        mapper = MapperRegistry.get_current_mapper('category')
        return mapper.all()


class StudentListView(ListView):
    queryset = site.students
    template_name = 'student_list.html'

    def get_queryset(self):
        mapper = MapperRegistry.get_current_mapper('student')
        return mapper.all()


class StudentCreateView(CreateView):
    template_name = 'create_student.html'

    def create_obj(self, data: dict):
        name = data['name']
        new_obj = site.create_user('student', name)
        site.students.append(new_obj)
        new_obj.mark_new()
        UnitOfWork.get_current().commit()


class CourseListView(ListView):
    # queryset = site.categories
    template_name = 'course_list.html'

    def get_queryset(self):
        mapper = MapperRegistry.get_current_mapper('course')
        return mapper.all()


class AddStudentByCourseCreateView(CreateView):
    template_name = 'add_student.html'

    def get_context_data(self):
        context = super().get_context_data()
        context['courses'] = site.courses
        context['students'] = site.students
        return context

    def create_obj(self, data: dict):
        course_name = data['course_name']
        course = site.get_course(course_name)
        student_name = data['student_name']
        student = site.get_student(student_name)
        course.add_student(student)

class CourseCreateView(CreateView):
    template_name = 'create_course.html'

    def get_context_data(self):
        context = super().get_context_data()
        context['categories'] = site.categories
        return context

    def create_obj(self, data: dict):
        name = data['name']
        category_id = data.get('category_id')
        category = None
        if category_id:
            mapper = MapperRegistry.get_current_mapper('category')
            category = mapper.find_by_id(category_id)
            new_course = site.create_course('record', name, category)
            site.courses.append(new_course)
            new_course.category.courses.append(new_course)
            new_course.mark_new()
            UnitOfWork.get_current().commit()


fronts = [front_1, front_2]

urls = {
    '/category-list/': CategoryListView(),
    '/student-list/': StudentListView(),
    '/create-student/': StudentCreateView(),
    '/add-student/': AddStudentByCourseCreateView(),
    '/create-category/': CategoryCreateView(),
    '/course-list/': CourseListView(),
    '/create-course/': CourseCreateView()
}

application = Application(urls, fronts)
# application = EmFwApplication(urls, fronts)


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
    name = query_string_param['name']
    old_course = site.get_course(name)

    if old_course:
        new_name = f'copy_{name}'
        new_course = site.create_course('record', new_name, old_course.category)
        new_course.category.courses.append(new_course)
        new_course.mark_new()
        UnitOfWork.get_current().commit()
    site.courses = MapperRegistry.get_current_mapper('course').all()
    return '200 OK', render('course_list.html', objects_list=site.courses)



# @application.add_route('/category-list/')
# def category_list(request):
#     logger.log('Список категорий')
#     return '200 OK', render('category_list.html', objects_list=site.categories)


@application.add_route('/')
def main_view(request):
    logger.log('Список курсов')
    return '200 OK', render('course_list.html', objects_list=site.courses)


# @application.add_route('/create-course/')
# def create_course(request):
#     categories = site.categories
#     if request['method'] == 'POST':
#         data = request['wsgi_input_params']
#         name = data['name']
#         category_id = data.get('category_id')
#         category = None
#         if category_id:
#             category = site.find_category_by_id(int(category_id))
#             course = site.create_course('record', name, category)
#             course.observers.append(email_notifier)
#             course.observers.append(sms_notifier)
#             site.courses.append(course)
#         return '200 OK', render('create_course.html', categories=site.categories)
#     else:
#         categories = site.categories
#         return '200 OK', render('create_course.html', categories=categories)


# @application.add_route('/create-category/')
# def create_category(request):
#     if request['method'] == 'POST':
#         # метод пост
#         data = request['wsgi_input_params']
#         # print(data)
#         name = data['name']
#         category_id = data.get('category_id')
#         category = None
#         if category_id:
#             category = site.find_category_by_id(int(category_id))
#         else:
#             new_category = site.create_category(name, category)
#             site.categories.zend(new_category)
#         return '200 OK', render('create_category.html', categories=site.categories)
#     else:
#         return '200 OK', render('create_category.html', categories=site.categories)


@application.add_route('/api/')
def course_api(request):
    return '200 OK', BaseSerializer(site.courses).save()