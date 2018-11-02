# To identify different token types, we use integer to speed up the process
# INT token is for the declaration where INT_CONST token is for immediate values
# similar for the REAL_CONST
# DIV in pascal means integer divide, so we need a F_DIV for float divide
import json

TK_BOOL = 0
TK_INT_CONST = 1
TK_REAL_CONST = 2
TK_EOF = 3
TK_ADD = 4
TK_MINUS = 5
TK_MUL = 6
TK_DIV = 7
TK_LPR = 8
TK_RPR = 9
TK_BEGIN = 10
TK_END = 11
TK_DOT = 12
TK_ASSIGN = 13
TK_ID = 14
TK_SEMI = 15
TK_VAR = 16
TK_PROGRAM = 17
TK_COMMA = 18
TK_COLON = 19
TK_INT = 20
TK_REAL = 21
TK_F_DIV = 22
TK_GREAT = 23
TK_LESS = 24
TK_GREAT_THAN = 25
TK_LESS_THAN = 26
TK_MOD = 27
TK_REPEAT = 28
TK_UNTIL = 29
TK_EQUAL = 30
TK_NOT_EQUAL = 31
TK_BREAK = 32
TK_CONTINUE = 33


# A class to represent a Token with two elements: type of the token, and the value the token have
class Token(object):
    def __init__(self, tk_type, value):
        self.tk_type = tk_type
        self.value = value

    # Rewrite the __str__ so we output the value of the token rather than the token address in memory, this is for test
    def __str__(self):
        return '{x}'.format(x=self.value)


# Instructions that take in 2 parameters other than the instruction if self
class Two_Instruction(object):
    def __init__(self, instruction, rt, rs):
        self.ins = instruction
        self.rs = rs
        self.rt = rt

    def __str__(self):
        return '< {ins} {rt} {rs} >'.format(
            ins=self.ins, rt=self.rt, rs=self.rs
        )


# Instruction that take in 1 parameter
class One_Instruction(object):
    def __init__(self, instruction, address):
        self.ins = instruction
        self.adr = address

    def __str__(self):
        return '< {ins} {address} >'.format(
            ins=self.ins, address=self.adr
        )


# A dictionary of list of keywords, so when user input identifiers in this list,
# the corresponding token would be returned rather than TK_ID
KEYWORD = {'BEGIN': Token(TK_BEGIN, 'BEGIN'), 'END': Token(TK_END, 'END'),
           'VAR': Token(TK_VAR, 'VAR'), 'REAL': Token(TK_REAL, 'REAL'),
           'PROGRAM': Token(TK_PROGRAM, 'PROGRAM'), 'DIV': Token(TK_DIV, 'DIV'),
           'INTEGER': Token(TK_INT, 'INTEGER'), 'BOOLEAN': Token(TK_BOOL, 'BOOLEAN'),
           'REPEAT': Token(TK_REPEAT, 'REPEAT'), 'UNTIL': Token(TK_UNTIL, 'UNTIL'),
           'BREAK': Token(TK_BREAK, 'BREAK'), 'CONTINUE': Token(TK_CONTINUE, 'CONTINUE')
           }


