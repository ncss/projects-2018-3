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
    ' x is True! '
    >>> render_template("{% if chicken %} x is True! {% end if %}", {'chicken': False})
    ''
    >>> render_template("{% if x == y %} x equals y! {% end if %}", {'x': 10, 'y': 10})
    ' x equals y! '
    >>> render_template("{% if x == y %} x equals y! {% end if %}", {'x': 11, 'y': 10})
    ''
    >>> render_template("{% if x == y %} name: {{ chicken }} {% end if %}break ", {'x': 10, 'y': 10, 'chicken': 'hello'} )
    ' name: hello break '
    >>> render_template("{% for i in chicken %} {{ i }} {% end for %}", {'chicken': [1,2,3,10]})
    ' 1  2  3  10 '
    >>> render_template("{% if x == y %} name: {{ chicken }} {% end if %}", {'x': 10, 'y': 10, 'chicken': 'hello'} )
    ' name: hello '
    >>> render_template("{% for i in range(5) %}m{% end for %}h",{})
    'mmmmmh'
    >>> render_template("{% for i in range(5) %}m{% end for %}h {{ food }}",{"food":"chicken"})
    'mmmmmh chicken'
    >>> render_template("{% if do %}{% for i in range(num) %}my num is {{ i }}!{% end for %}{% end if %}",{"do":True,"num":4})
    'my num is 0!my num is 1!my num is 2!my num is 3!'
    >>> render_template("{% for i in range(num) %}{% if i%2==0 %}{{ i }}{% end if %}{% end for %}",{"num":10})
    '02468'
    >>> render_template("{{            i}}",{"i":42})
    '42'
    >>> render_template("My name is{% comment %} please ignore {% end comment %} {{ name }}", {"name": "James"})
    'My name is James'
    >>> render_template("{% comment %} VERY IMPORTANT MESSAGE {% end comment %}", {})
    ''
    >>> render_template("{% if True %} a {% comment %} very {% end comment %}important word {% end if %}", {})
    ' a important word '
    >>> render_template('''{% include templateTesting/header.html %} and we can have text from no file and {% include templateTesting/footer.html %}''',{})
    'we can get stuff from the header and we can have text from no file and we can get stuff from the footer!'
    """
    node = Parser(string)._parse_group()
    return node.render(context)

class TemplateException(Exception):
    def __init__(self, name, msg):
        super().__init__()
        self.name = name
        self.msg = msg

    def __str__(self):
        return self.msg

class FileException(Exception):
    def __init__(self, name, msg):
        super().__init__()
        self.name = name
        self.msg = msg

    def __str__(self):
        return self.msg

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
    
    def remaining_text(self):
        return self._characters[self._upto:]
    
    def nextn(self, number):
        if self._upto + number <= self._length:
            self._upto += number

    def _parse_group(self):
        nodes = []
        while not self.end():
            if self.peek() != '{':
                # we know this is a text node
                nodes.append(self._parse_text())
            elif re.match(r'^{%\s*include',self.remaining_text()):
                nodes.append(self._parse_include())
            elif self.peekn(2) == '{{':
                 nodes.append(self._parse_python())
            elif re.match(r'^{%\s*if',self.remaining_text()):
                nodes.append(self._parse_if())
            elif re.match(r'^{%\s*fo',self.remaining_text()):
                nodes.append(self._parse_for())
            elif re.match(r'^{%\s*comment',self.remaining_text()):
                self._parse_comment()
            else:
                break
        return GroupNode(nodes)

    def _parse_text(self):
        node = ''
        while self.peek() != '{' and not self.end():
            node += self._characters[self._upto]
            self.next()
        return TextNode(node)

    def _parse_python(self):
        matched = re.match(r'^{{\s*(\w*)\s*}}', self.remaining_text())
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

        endTag = re.match(r"^{%\s*end\s+if\s*%}", self.remaining_text())
        #checking for an end tag
        if endTag is None:
            raise TemplateException('Syntax Error', 'Expecting an "end if" tag')
        self.nextn(endTag.end())
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
        endTag = re.match(r"^{%\s*end\s+for\s*%}", self.remaining_text())
        if endTag is None:
            raise TemplateException('Syntax Error', 'Expecting an "end for" tag')
        self.nextn(endTag.end())
      
        return ForNode(variable.strip(),coln,body)

    def _parse_include(self):
        #Test below no longer work. Paths now have to be valid
        
        #r'''
        #>>> parser = Parser("{% include folder/file.html %} {% include folder2/file2.html %}")
        #>>> node = parser._parse_include()
        #>>> print(node.path)
        #folder/file.html
        #'''
        
        #This functions assumes we are on the "{" of a block like this {% include fi.le %}
        match = re.match(r'^{%\s*include\s+([\w\/]+\.[\w]+)\s*%}', self.remaining_text())
        path = match.group(1)
        self.nextn(match.end())
        try:
            open(path, 'r').close()
        except OSError:
            raise FileException('FileException', 'file not found')
        return IncludeNode(path)

    def _parse_comment(self):
        #This function assumes that we are on the first character of a block like this
        #{% comment %} WOW, THIS LANGUAGE HAS COMMENTS! {% end comment %}

        while self.peekn(2) != '%}':
            self.next()
        #Now we are past the first {% comment %}
        while self.peekn(2) != '{%':
            self.next()
            
        endTag = re.match(r"^{%\s*end\s+comment\s*%}", self._characters[self._upto:])
        if endTag is None:
            raise TemplateException('Syntax Error', 'Expecting an "end comment" tag')
        self.nextn(endTag.end())

def asserEx(invalid, context):
    #Function that passes if the string is invalid
    """
    >>> asserEx('{% if x == y %} x equals y! ', {'x': 10, 'y': 10})
    >>> asserEx("{% for i in range(5) %}mfor %}h",{})
    >>> asserEx("{% if True %} a {% comment %} very {% end important word {% end if %}", {})
    >>> asserEx("{% if True %} a {% comment %} very {% end comment %} important word  if %}", {})
    >>> asserEx('''{% include templateTesting/headerasd.html %}''',{})
    """
    try:
        render_template(invalid, context)
        assert False, "should throw an exception, was expecting an invalid string"
        
    except (TemplateException, FileException):
        pass    

if __name__ == '__main__':
    import doctest
    doctest.testmod()
    node = Parser("{% for i in chicken %} {{ i }} {% end for %}")
    context = {'chicken': [1,2,3,10]}
    print("All tests done, you are awesome :)")
    #render_template("{% if True %} a {% comment %} very {% end comment %} important word  if %}", {})
    #render_template('''{% include templateTesting/headerasd.html %}''',{})

    


