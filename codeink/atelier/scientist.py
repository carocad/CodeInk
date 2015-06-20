"""General mathematic related functions"""

import math
from radon import metrics
from codeink.atelier import secretary
from codeink.parchment import tools
filterfalse = tools.safe_import(origin='itertools', funk1='filterfalse', funk2='ifilterfalse')

def get_size_color(strcode, initsize=50):
    """base on the `strcode` string, calculate its complexity
    and maintainabiliy indexes and transform those into size and
    color values.

    Args:
        strcode (str): source code to use for the calculations.
        initsize (Optional[int]): minimum value of size.
    Returns:
        tuple(int): size and color of the passed source code.

    """
    size = initsize # minimum size
    cyclom, maintainability = calculate_complexity(strcode)
    size += math.pow(cyclom, 2)

    hsl = secretary.value_to_HSL(maintainability)
    color = secretary.hsl_to_str(*hsl)
    return size, color

def calculate_complexity(sourcecode):
    """calculate the ciclomatic and maintainability index of the
    provided `source code`.

    Args:
        sourcecode (str): source code to use for the calculations.
    Returns:
        Tuple[int]: cyclomatic and maintainability index.

    """
    halstead, cyclom, lloc, pcom = metrics.mi_parameters(sourcecode, count_multi=False)
    maintainability = metrics.mi_compute(halstead, cyclom, lloc, pcom)
    return cyclom, maintainability

def compute_edges(filepath, base, found_imports, missing_imports=None):
    """base on `found_imports` list, determine which of the imported modules
    are related to each other.

    Args:
        filepath (str): absolute filepath of the module under analysis.
        base (str): The most basic node. Every unknown import will be treated
          as related to this node.
        found_imports (List[modulefinder.Module]): list of modules imported
        missing_imports (List[str]): list of names of modules not found.
    Yields:
        Tuple[str, str]: module filepath and import filepath. Note that `base`
          is used in case the module filepath is unknown.
    """
    for module in found_imports:
        if include_module(module):
            yield (filepath, module.__file__)
    if missing_imports:
        yield (filepath, base)

def include_module(module):
    """nice wrapper around a set of ugly comparison neccessary to determine
    if a module should be included in the list of related modules.

    Args:
        module (modulefinder.Module): Module information gathered by modulefinder.
    Returns:
        bool: True if the module should be included, False otherwise.
    """
    return (module.__file__ is not None # builtin import
            and not module.__file__.endswith('__init__.py') # pkg import
            #and filepath != module.__file__
            and module.__name__ != '__main__') # self module

def filtertype(objtype, sequence, filterfalse=False):
    """filter a list of objects base on their type. Currently two types of filtering
    are allowed, those that have the same type as `objtype` and those that doesnt.
    `filterfalse` should be set to `True` if negative filtering is desired.

    Args:
        objtype (Any): Type of the objects that are used as comparison.
        sequence (Sequence[Any]): A sequence of objects to be filtered.
        filterfalse (Optional[bool]): whether or not to filter those objects that
          are not of type `objtype`.
    Returns:
        Iterator[Any]: iterator over the sequence of objects that conform to the
          desired filtering process.
    """
    filterfn = filter if not filterfalse else filterfalse
    return filterfn(lambda element: isinstance(element, objtype), sequence)
