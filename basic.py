################################
# CONSTANTS
################################

TT_INT = "INT"
TT_FLOAT = "FLOAT"
TT_MUL = "MULTIPLY"
TT_DIV = "DIVIDE"
TT_PLUS = "PLUS"
TT_MINUS = "MINUS"
TT_OPARENT = "OPARENT"
TT_CPARENT = "CPARENT"
DIGITS = "0123456789"


################################
# ERROR HANDLING
################################

class Error:
    def __init__(self, start_pos, end_pos, error_name, error_details):
        self.start_pos = start_pos
        self.end_pos = end_pos
        self.error_name = error_name
        self.error_details = error_details

    def str_error(self):
        return f"{self.error_name}:{self.error_details}\nFile {self.start_pos.filename}, line {self.start_pos.line + 1}"


class IllegalCharError(Error):
    def __init__(self, start_pos, end_pos, details):
        super().__init__(start_pos, end_pos, "Illegal Characters Error", details)


################################
# POSITIONS
################################

class Positions:
    def __init__(self, index, line, column, filename, ftext):
        self.index = index
        self.line = line
        self.column = column
        self.filename = filename
        self.ftext = ftext

    def advanced(self, current_char):
        self.index += 1
        self.column += 1

        if current_char == '\n':
            self.line += 1
            self.column = 0

        return self

    def copy(self):
        return Positions(self.index, self.line, self.column, self.filename, self.ftext)


################################
# TOKENS
################################

class Token:
    def __init__(self, _type, value=None):
        self.type = _type
        self.value = value

    def __repr__(self):
        if self.value:
            return f"{self.type}:{self.value}"
        return f"{self.type}"


################################
# LEXICAL ANALYZER
################################

class Lexer:
    def __init__(self, filename, inp):
        self.filename = filename
        self.text = inp
        self.pos = Positions(-1, 0, -1, filename, inp)
        self.current_char = None
        self.advanced()

    def advanced(self):
        self.pos.advanced(self.current_char)
        self.current_char = self.text[self.pos.index] if self.pos.index < len(self.text) else None

    def make_tokens(self):
        tokens = []

        while self.current_char is not None:
            if self.current_char in " \t":
                self.advanced()
                continue
            elif self.current_char == '*':
                tokens.append(Token(TT_MUL))
            elif self.current_char == '/':
                tokens.append(Token(TT_DIV))
            elif self.current_char == '+':
                tokens.append(Token(TT_PLUS))
            elif self.current_char == '-':
                tokens.append(Token(TT_MINUS))
            elif self.current_char == '(':
                tokens.append(Token(TT_OPARENT))
            elif self.current_char == ')':
                tokens.append(Token(TT_CPARENT))
            elif self.current_char in DIGITS:
                tokens.append(self.make_number())
            else:
                err_start_pos = self.pos.copy()
                error = self.current_char
                self.advanced()
                return [], IllegalCharError(err_start_pos, self.pos, "'" + error + "'")
            self.advanced()

        return tokens, None

    def make_number(self):
        str_num = ""
        dots_cnt = 0

        while self.current_char is not None and self.current_char in DIGITS + '.':
            if self.current_char == '.':
                if dots_cnt > 0:
                    break

                dots_cnt += 1
                str_num += self.current_char
            else:
                str_num += self.current_char
            self.advanced()

        self.pos.index -= 1
        if dots_cnt == 0:
            return Token(TT_INT, int(str_num))
        else:
            return Token(TT_FLOAT, float(str_num))


################################
# RUN
################################


def run(filename, inp):
    lexer = Lexer(filename, inp)
    tokens, error = lexer.make_tokens()

    return tokens, error
