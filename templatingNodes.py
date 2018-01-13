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
    >>> a = IncludeNode("templateTesting/1.html",lambda x,y:x)
    >>> print(a.render({}).strip())
    <html> webpage </html>
    '''
    def __init__(self,path,render_func,include_context={}):
        self.path = "./templates/"+path
        self.render_func = render_func
        self.include_context = include_context
    def render(self,context):
        newContext = {}
        newContext.update(context)
        newContext.update(self.include_context)
        return self.render_func(open(self.path).read(),newContext)

class IfNode(Node):
    '''
    >>> bodyNode = GroupNode([PythonNode("age")])
    >>> a = IfNode("age > 5",bodyNode)
    >>> print(a.render({"age":3}))
    <BLANKLINE>
    >>> print(a.render({"age":8}))
    8
    >>> a.false_body = TextNode("younger then six")
    >>> a.render({"age":3})
    'younger then six'
    >>> a.render({"age":6})
    '6'
    '''
    def __init__(self,condition,true_body,false_body=GroupNode([])):
        self.true_body = true_body
        self.false_body = false_body
        self.condition = condition

    def render(self,context):
        if eval(self.condition,context):
            return self.true_body.render(context)
        else:
            return self.false_body.render(context)
    
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
    >>> bNode = GroupNode([PythonNode("a"), PythonNode("b")])
    >>> fNode = ForNode("a, b", "[(1,2), (4,8)]", bNode)
    >>> print(fNode.render({}))
    1248
    '''
    def __init__(self,variable_block,collection,body):
        self.variable_block = variable_block.split(",")
        self.collection = collection
        self.body = body

    def render(self,context):
        output = ""
        # taking each object in the list
        for block in eval(self.collection, context):
            # if it can't be unpacked
            if not (isinstance(block, list) or isinstance(block, tuple)) or len(self.variable_block) == 1:
                context[self.variable_block[0]] = block
                output += self.body.render(context)
            else:
            # tuple unpacking
                for i in range(len(self.variable_block)):
                    var = self.variable_block[i].strip()
                    context[var] = block[i]
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
   
