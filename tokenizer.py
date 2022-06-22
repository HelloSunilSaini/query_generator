

class TokenType:
    LP, RP, STR, AND, OR = range(5)

class Tokenizer:
    expression = None
    tokens = None
    tokenTypes = None
    i = 0
    
    def __init__(self, exp:str):
        self.expression = exp
    
    def next(self):
        self.i += 1
        return self.tokens[self.i-1]
	
    def hasNext(self):
        return self.i < len(self.tokens)
    
    def nextTokenType(self):
        return self.tokenTypes[self.i]
    
    def tokenize(self):
        import re
        reg = re.compile(r'(\bAND\b|\bOR\b|\(|\))')
        self.tokens = reg.split(self.expression)
        self.tokens = [t.strip() for t in self.tokens if t.strip() != '']
        self.tokenTypes = []
        for i,t in enumerate(self.tokens):
            if t == 'AND':
                self.tokenTypes.append(TokenType.AND)
            elif t == 'OR':
                self.tokenTypes.append(TokenType.OR)
            elif t == '(':
                self.tokenTypes.append(TokenType.LP)
            elif t == ')':
                self.tokenTypes.append(TokenType.RP)
            else:
                if t[0] == '"' and t[-1] == '"' :
                    self.tokens[i] = t.replace('"','').strip()
                elif t[0] == "'" and t[-1] == "'":
                    self.tokens[i] = t.replace("'",'').strip()
                self.tokenTypes.append(TokenType.STR)

if __name__ == "__main__":
    exp = '(Java AND Spring) OR (Python AND Django) OR (Ruby AND ("Ruby on Rails" OR ROR) AND \'Hello world\')'
    QT = Tokenizer(exp)
    QT.tokenize()
    print("tokens",QT.tokens)
    print("tokens types",QT.tokenTypes)