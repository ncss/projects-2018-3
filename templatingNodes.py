class Node:
    def render():
        raise NotImplementedError("render() should not be called for base node class")

class TextNode(Node):
    '''
    >>> a = TextNode("just plain text")
    >>> print(a.render())
    just plain text
    '''
    def __init__(self,text):
        self.text = text
    def render(self):
        return self.text

class GroupNode(Node):
    '''
    >>> a = GroupNode([TextNode("some te"),TextNode("xt")])
    >>> print(a.render())
    some text
    '''
    def __init__(self,nodes):
        self.nodes = nodes
    def render(self):
        result = ""
        for node in self.nodes:
            result+=node.render()
        return result
if __name__ == "__main__":
    import doctest
    doctest.testmod()
    print("Tests passed!")
