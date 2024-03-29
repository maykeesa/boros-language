import re


class lexical_analyzer:

    lin_num = 1

    def tokens(self, code):
        rules = [
            # Regras para tokens compostos e específicos
            ('ATRIB', r':='),
            ('MAIG', r'>='),
            ('MENIG', r'<='),
            ('IGUAL', r'=='),
            ('DIFER', r'<>'),
            ('OR', r'\b[oO][rR]\b'),
            ('AND', r'\b[aA][nN][dD]\b'),
            # Palavras-chave
            ('PROGRAM', r'\b[pP][rR][oO][gG][rR][aA][mM]\b'),
            ('INTEGER', r'\b[iI][nN][tT]\b'),
            ('BOOLEAN', r'\b[bB][oO][oO][lL]\b'),
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
            ('MAIS', r'\+'),
            ('MENOS', r'-'),
            ('VEZES', r'\*'),
            ('DIVIDIR', r'\/'),
            ('NEG', r'\~'),
            ('MAIOR', r'>'),
            ('MENOR', r'<'),
            # Símbolos diversos
            ('PVIG', r';'),
            ('PONTO', r'\.'),
            ('DPONTOS', r':'),
            ('VIG', r','),
            ('ABPAR', r'\('),
            ('FPAR', r'\)'),
            # Comentários e espaços em branco
            ('COMMENT', r'\/\/[^\n]*'),
            ('NEWLINE', r'\n'),
            ('SKIP', r'[ \t]+'),
            # Qualquer caractere não reconhecido
            ('MISMATCH', r'.')
        ]

        tokens_join = '|'.join('(?P<%s>%s)' % x for x in rules)
        print(tokens_join, '\n\n\n')
        lin_start = 0

        # Lists of output for the program
        token = []
        lexeme = []
        row = []
        column = []

        # It analyzes the code to find the lexemes and their respective Tokens
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
                print(1)
                print(f"token_lexeme: {
                      token_lexeme}, token_type: {token_type}")
                raise RuntimeError('%r unexpected on line %d' %
                                   (token_lexeme, self.lin_num))
            else:
                col = m.start() - lin_start
                column.append(col)
                token.append(token_type)
                lexeme.append(token_lexeme)
                row.append(self.lin_num)
                # To print information about a Token
                print('Token = {0}, Lexeme = \'{1}\', Row = {2}, Column = {3}'
                      .format(token_type, token_lexeme, self.lin_num, col))

        return token, lexeme, row, column


if (__name__ == "__main__"):
    codigo_funciona = """
    program;
    var: int;
    begin
        := 10;
        write(a);
        fasfasfafafs
    end
    """

    lex = lexical_analyzer()
    tokens, lexemas, linhas, colunas = lex.tokens(codigo_funciona)
    print("Tokens:", tokens)
    print("Lexemas:", lexemas)
    print("Linhas:", linhas)
    print("Colunas:", colunas)