# Scanner or lexer that break the input file or string into tokens, so parser could have access to tokens not single
# digit character
class Scanner(object):

    # initialization, pos is the position of the curr_character in the input string
    def __init__(self, string):
        self.string = string
        self.pos = 0
        self.curr_char = self.string[self.pos]

    # sometime we need to look ahead to see what exactly is current token
    def look_ahead(self):
        look_pos = self.pos + 1
        if look_pos > len(self.string) - 1:
            return None
        else:
            return self.string[look_pos]

    # kind like the match function in parser, go to next position until we reach the end of string
    # update the curr_char
    def advance(self):
        self.pos += 1
        if self.pos > len(self.string) - 1:
            self.curr_char = None
        else:
            self.curr_char = self.string[self.pos]

    # for identifiers, take in all the alphabetical characters, and if those character forms a keyword, return the
    # keyword token, if not, return a id token both with the value of the combined char
    def id(self):
        string = ''
        while self.curr_char is not None and self.curr_char.isalnum():
            string += self.curr_char
            self.advance()
        token = KEYWORD.get(string, Token(TK_ID, string))
        return token

    # similar function as id, take in all the digits, if we see a dot, return real token, else return integer token
    # with the corresponding value
    def number(self):
        num = ''
        while self.curr_char is not None and self.curr_char.isdigit():
            num += self.curr_char
            self.advance()
        if self.curr_char == '.':
            num += self.curr_char
            self.advance()
            while self.curr_char is not None and self.curr_char.isdigit():
                num += self.curr_char
                self.advance()
            token = Token(TK_REAL_CONST, float(num))
        else:
            token = Token(TK_INT_CONST, int(num))

        return token

    # only called when we see a {, skip all the characters until we see a } that close the comment
    def skip_comment(self):
        while self.curr_char != '}':
            self.advance()
        # for skip the }
        self.advance()

    # a go to function for the usage of repeat
    def go_to(self, address):
        self.pos = address
        self.curr_char = self.string[address]
        return self.get_next_token()

    # the core of scanner, get next token for the usage of parser
    def get_next_token(self):
        # skip the section if current token is none
        while self.curr_char is not None:
            # skip all the white spaces as we don't need them
            if self.curr_char.isspace():
                while self.curr_char is not None and self.curr_char.isspace():
                    self.advance()
                continue
            # so for different inputs we got, we return different tokens
            if self.curr_char.isdigit():
                return self.number()
            if self.curr_char == '*':
                self.advance()
                return Token(TK_MUL, '*')
            if self.curr_char == '(':
                self.advance()
                return Token(TK_LPR, '(')
            if self.curr_char == ')':
                self.advance()
                return Token(TK_RPR, ')')
            if self.curr_char == '+':
                self.advance()
                return Token(TK_ADD, '+')
            if self.curr_char == '-':
                self.advance()
                return Token(TK_MINUS, '-')
            if self.curr_char == '/':
                self.advance()
                return Token(TK_F_DIV, '/')
            # use look ahead to see if the : is followed by =, so we don't return TK_COLON when it should be an
            # assignment
            if self.curr_char == ':' and self.look_ahead() == '=':
                self.advance()
                self.advance()
                return Token(TK_ASSIGN, ':=')
            if self.curr_char.isalpha():
                return self.id()
            if self.curr_char == '.':
                self.advance()
                return Token(TK_DOT, '.')

            if self.curr_char == ';':
                self.advance()
                return Token(TK_SEMI, ';')
            if self.curr_char == ',':
                self.advance()
                return Token(TK_COMMA, ',')
            if self.curr_char == ':':
                self.advance()
                return Token(TK_COLON, ':')
            if self.curr_char == '{':
                self.advance()
                self.skip_comment()
                continue
            if self.curr_char == '%':
                self.advance()
                return Token(TK_MOD, '%')
            if self.curr_char == '<' and self.look_ahead() == '>':
                self.advance()
                self.advance()
                return Token(TK_NOT_EQUAL, '<>')
            if self.curr_char == '<' and self.look_ahead() == '=':
                self.advance()
                self.advance()
                return Token(TK_LESS_THAN, '<=')
            if self.curr_char == '>' and self.look_ahead() == '=':
                self.advance()
                self.advance()
                return Token(TK_GREAT_THAN, '>=')
            if self.curr_char == '<':
                self.advance()
                return Token(TK_LESS, '<')
            if self.curr_char == '>':
                self.advance()
                return Token(TK_GREAT, '>')
            if self.curr_char == '=':
                self.advance()
                return Token(TK_EQUAL, '=')
            # when not belong to any case, return an error
            raise Exception('"{char}" can not be recognized by scanner!'.format(char=self.curr_char))
        # indicate end of file
        return Token(TK_EOF, None)


