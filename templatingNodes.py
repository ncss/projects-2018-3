import html

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
    >>> print(a.render({"name":"James","age":13}))
    James
    >>> b = PythonNode("age")
    >>> r = b.render({"name":"James","age":13})
    >>> print(r)
    13
    >>> isinstance(r,str)
    True
    '''
    def __init__(self,command):
        self.command = command
    def render(self, context):
        return html.escape(str(eval(self.command, context)))

class IncludeNode(Node):
    '''
    >>> a = IncludeNode("templateTesting/1.html")
    >>> print(a.render({}).strip())
    <html> webpage </html>
    '''
    def __init__(self,path):
        self.path = path
    def render(self,context):
        return open(self.path).read()

class IfNode(Node):
    '''
    >>> bodyNode = GroupNode([PythonNode("age")])
    >>> a = IfNode("age > 5",bodyNode)
    >>> print(a.render({"age":3}))
    <BLANKLINE>
    >>> print(a.render({"age":8}))
    8
    '''
    def __init__(self,condition,body):
        self.body = body
        self.condition = condition

    def render(self,context):
        if eval(self.condition,context):
            return self.body.render(context)
        return ""
    
class ForNode(Node):
    r'''
    >>> pNode = PythonNode("i")
    >>> bNode = GroupNode([TextNode("\n"), pNode])
    >>> a = ForNode("i", "range(3)", bNode)
    >>> print(a.render({}))
    <BLANKLINE>
    0
    1
    2
    '''
    def __init__(self,variable,collection,body):
        self.variable = variable
        self.collection = collection
        self.body = body

    def render(self,context):
        output = ""
        for i in eval(self.collection,context):
            context[self.variable] = i
            output += self.body.render(context)
        return output

class CommentNode(Node):
    r'''
    >>> c = CommentNode()
    >>> print(c.render({}))
    <BLANKLINE>
    '''
    def __init__(self):
        pass
    
    def render(self,context):
        return ""
if __name__ == "__main__":
    import doctest
    doctest.testmod()
    print("Tests done!")
