
from tokenizer import TokenType
from custom_parser import Parser,TreeNode
from interface import QueryGenerator
import json

class ESQueryGenerator(QueryGenerator):
    index_name = None
    field_name = None
    def __init__(self,index_name:str,field_name:str) -> None:
        self.index_name = index_name
        self.field_name = field_name
        
    def getQuery(self,exp:str):
        parser = Parser(exp)
        query = {}
        query["query"] = self._generateQuery(parser.root)
        query_with_index = "GET /" + self.index_name+ "/_search\n"
        query_with_index += json.dumps(query, indent=4)
        return query_with_index

    def _generateQuery(self,root: TreeNode):
        query = {}
        if root.tokenType == TokenType.OR:
            leftQuery = self._generateQuery(root.left)
            rightQuery = self._generateQuery(root.right)
            query["bool"] = {
                "should": [
                    leftQuery,
                    rightQuery
                ]
            }
        elif root.tokenType == TokenType.AND:
            leftQuery = self._generateQuery(root.left)
            rightQuery = self._generateQuery(root.right)
            query["bool"] = {
                "must": [
                    leftQuery,
                    rightQuery
                ]
            }
        elif root.tokenType == TokenType.STR:
            if ' ' in root.value:
                query["match_phrase"] = {self.field_name: root.value}
            else:
                query["match"] = {self.field_name: root.value}
        else:
            raise Exception("Invalid Token Type")
        return query



if __name__ == "__main__":
    index_name = "resume"
    field_name = "text"
    exp = '(Java AND Spring) OR (Python AND Django) OR (Ruby AND ("Ruby on Rails" OR ROR) AND \'Hello World\')'
    # exp = "Java OR python"
    # exp = "Java"
    QG = ESQueryGenerator(index_name,field_name)
    query = QG.getQuery(exp)
    print(query)

