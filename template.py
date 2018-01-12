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

    def peekCharacters(self,num):
        if self.end():
            return None
        return self._characters[self._upto:self._upto+num]
    
    def next(self):
        if not self.end():
            self._upto += 1

    def nextCharacters(self,num):
        for i in range(num):
            self.next()
            
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

    def _parse_if(self):
        
        #This function assumes we are on the "{" of a block that starts with "{%<Whitespace>if"
        while self.peek()!='f':
            self.next()
        self.next()
        
        condition = ""
        while self.peekCharacters(2)!= '%}':

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
        while self.peekCharacters(4)!=" in ":
            variable+=self.peek()
            self.next()

        #We should currently be on the first " " of " in collection %}"
        self.nextCharacters(3)
        #We should now be on the second " " of the above string
        coln = ""
        while self.peekCharacters(2)!='%}':
            coln+=self.peek()
            self.next()
        #We chould now be on the " " of  " %}"
        self.nextCharacters(2)
        body = self._parse_group()
        
        #Relies on ._parse_group breaking if it hits a previously unmatched end tag
        return ForNode(variable,coln,body)

if __name__ == '__main__':
    #import doctest
    #doctest.testmod()
    node = Parser("My name is {{ name }}")
    print(node._characters)
    print(node._parse_group().nodes)
    a ='''{% if x %} x is True! {% end if %}'''
    b = Parser(a)
    c = b._parse_if()
    print("if parser result:\n ",c.render({"x":True}), "\nshould be around:\n x is True! ")
    print()
    a = r'''{% for i in range(3) %}hey!{% end for % }'''
    b = Parser(a)
    c = b._parse_for()
    print(c.render({}))
