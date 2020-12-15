from em_fw import render

# page controllers


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
