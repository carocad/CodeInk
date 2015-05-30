
import math
from radon import metrics
from codeink.atelier import secretary
filterfalse = safe_import(origin='itertools', funk1='filterfalse', funk2='ifilterfalse')

def check_complexity(filepath, minsize=80):
    with open(filepath) as source:
        return check_snippet_complexity(source.read(), minsize)

def check_snippet_complexity(strcode, initsize=50):
    size = initsize # minimum size
    cyclom, maintainability = calculate_complexity(strcode)
    size += math.pow(cyclom, 2)

    hsl = secretary.value_to_HSL(maintainability)
    color = secretary.hsl_to_str(hsl)
    return size, color

def calculate_complexity(sourcecode):
    halstead, cyclom, lloc, pcom = metrics.mi_parameters(sourcecode, count_multi=False)
    maintainability = metrics.mi_compute(halstead, cyclom, lloc, pcom)
    return cyclom, maintainability

def compute_edges(filepath, base, found_imports, missing_imports=None):
    for module in found_imports:
        if include_module(module):
            yield (filepath, module.__file__)
    if missing_imports:
        yield (filepath, base)

def include_module(module):
    return (module.__file__ is not None # builtin import
            and not module.__file__.endswith('__init__.py') # pkg import
            #and filepath != module.__file__
            and module.__name__ != '__main__') # self module

def filtertype(objtype, iterable, filterfalse=False):
    filterfn = filter if not filterfalse else filterfalse
    return filterfn(lambda element: isinstance(element, objtype), iterable)


def safe_import(origin, funk1, funk2):
    """Safely import a function whose name was changed from a module whose name was not
    Example:
    # instead of writting this
        try:
            from itertools import filterfalse
        except ImportError:
            from itertools import ifilterfalse as filterfalse
    # write this
        filterfalse = safe_import('itertools', 'filterfalse', 'ifilterfalse')
    """
    try:
        hook = __import__(origin, globals(), locals(), [funk1], 0)
        return getattr(hook, funk1)
    except:
        hook = __import__(origin, globals(), locals(), [funk2], 0)
        return getattr(hook, funk2)