# Using the tokens from the scanner, we do actions accordingly using parser
class Parser(object):

    # initialization, also taking scanner as parameters so we can have access to get next token function
    def __init__(self, scanner):
        self.scanner = scanner
        self.curr_token = self.scanner.get_next_token()
        # symbol table is for storing data_types
        self.symbol_table = {}
        # for storing actual value
        self.memory_table = {}
        self.ip = 0
        self.code = []

    # 'eat' the current token, kind like the advance function in scanner, also return error if current token is not what
    # we  wanted to be
    def match(self, token):
        if self.curr_token.tk_type == token:
            self.curr_token = self.scanner.get_next_token()
        else:
            raise Exception('"{token}" not match as intended, parsing error!'.format(token=self.curr_token.value))

    # Push in real or int
    def pushi(self):
        self.code.append(str(One_Instruction('PUSHI', self.curr_token.value)))

    # Push in variable
    def push(self):
        self.code.append(str(One_Instruction('PUSH', self.curr_token.value)))

    # 'POP' from the stack
    def pop(self):
        self.code.append('<POP>')

    # the deepest part in our grammar, always being executed first
    def factor(self):
        token = self.curr_token
        # not adding or subtracting but for positive or negative, so each time we see '-' at factor level, we
        # invert the value of the expression, each time we see positive, 'do nothing'
        if token.tk_type == TK_ADD:
            self.match(TK_ADD)
            return +self.expr()
        elif token.tk_type == TK_MINUS:
            self.match(TK_MINUS)
            result = self.expr()
            self.code.append(str(One_Instruction('NEG', result)))
            return -result
        # return numbers for the calculations
        elif token.tk_type == TK_INT_CONST:
            self.pushi()
            self.match(TK_INT_CONST)
            return token.value
        elif token.tk_type == TK_REAL_CONST:
            self.pushi()
            self.match(TK_REAL_CONST)
            return token.value
        # when we see (, we calculate the expression inside the parentheses first
        elif token.tk_type == TK_LPR:
            self.match(TK_LPR)
            result = self.expr()
            self.match(TK_RPR)
            return result
        # for accessing the value inside a variable
        else:
            self.push()
            var = self.var()
            result = self.memory_table.get(var.value)
            if result is None:
                raise Exception('"{var}" has not be declared or don"t have value assigned!'.format(var=var.value))
            return result

    # upper part in our grammar
    def term(self):
        # call factor before we calculate anything in terms
        result = self.factor()
        # perform mul or div or mod
        while self.curr_token.tk_type in (TK_MUL, TK_DIV, TK_F_DIV, TK_MOD):
            if self.curr_token.tk_type == TK_MUL:
                self.match(TK_MUL)
                factor = self.factor()
                self.code.append(str(Two_Instruction('MUL', result, factor)))
                self.pop()
                result *= factor
            elif self.curr_token.tk_type == TK_DIV:
                self.match(TK_DIV)
                factor = self.factor()
                self.code.append(str(Two_Instruction('DIV', result, factor)))
                self.pop()
                result = int(result / factor)
            elif self.curr_token.tk_type == TK_F_DIV:
                self.match(TK_F_DIV)
                factor = self.factor()
                self.code.append(str(Two_Instruction('FDIV', result, factor)))
                self.pop()
                result = float(result / factor)
            elif self.curr_token.tk_type == TK_MOD:
                self.match(TK_MOD)
                factor = self.factor()
                self.code.append(str(Two_Instruction('MOD', result, factor)))
                self.pop()
                result %= factor
        return result

    # expression, 'highest' part of our grammar for arithmetic calculation
    def expr(self):
        # call term first
        result = self.term()
        # add or subtract always perform last
        while self.curr_token.tk_type in (TK_ADD, TK_MINUS):
            if self.curr_token.tk_type == TK_ADD:
                self.match(TK_ADD)
                term = self.term()
                self.code.append(str(Two_Instruction('ADD', result, term)))
                self.pop()
                result += term
            elif self.curr_token.tk_type == TK_MINUS:
                self.match(TK_MINUS)
                term = self.term()
                self.code.append(str(Two_Instruction('SUB', result, term)))
                result -= term
        return result

    def comparison(self):
        result = self.expr()
        if self.curr_token.tk_type == TK_GREAT_THAN:
            self.code.append(str(One_Instruction('JGE', self.ip)))
            self.match(TK_GREAT_THAN)
            return result >= self.expr()
        elif self.curr_token.tk_type == TK_GREAT:
            self.code.append(str(One_Instruction('JG', self.ip)))
            self.match(TK_GREAT)
            return result > self.expr()
        elif self.curr_token.tk_type == TK_LESS_THAN:
            self.code.append(str(One_Instruction('JLE', self.ip)))
            self.match(TK_LESS_THAN)
            return result <= self.expr()
        elif self.curr_token.tk_type == TK_LESS:
            self.code.append(str(One_Instruction('JL', self.ip)))
            self.match(TK_LESS)
            return result < self.expr()
        elif self.curr_token.tk_type == TK_EQUAL:
            self.code.append(str(One_Instruction('JE', self.ip)))
            self.match(TK_EQUAL)
            return result == self.expr()
        elif self.curr_token.tk_type == TK_NOT_EQUAL:
            self.code.append(str(One_Instruction('JNE', self.ip)))
            self.match(TK_NOT_EQUAL)
            return result != self.expr()

    # when we returned a token, scanner.pos is where the token ended, so we want to go back to where the token started
    # by subtract the token value from it.
    def loop_pos(self):
        return self.scanner.pos - len(self.curr_token.value)

    # essentially to match the TK_ID and return the token for that id
    def var(self):
        result = self.curr_token
        self.match(TK_ID)
        return result

    # only called when we have an assignment
    def assignment(self):
        left = self.var()  # token
        self.match(TK_ASSIGN)
        right = self.expr()  # value of the token ( a:= expr)
        # in Pascal, all the variables must be declared before assignment, so print a error message for that
        if left.value not in self.symbol_table:
            raise Exception('Variable "{name}" not declared before assignment!'.format(name=left.value))
        # also, if the variable is assign to different type as declared, we return an error
        elif self.check_type(self.symbol_table.get(left.value), right) is False:
            raise Exception('Variable "{name}" is assigned to wrong type!'.format(name=left.value))
        # token.value is the identifier, so we stored the token name and it's value as a pair in our memory
        self.memory_table[left.value] = right
        self.code.append(str(Two_Instruction('MOV', left, right)))

    # a statement could be an assignment or another begin end blocks
    def statement(self):
        if self.curr_token.tk_type == TK_BEGIN:
            self.begin_stat()
        elif self.curr_token.tk_type == TK_ID:
            self.assignment()
        elif self.curr_token.tk_type == TK_REPEAT:
            # Get the address for the jump, just before the repeat
            self.ip = self.loop_pos()
            self.code.append(str(Two_Instruction('MOV', '$ra', self.ip)))
            self.repeat_statement()

    #  loop
    def repeat_statement(self):
        self.match(TK_REPEAT)
        self.statement_list()
        self.match(TK_UNTIL)
        # Save the comparison result
        compare = self.comparison()
        # If comparison returns false, jump back
        if not compare:
            self.curr_token = self.scanner.go_to(self.ip)
            self.repeat_statement()

    def statement_list(self):
        self.statement()
        # if their are multiple statements in one block, call all of them
        while self.curr_token.tk_type == TK_SEMI:
            self.match(TK_SEMI)
            self.statement()

    # begin end block, each block could contain multiple statements so we use statement_list
    def begin_stat(self):
        self.match(TK_BEGIN)
        self.statement_list()
        self.match(TK_END)

    # for the declaration before the begin and end block, as all variable must be declared before assignment
    def declaration(self):
        if self.curr_token.tk_type == TK_VAR:
            self.match(TK_VAR)
            # loop until we go through all the declaration lines
            while self.curr_token.tk_type == TK_ID:
                self.var_declare()
                self.match(TK_SEMI)
            # if we don't see VAR, just skip the function
        else:
            pass

    # declare variables
    # a : INTEGER
    def var_declare(self):
        # store the variable's name
        var_name = self.curr_token.value
        # check if the variable is already declared
        if self.symbol_table.get(var_name) is not None:
            raise Exception('Variable "{name}" duplicated!'.format(name=var_name))
        # add the variable to the list
        variable = [var_name]
        self.match(TK_ID)
        # we could declare multiple variable in one line, so if we see comma after a variable, declare them as well
        while self.curr_token.tk_type == TK_COMMA:
            self.match(TK_COMMA)
            # add identifier after comma into the list of variables of same time
            variable.append(self.curr_token.value)
            self.match(TK_ID)
        self.match(TK_COLON)
        # the type of variable
        right = self.type_declare()
        # adding those to symbol_table
        for ID in variable:
            # in the form of a:INTEGER, and we could reassign value later
            if self.symbol_table.get(ID) is not None:
                raise Exception('Variable "{name}" is duplicated!'.format(name=ID))
            self.symbol_table[ID] = right
            self.code.append('{VAR}: .word {type}'.format(VAR=ID, type=right))

    # Return the type according to tokens
    def type_declare(self):
        token = self.curr_token
        if token.tk_type == TK_INT:
            self.match(TK_INT)
            return 'INTEGER'
        else:
            self.match(TK_REAL)
            return 'REAL'

    # Using the isinstance function to check if the variable and expression belong to same type
    @staticmethod
    def check_type(variable, expr):
        if variable == 'INTEGER':
            return isinstance(expr, int)
        elif variable == 'REAL':
            return isinstance(expr, float)

    # main function
    def program(self):
        # all program starts with PROGRAM id;
        self.match(TK_PROGRAM)
        # store the program name into our table for later use (if any)
        # name = self.curr_token.value
        # self.symbol_table['Program_Name'] = name
        self.match(TK_ID)
        self.match(TK_SEMI)
        # VAR block
        self.declaration()
        # Begin blocks
        self.begin_stat()
        # Match the dot for the end of program
        self.match(TK_DOT)


def main():
    # Take in the input_file
    with open('input_file','r') as input_file:
        text = input_file.read()
    text = str(text)
#     text = """\
# PROGRAM TestProgram;
# VAR
#    {a,}a, b, c, x, d : INTEGER; { uncomment to get duplicate error} { get rid of a to get undeclared error}
#    y, ss        : REAL;
#    {comment section}
# BEGIN
#       BEGIN
#       END;
#       a := 2;
#       b := 0;
#       REPEAT
#       a := a+1;
#       {a := 1.1} {comment to get type error}
#       b := a
#       UNTIL a >= 5;
#       c := 2 % 3 * 5 * (3+5) DIV 8;
#       d := 5-(-5);
#       y := 5.5/3;
#       d := 5 * 5;
#       ss := 5.5;
#       BEGIN
#       d := 5
#       END;
# END.
#  """
    # Initialize scanner and parser
    scanner = Scanner(text)
    parser = Parser(scanner)
    # Call the parser main program
    parser.program()
    # Print the symbol table and the memory table
    print('Symbol table: ')
    print(parser.symbol_table)
    print('Memory table: ')
    print(parser.memory_table)
    data = parser.code
    with open('simple_stack', 'w') as outfile:
        json.dump(data, outfile, indent=2)


main()
