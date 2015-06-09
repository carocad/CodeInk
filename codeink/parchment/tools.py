
def safe_import(origin, funk1, funk2):
    """Safely import a function whose name was changed from a module whose name was not.
    This function is specially useful if the function name is not known at runtime.

    Args:
        origin (str): name of the module where the function to be imported is located
        funk1 (str): name of the first function name to try to import
        funk2 (str): name of the second function name to try to import
    Returns:
        function: function object imported from `origin`

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
