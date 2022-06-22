from tokenizer import Tokenizer,TokenType

class TreeNode:
    tokenType = None
    value = None
    left = None
    right = None
    
    def __init__(self, tokenType):
        self.tokenType = tokenType

    def __str__(self) -> str:
        return self.value

    def __repr__(self) -> str:
        return self.value
    
    def inorder(self,inorder:list):
        if self.tokenType == TokenType.STR :
            inorder.append(" '" + self.value + "' ")
            return inorder
        else:
            inorder.append("(")
            if not self.left == None:
                self.left.inorder(inorder)
            inorder.append(" " + self.value + " ")
            if not self.right == None:
                self.right.inorder(inorder)
            inorder.append(")")
            return inorder
    
class Parser:
    tokenizer = None
    root = None

    def __init__(self, exp: str):
        self.tokenizer = Tokenizer(exp)
        self.tokenizer.tokenize()
        self._parse()
        
    def _parse(self):
        self.root = self._parseExpression()

    def _parseExpression(self) -> TreeNode:
        stack = []
        while self.tokenizer.hasNext():
            nextTokenType = self.tokenizer.nextTokenType()
            if nextTokenType in [TokenType.STR, TokenType.LP, TokenType.AND, TokenType.OR]:
                node = TreeNode(nextTokenType)
                node.value = self.tokenizer.next()
                stack.append(node)
            elif nextTokenType == TokenType.RP:
                self.tokenizer.next()
                rightElem = stack.pop()
                while not rightElem.tokenType == TokenType.LP:
                    if len(stack) > 0:
                        operElem = stack.pop()
                        if operElem.tokenType == TokenType.LP:
                            stack.append(rightElem)
                            break
                        elif not operElem.tokenType in [TokenType.AND, TokenType.OR]:
                            raise Exception('AND / OR expected, but got ' + operElem.value)
                        elif len(stack) == 0:
                            raise Exception('element expected, before ' + operElem.value)
                        else:
                            leftElem = stack.pop()
                            if leftElem.tokenType == TokenType.LP:
                                raise Exception('element expected, but got ( ')
                            else:
                                operElem.right = rightElem
                                operElem.left = leftElem
                                rightElem = operElem
                    else:
                        raise Exception('element expected, before')

        while len(stack) > 0:
            rightElem = stack.pop()
            if len(stack) > 0:
                operElem = stack.pop()
                if not operElem.tokenType in [TokenType.AND, TokenType.OR]:
                    raise Exception('AND / OR expected, but got ' + operElem.value)
                elif len(stack) == 0:
                    raise Exception('element expected, before ' + operElem.value)
                else:
                    leftElem = stack.pop()
                    if leftElem.tokenType == TokenType.LP:
                        raise Exception('element expected, but got ( ')
                    else:
                        operElem.right = rightElem
                        operElem.left = leftElem
                        stack.append(operElem)
            else:
                return rightElem
  
    def inorder(self):
        inorder = self.root.inorder([])
        return ''.join(inorder)



if __name__ == "__main__":
    exp = '(Java AND Spring) OR (Python AND Django) OR (Ruby AND ("Ruby on Rails" OR ROR) AND \'Hello world\')'
    # exp = 'Java'
    P = Parser(exp)
    print(P.inorder())


# Java 
# Java OR python 
# (Java AND Spring) OR (Python AND Django) OR (Ruby AND ("Ruby on Rails" OR ROR))
