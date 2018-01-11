class Node:
    def render(self, context):
        raise NotImplementedError("render() should not be called for base node class")

class TextNode(Node):
    '''
    >>> a = TextNode("just plain text")
    >>> print(a.render({}))
    just plain text
    '''
    def __init__(self,text):
        self.text = text
    def render(self, context):
        return self.text

class GroupNode(Node):
    '''
    >>> a = GroupNode([TextNode("some te"),TextNode("xt")])
    >>> print(a.render({}))
    some text
    >>> b = GroupNode([TextNode("this is also "),a])
    >>> print(b.render({}))
    this is also some text
    >>> a = GroupNode([PythonNode("name")])
    >>> print(a.render({"name":"James","age":"13"}))
    James
    '''
    def __init__(self,nodes):
        self.nodes = nodes
    def render(self, context):
        result = ""
        for node in self.nodes:
            result+=node.render(context)
        return result

class PythonNode(Node):
    '''
    >>> a = PythonNode("name")
    >>> print(a.render({"name":"James","age":"13"}))
    James
    '''
    def __init__(self,command):
        self.command = command
    def render(self, context):
        return eval(self.command, context)

if __name__ == "__main__":
    import doctest
    doctest.testmod()
    print("Tests passed!")
