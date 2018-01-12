from templatingNodes import *
import re

def render_template(string, context):
    """
    >>> render_template("My name is {{ name }}", {"name": "James"})
    'My name is James'
    >>> render_template("{{ name }} is {{ age }} years old", {"name": "James", "age" : "25"})
    'James is 25 years old'
    >>> render_template("User is {{ age }} years old", {"name": "James", "age" : 25})
    'User is 25 years old'
    """
    node = Parser(string)._parse_group()
    return node.render(context)


class Parser():
    def __init__(self, characters: str):
        self._characters = characters
        self._length = len(characters)
        self._upto = 0

    def end(self):
        return self._upto == self._length

    def peek(self):
        return None if self.end() else self._characters[self._upto]

    def peekn(self, number):
        return None if self.end() else self._characters[self._upto:self._upto + number]    

    def next(self):
        if not self.end():
            self._upto += 1

    def nextn(self, number):
        if self._upto + number <= self._length:
            self._upto += number

    def _parse_group(self):
        nodes = []
        while not self.end():
            if self.peek() != '{':
                # we know this is a text node
                nodes.append(self._parse_text())
            else:
                if self.peekn(2) == '{{':
                    nodes.append(self._parse_python())
        return GroupNode(nodes)

    def _parse_text(self):
        node = ''
        while self.peek() != '{' and not self.end():
            node += self._characters[self._upto]
            self.next()
        return TextNode(node)

    def _parse_python(self):
        string = self._characters[self._upto:]
        matched = re.match(r'{{ (\w*) }}', string)
        variable = matched.group(1)
        self.nextn(matched.end())
        return PythonNode(variable)

if __name__ == '__main__':
    import doctest
    doctest.testmod()
    
    
