from jinja2 import Template, FileSystemLoader
from jinja2.environment import Environment
# import os


# def render(template_name, folder='templates', **kwargs):
#     path = os.path.join(folder, template_name)
#     with open(path, encoding='utf-8') as f:
#         template = Template(f.read())
#     return template.render(**kwargs)

def render(template_name, folder='templates', **kwargs):
    # создаем окружение jinja2
    env = Environment()
    # добавляем загрузчик шаблонов, указываем папку folder
    env.loader = FileSystemLoader([folder])
    # считываем шаблон по имени
    template = env.get_template(template_name)
    # рендерим шаблон
    return template.render(**kwargs)
