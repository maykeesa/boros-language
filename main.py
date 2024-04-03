import re

class lexical_analyzer:

    lin_num = 1

    def tokens(self, code):
        rules = [
            # Regras para tokens compostos e específicos
            ('ATRIB', r':='),
            ('OPREL', r'>=|<=|==|<>|>|<'),
            ('OPLOG', r'\b[oO][rR]\b|\b[aA][nN][dD]\b'),
            ('COMMENT', r'\/\/[^\n]*'),
            ('CADEIA', r'\".*?\"'),
            # Palavras-reservadas
            ('PROGRAM', r'\b[pP][rR][oO][gG][rR][aA][mM]\b'),
            ('INTEGER', r'\b[iI][nN][tT]\b'),
            ('BOOLEAN', r'\b[bB][oO][oO][lL]\b'),
            ('STRING', r'\b[sS][tT][rR]\b'),
            ('BEGIN', r'\b[bB][eE][gG][iI][nN]\b'),
            ('END', r'\b[eE][nN][dD]\b'),
            ('WHILE', r'\b[wW][hH][iI][lL][eE]\b'),
            ('DO', r'\b[dD][oO]\b'),
            ('READ', r'\b[rR][eE][aA][dD]\b'),
            ('VAR', r'\b[vV][aA][rR]\b'),
            ('FALSE', r'\b[fF][aA][lL][sS][eE]\b'),
            ('TRUE', r'\b[tT][rR][uU][eE]\b'),
            ('WRITE', r'\b[wW][rR][iI][tT][eE]\b'),
            # Tokens numéricos e operadores
            ('NUMBER', r'\b[+-]?\d+\b'),
            ('OPAD', r'\+|-'),
            ('OPMULT', r'\*|\/'),
            ('OPNEG', r'\~'),
            ('MAIOR', r'>'),
            ('MENOR', r'<'),
            # Símbolos diversos
            ('PVIG', r';'),
            ('PONTO', r'\.'),
            ('DPONTOS', r':'),
            ('VIG', r','),
            ('ABPAR', r'\('),
            ('FPAR', r'\)'),
            # Identificadores (nome do programa, variáveis, etc.)
            ('IDENTIFIER', r'[a-zA-Z_][a-zA-Z0-9_]*'),  # Corrigido para reconhecer identificadores corretamente
            # Comentários e espaços em branco
            ('NEWLINE', r'\n'),
            ('SKIP', r'[ \t]+'),
            # Qualquer caractere não reconhecido
            ('MISMATCH', r'.')
        ]

        tokens_join = '|'.join('(?P<%s>%s)' % x for x in rules)
        lin_start = 0

        token = []
        lexeme = []
        row = []
        column = []

        for m in re.finditer(tokens_join, code):
            token_type = m.lastgroup
            
            token_lexeme = m.group(token_type)

            if token_type == 'NEWLINE':
                lin_start = m.end()
                self.lin_num += 1
            elif token_type == 'SKIP':
                continue
            elif token_type == 'COMMENT':
                continue
            elif token_type == 'MISMATCH':
                raise RuntimeError('%r unexpected on line %d' %
                                   (token_lexeme, self.lin_num))
            else:
                col = m.start() - lin_start
                column.append(col)
                token.append(token_type)
                lexeme.append(token_lexeme)
                row.append(self.lin_num)

        all_tokens = []
        for i in range(len(token)):
            all_tokens.append({
                "type": token[i],
                "lexeme": lexeme[i],
                "line": row[i], 
                "column": column[i]
            })

        return all_tokens

class syntax_analyzer:
    def __init__(self):
        self.current_token = None
        self.token_index = 0

    def parse(self, tokens):
        self.tokens = tokens
        self.current_token = self.tokens[self.token_index]
        self.program()

    def program(self):
        self.match('PROGRAM')
        self.match('IDENTIFIER')
        self.match('PVIG')
        self.variable_declarations()
        self.match('BEGIN')
        self.instructions()
        self.match('END')
        self.match('PONTO')

    def variable_declarations(self):
        if self.current_token['type'] == 'VAR':
            self.match('VAR')
            self.match('IDENTIFIER')

            while self.current_token['type'] == 'VIG':
                self.match('VIG')
                self.match('IDENTIFIER')

            self.match('DPONTOS')

            if self.current_token['type'] == 'INTEGER' or self.current_token['type'] == 'BOOLEAN' or self.current_token['type'] == 'STRING':
                self.match(self.current_token['type'])
            else:
                raise RuntimeError('Unexpected token: ' + self.current_token['type'])
            
            self.match('PVIG')
        else:
            return

    def instructions(self):
      self.instruction()
      while self.current_token['type'] == 'IDENTIFIER' or self.current_token['type'] == 'WRITE':
        self.instruction()

    def instruction(self):
        if self.current_token['type'] == 'IDENTIFIER':
            self.match('IDENTIFIER')
            self.match('ATRIB')
            self.expressions()
            self.match('PVIG')
        elif self.current_token['type'] == 'WRITE':
            self.match('WRITE')
            self.match('ABPAR')
            self.match('CADEIA')
            self.match('FPAR')
            self.match('PVIG')
        else:
            raise RuntimeError('Unexpected token: ' + self.current_token['type'])
        
    def expressions(self):
        self.expression()
        while self.current_token['type'] == 'OPAD' or self.current_token['type'] == 'OPMULT' or self.current_token['type'] == 'OPREL' or self.current_token['type'] == 'OPLOG':
            self.match(self.current_token['type'])
            self.expression()

    def expression(self):
        if self.current_token['type'] == 'NUMBER' or self.current_token['type'] == 'IDENTIFIER':
            self.match(self.current_token['type'])
        else:
            raise RuntimeError('Unexpected token: ' + self.current_token['type'])

    def match(self, token_type):
        if self.current_token['type'] == token_type:
            self.token_index += 1
            if self.token_index < len(self.tokens):
                self.current_token = self.tokens[self.token_index]
        else:
            raise RuntimeError('Unexpected token: ' + self.current_token['type'])

if __name__ == "__main__":
    lex = lexical_analyzer()
    syntax = syntax_analyzer()
    codigo_funciona = """
    program exemplo;
    var abc: str;
    begin
        x := 10;
        write("Hello World");
    end.
    """
    tokens = lex.tokens(codigo_funciona)
    print("\nLexical analysis successful.")
    syntax.parse(tokens)
    print("Syntax analysis successful.")

