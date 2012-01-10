def endswith(name, extensions):
    """ Custom 'endswith' taking a list instead of a string.
    """
    for ext in extensions:
        if name.endswith(ext):
            return True
    return False

def dual_list_to_dict(d, keys, values):
    """ Updates dictionary 'd' with the
    list of keys and values.

    >>> d = {}
    >>> dual_list_to_dict(d, ['a'], ['b'])
    >>> d
    {'a': ['b']}
    >>> dual_list_to_dict(d, ['a'], ['c', 'd'])
    >>> d
    {'a': ['b', 'c', 'd']}
    >>> dual_list_to_dict(d, ['a', 'a1'], ['x', 'y'])
    >>> d
    {'a': ['b', 'c', 'd', 'x', 'y'],
     'a1': ['x', 'y']}

    There is no double entries in the values:
    >>> dual_list_to_dict(d, ['a', 'a1'], ['b'])
    >>> d
    {'a': ['b', 'c', 'd', 'x', 'y'],
     'a1': ['x', 'y', 'b']}
    """
    for key in keys:
        if not key in d:
            d[key] = []

        for value in values:
            if not value in d[key]:
                d[key].append(value)

def display_list(header, elements):
    """ Display a list in a more usable way.

    >>> display_list('My header message', ['point 1', 'point 2'])
    My header message
    _________________
     - point 1
     - point 2
    <BLANKLINE>
    <BLANKLINE>

        If the list is empty, it just displays the header:
    >>> display_list('My header message', [])
    My header message
    _________________
    <BLANKLINE>
    <BLANKLINE>

    """
    print header
    print '_' * len(header)
    for el in elements:
        print ' - %s' % el
    print '\n'

def check_included(s1, s2):
    """ Check if s1 is included in s2 (both strings) after removing
    spaces in it.

    >>> check_included('dou', 'doupidou')
    True

    >>> check_included('dou', 'd ou pi do u')
    True

    >>> check_included('dou', 'dupidu')
    False
    """
    def clean(s):
        return s.strip().replace(' ', '')

    return clean(s1) in clean(s2)
