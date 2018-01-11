from templatingNodes import *

def render_template(string, context):
    """
    >>> render_template("My name is {{ name }}", {"name": "James"})
    'My name is James'
    >>> render_template("{{ name }} is {{ age }} years old", {"name": "James", "age" : "25"})
    'James is 25 years old'
    >>> render_template("User is {{ age }} years old", {"name": "James", "age" : 25})
    'User is 25 years old'
    """

       
    return string


class Parser():
    def __init__(self, characters: str):
        self._characters = characters
        self._length = len(characters)
        self._upto = 0

    def end(self):
        return self._upto == self._length

    def peek(self):
        return None if self.end() else self._characters[self._upto]

    def next(self):
        if not self.end():
            self._upto += 1

    def _parse_group(self):
        nodes = []
        if self.peek() != '{':
            # we know this is a text node
            nodes.append(self._parse_text())
            print(nodes[0].text)
        return GroupNode(nodes)

    def _parse_text(self):
        node = ''
        while self.peek() != '{' and not self.end():
            node += self._characters[self._upto]
            self.next()
        return TextNode(node)

if __name__ == '__main__':
    #import doctest
    #doctest.testmod()
    node = Parser("My name is {{ name }}")
    print(node._characters)
    print(node._parse_group().nodes)
