class Application:
    def __init__(self, urls: dict, fronts: list):
        self.urls = urls
        self.fronts = fronts

    def __call__(self, environ, start_response):
        path = environ['PATH_INFO']
        if not path.endswith('/') and '.' not in path.split('/')[-1]:
            path = f'{path}/'
        view = self.urls.get(path, self.default_not_found)

        request = {}
        for front in self.fronts:
            front(request)

        code, body = view(request)
        start_response(code, [('Content-Type', 'text/html')])
        return body.encode('utf-8')

    @staticmethod
    def default_not_found(request):
        return '404 NOT FOUND', '404 page not found'
