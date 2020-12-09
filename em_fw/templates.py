from jinja2 import Template
import os


def render(template_, folder='templates', **kwargs):
    path = os.path.join(folder, template_)
    with open(path, encoding='utf-8') as f:
        template = Template(f.read())
    return template.render(**kwargs)
