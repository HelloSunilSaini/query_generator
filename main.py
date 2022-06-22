
import sys
from elasticsearch import ESQueryGenerator
from posgres import PosgersQueryGenerator
from interface import QueryGenerator

def factory(db_type) -> QueryGenerator:
    if db_type == "ES":
        return ESQueryGenerator
    elif db_type == "Postgres":
        return PosgersQueryGenerator
    else:
        raise Exception("Invalid DB Argument")

if __name__=="__main__":
    n = len(sys.argv)
    i = 0
    if n < 5:
        print("4 arguments required you provided only " + str(n-3) + "\nRequired arguments are: \n1. Database(ES/Postgres)\n2. index/table name\n3. column/field name\n4. Query")
    else:
        DB = factory(sys.argv[1])
        QG = DB(sys.argv[2],sys.argv[3])
        query = QG.getQuery(sys.argv[4])
        print(query)
