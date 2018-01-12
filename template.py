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
    >>> render_template("{% if x %} x is True! {% end if %}", {'x': True})
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

    def _parse_if(self):
        
        #This function assumes we are on the "{" of a block that starts with "{%<Whitespace>if"
        while self.peek()!='f':
            self.next()
        self.next()
        
        condition = ""
        while self.peekn(2)!= '%}':

            condition += self.peek()
            self.next()
        self.next()
        self.next()
        body = self._parse_group()
        #Relies on ._parse_group breaking if it hits a previously unmatched end tag
        return IfNode(condition,body)

    def _parse_for(self):

        #This function assums we are on the "{" of a block that starts with "{%<Whitespace>for"
        while self.peek()!='r':
            self.next()
        self.next()
        variable = ''
        while self.peekn(4)!=" in ":
            variable+=self.peek()
            self.next()

        #We should currently be on the first " " of " in collection %}"
        self.nextn(3)
        #We should now be on the second " " of the above string
        coln = ""
        while self.peekn(2)!='%}':
            coln+=self.peek()
            self.next()
        #We chould now be on the " " of  " %}"
        self.nextn(2)
        body = self._parse_group()
        
        #Relies on ._parse_group breaking if it hits a previously unmatched end tag
        return ForNode(variable,coln,body)

if __name__ == '__main__':
    import doctest
    doctest.testmod()
 
