
from tokenizer import TokenType
from custom_parser import Parser,TreeNode
from interface import QueryGenerator

class PosgersQueryGenerator(QueryGenerator):
    table_name = None
    column_name = None
    def __init__(self,table_name:str,column_name:str) -> None:
        self.table_name = table_name
        self.column_name = column_name
        
    def getQuery(self,exp:str):
        parser = Parser(exp)
        full_query = "SELECT * FROM " + self.table_name + " WHERE "
        full_query += self._generateQuery(parser.root)+";"
        return full_query

    def _generateQuery(self,root: TreeNode):
        if root.tokenType == TokenType.OR:
            leftQuery = self._generateQuery(root.left)
            rightQuery = self._generateQuery(root.right)
            return "(" + leftQuery + " OR " + rightQuery +  ")"
        elif root.tokenType == TokenType.AND:
            leftQuery = self._generateQuery(root.left)
            rightQuery = self._generateQuery(root.right)
            return "(" + leftQuery + " AND " + rightQuery +  ")"
        elif root.tokenType == TokenType.STR:
            return " " + self.column_name + " LIKE '%" + root.value + "%' "
        else:
            raise Exception("Invalid Token Type")


if __name__ == "__main__":
    table_name = "resume"
    column_name = "text"
    exp = '(Java AND Spring) OR (Python AND Django) OR (Ruby AND ("Ruby on Rails" OR ROR) AND \'Hello world\')'
    QG = PosgersQueryGenerator(table_name,column_name)
    query = QG.getQuery(exp)
    print(query)