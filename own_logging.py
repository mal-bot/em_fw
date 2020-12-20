from reusepatterns.singletones import SingletonByName


class Logger(metaclass=SingletonByName):
    @staticmethod
    def log(text):
        print(f'log => {text}')

# декоратор
def debug(func):
    def inner(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print('DEBUG-------->', func.__name__, end - start)
        return result

    return inner