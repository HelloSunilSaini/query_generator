# Query Generator

## This is a Query Generator for Postgres and ElasticSearch

##### Please Run below Commads to get Query 
```
Python main.py <DB TYPE> <TABLE NAME> <COLUMN NAME> <STRING QUERY>
```
###### DB TYPE : **ES** OR **Postgres**
###### DB NAME : **Index Name** OR **Table Name**
###### COLUMN NAME : **Field Name** OR **Column Name**
###### STRING QUERY : Ex. "Java OR python"

```
Here are some example runs:

$ python main.py "Postgres" "resume" "text" "\"elastic search\"" 
SELECT * FROM resume WHERE  text LIKE '%elastic search%' ;

$ python main.py "ES" "resume" "text" "\"elastic search\"" 
GET /resume/_search
{
    "query": {
        "match_phrase": {
            "text": "elastic search"
        }
    }
}

$ python main.py "ES" "resume" "text" "(Java AND Spring) OR (Python AND Django) OR (Ruby AND (\"Ruby on Rails\" OR ROR))"
GET /resume/_search
{
    "query": {
        "bool": {
            "should": [
                {
                    "bool": {
                        "must": [
                            {
                                "match": {
                                    "text": "Java"
                                }
                            },
                            {
                                "match": {
                                    "text": "Spring"
                                }
                            }
                        ]
                    }
                },
                {
                    "bool": {
                        "should": [
                            {
                                "bool": {
                                    "must": [
                                        {
                                            "match": {
                                                "text": "Python"
                                            }
                                        },
                                        {
                                            "match": {
                                                "text": "Django"
                                            }
                                        }
                                    ]
                                }
                            },
                            {
                                "bool": {
                                    "must": [
                                        {
                                            "match": {
                                                "text": "Ruby"
                                            }
                                        },
                                        {
                                            "bool": {
                                                "should": [
                                                    {
                                                        "match_phrase": {
                                                            "text": "Ruby on Rails"
                                                        }
                                                    },
                                                    {
                                                        "match": {
                                                            "text": "ROR"
                                                        }
                                                    }
                                                ]
                                            }
                                        }
                                    ]
                                }
                            }
                        ]
                    }
                }
            ]
        }
    }
}

$ python main.py "Postgres" "resume" "text" "(Java AND Spring) OR (Python AND Django) OR (Ruby AND (\"Ruby on Rails\" OR ROR))" 
SELECT * FROM resume WHERE (( text LIKE '%Java%'  AND  text LIKE '%Spring%' ) OR (( text LIKE '%Python%'  AND  text LIKE '%Django%' ) OR ( text LIKE '%Ruby%'  AND ( text LIKE '%Ruby on Rails%'  OR  text LIKE '%ROR%' ))));

```
