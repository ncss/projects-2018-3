def render_template(string, context):
    """
    >>> render_template("My name is {{ name }}", {"name": "James"})
    'My name is James'
    >>> render_template("User is {{ age }} years old", {"name": "James", "age" : "25"})
    'User is 25 years old'
    """
    for variable in context:
        string = string.replace("{{ "+variable+" }}",context[variable])
    
    return string

if __name__ == '__main__':
    import doctest
    doctest.testmod()
