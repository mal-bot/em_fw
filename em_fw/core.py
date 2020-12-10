from pprint import pprint

class Application:
    def __init__(self, urls: dict, fronts: list) -> None:
        self.urls = urls
        self.fronts = fronts

    def __call__(self, environ: dict, start_response) -> bytes:
        # pprint(environ)
        path = environ['PATH_INFO']
        if (not path.endswith('/')) and ('.' not in path.split('/')[-1]):
            path = f'{path}/'

        method = environ['REQUEST_METHOD']

        wsgi_input_params = self.get_wsgi_input_data(environ)
        wsgi_input_params = self.parse_wsgi_input_data(wsgi_input_params)

        query_string_params = environ['QUERY_STRING']
        query_string_params = self.parse_input_data(query_string_params)

        view = self.urls.get(path, self.default_not_found)

        request = {}
        if view != self.default_not_found:
            request.update({
                'method': method,
                'wsgi_input_params': wsgi_input_params,
                'query_string_param': query_string_params,
            })

            for front in self.fronts:
                front(request)

        code, body = view(request)
        start_response(code, [('Content-Type', 'text/html')])
        return body.encode('utf-8')

    @staticmethod
    def default_not_found(request: dict) -> tuple:
        return '404 NOT FOUND', '404 page not found'

    @staticmethod
    def get_wsgi_input_data(environ: dict) -> bytes:
        content_length = int(environ.get('CONTENT_LENGTH', 0))
        data = environ['wsgi.input'].read(content_length)
        return data

    def parse_wsgi_input_data(self, data: bytes) -> dict:
        result = {}
        if data:
            data_str = data.decode(encoding='utf-8')
            result = self.parse_input_data(data_str)
        return result

    @staticmethod
    def parse_input_data(data: str) -> dict:
        if data:
            params = data.split('&')
            result = map(lambda x: x.split('='), params)
            return dict(result)
        else: 
            return {}
