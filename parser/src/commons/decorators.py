import time

from flasgger import swag_from


def api_doc(func):
    class_name = str(func.__qualname__)
    method_name = str(func.__name__)

    separator_index = class_name.rindex("Resource.{0}".format(method_name))

    file_name = "{0}_{1}".format(class_name[:separator_index], method_name)

    @swag_from("../../doc/{0}.yml".format(file_name))
    def wrapper_fn(*args, **kwargs):
        return func(*args, **kwargs)

    return wrapper_fn


def elapsed_time(method):
    def timed(*args, **kw):
        class_name = str(method.__qualname__)
        # method_name = str(method.__name__)

        ts = time.time()
        result = method(*args, **kw)
        te = time.time()
        if 'log_time' in kw:
            name = kw.get('log_name', class_name.upper())
            kw['log_time'][name] = int((te - ts) * 1000)
        else:
            print('%r  %2.2f ms' %(class_name, (te - ts) * 1000))
        return result

    return timed
