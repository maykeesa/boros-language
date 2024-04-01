from pprint import pprint
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
            ('COMMENT', r'\/\/[^\n]*'),
            ('STRING', r'\".*?\"'),
            # Palavras-reservadas
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
            ('NEWLINE', r'\n'),
            ('SKIP', r'[ \t]+'),
            # Qualquer caractere não reconhecido
            ('MISMATCH', r'.')
        ]

        tokens_join = '|'.join('(?P<%s>%s)' % x for x in rules)
        print(tokens_join, '\n\n\n')
        lin_start = 0

        token = []
        lexeme = []
        row = []
        column = []

        for m in re.finditer(tokens_join, code):
            token_type = m.lastgroup
            print(token_type)
            
            token_lexeme = m.group(token_type)
            print(token_lexeme)

            if token_type == 'NEWLINE':
                lin_start = m.end()
                self.lin_num += 1
            elif token_type == 'SKIP':
                continue
            elif token_type == 'COMMENT':
                continue
            elif token_type == 'MISMATCH':
                print(1)
                print(f"token_lexeme: {token_lexeme}, token_type: {token_type}")
                raise RuntimeError('%r unexpected on line %d' %
                                   (token_lexeme, self.lin_num))
            else:
                col = m.start() - lin_start
                column.append(col)
                token.append(token_type)
                lexeme.append(token_lexeme)
                row.append(self.lin_num)

                print('Token = {0}, Lexeme = \'{1}\', Row = {2}, Column = {3}'
                      .format(token_type, token_lexeme, self.lin_num, col))

        all_tokens = []
        for i in range(len(token)):
            all_tokens.append({
                "type": token[i],
                "lexeme": lexeme[i],
                "line": row[i], 
                "column": column[i]
            })

        return all_tokens

if (__name__ == "__main__"):
    codigo_funciona = """
    program;
    //opa tudo bem
    var: int;
    begin
        := 10;
        write("Hello World");
    end
    """

    lex = lexical_analyzer()
    teste = lex.tokens(codigo_funciona)
    pprint(teste)
    
