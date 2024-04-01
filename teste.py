from lark import Lark
from lexical_analyzer import lexical_analyzer
grammar = """
start: program

program: PROGRAM identifier PVIG decls cmdComp PONTO

decls: empty | VAR listDecl

listDecl: declTip | declTip listDecl

declTip: listId DPONTOS tip PVIG

listId: IDENTIFIER | IDENTIFIER VIG listId

tip: INTEGER | BOOLEAN | STRING

cmdComp: BEGIN listCmd END

listCmd: cmd listCmdTail

listCmdTail: PVIG listCmd | empty

cmd: cmdIf | cmdWhile | cmdWrite | cmdAtrib | cmdComp | cmdRead

cmdIf: IF expr THEN cmd maybeElse

maybeElse: ELSE cmd | empty

cmdWhile: WHILE expr DO cmd

cmdRead: READ LPAR listId RPAR

cmdWrite: WRITE LPAR listW RPAR

elemW: expr | STRING

cmdAtrib: identifier ATRIB expr

expr: term exprTail

exprTail: OPREL term exprTail | empty

term: factor termTail

termTail: OPAD factor termTail | empty

factor: primary factorTail

factorTail: OPMULT primary factorTail | empty

primary: IDENTIFIER | CTE | TRUE | FALSE | LPAR expr RPAR | OPNEG primary

identifier: /[a-zA-Z][a-zA-Z0-9]*/

CTE: /[0-9]+/

STRING: /"(.*?)"/

OPREL: /<=|>=|==|<>/

OPAD: /\+|\-/

OPMULT: /\*|\//

NEG: /\~/

PVIG: /;/

PONTO: /\./

DPONTOS: /:/

VIG: /,/

LPAR: /\(/

RPAR: /\)/

ATTRIB: /:=/

empty:

%import common.WS
%ignore WS
"""



def main():
    code = """
    program teste;
    var: int;
    begin
        := 10;
        write("Hello World");
    end
    """

    parser = Lark(grammar)

    lex = lexical_analyzer()
    tokens = lex.tokens(code)  # Agora tokens é uma lista de dicionários

    tree = parser.parse(tokens)  # Passe a lista de tokens para o parser
    print(tree.pretty())
if __name__ == "__main__":
    


    main()