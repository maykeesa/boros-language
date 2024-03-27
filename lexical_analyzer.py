import re

class lexical_analyzer:

    def tokens(self, code):
        rules = [
            ('PROGRAM', r'^program$'),
            ('INTEGER', r'^int$'),
            ('BOOLEAN', r'^bool$'),
            ('BEGIN', r'^begin$'),
            ('END', r'^end$'),
            ('WHILE', r'^while$'),
            ('DO', r'^do$'),
            ('READ', r'^read$'),
            ('VAR', r'^var$'),
            ('FALSE', r'^false$'),
            ('TRUE', r'^true$'),
            ('WRITE', r'^write$'),
            ('NUMBER', r'^[+-]?\d+$'),                
            ('OPAD', r'\+'),           
            ('OPAD', r'\-'),              
            ('OPMULT', r'\*'),              
            ('OPMULT', r'\/'),              
            ('OPREL', r'>'),              
            ('OPREL', r'<'),            
            ('OPREL', r'>='),             
            ('OPREL', r'<='),            
            ('OPREL', r'=='),                 
            ('OPREL', r'<>'),
            ('OPLOG', r'^or$'),            
            ('OPLOG', r'^and$'),
            ('OPNEG', r'~'),
            ('PVIG', r';'),             
            ('PONTO', r'\.'),     
            ('DPONTOS', r':'),   
            ('VIG', r','),          
            ('ABPAR', r'\('),         
            ('FPAR', r'\)'),        
            ('ATRIB', r':='),
            ('COM', r'\/\/'),
        ]

        tokens_join = '|'.join('(?P<%s>%s)' % x for x in rules)
        lin_start = 0

        print(tokens_join)
        
        token = []
        lexeme = []
        row = []
        column = []

if(__name__ == "__main__"):
    lex = lexical_analyzer()
    lex.tokens("program begin do +543 read end")
