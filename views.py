from em_fw import render


# page controller
def index_view(request):
    return '200 OK', render('index.html', smth=request.get('1', None))


def abc_view(request):
    return '200 OK', 'abc'
