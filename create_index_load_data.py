import requests
import json

index = 'dictionary'
headers = {'content-type': 'application/json'}

print("***** Begin check ES status *****")
r = requests.get('http://localhost:9200/_cluster/health?wait_for_status=yellow&timeout=50s&pretty')
if r.status_code == 200:
    if r.json()['status'] in ('green', 'yellow'):
        print(f"Info: ES status: {r.json()['status']}")
    else:
        raise Exception(f"Error: ES status: {r.json()['status']}")
else:
    raise Exception("Error: request could not get ES health status")
print("***** End check ES status *****")
print("")
print("")

print("***** Begin check if dictionary index exists *****")
r = requests.get('http://localhost:9200/_aliases?pretty=true')
if r.status_code == 200:
    index_exists = 'dictionary' in r.json()
    if index_exists:
        print("Info: Index 'dictionary' already exists in ES")
    else:
        print("Info: Index 'dictionary' did not found in ES")
else:
    raise Exception("Error: could not get indices info")
print("***** End check if dictionary index exists *****")
print("")
print("")


if index_exists == False:  
    print(f"****** Begin create '{index}' index ******")
    # data = json.dumps(
    #     {
    #         "settings": {
    #             "index": {
    #                "number_of_shards": 1,  
    #                "number_of_replicas": 1,
    #                 "analysis": {
    #                     "analyzer": {
    #                         "phrase": {
    #                             "type": "custom",
    #                             "tokenizer": "standard",
    #                             "filter": ["lowercase","shingle"]
    #                         }                            
    #                     },
    #                     "filter": {
    #                         "shingle": {
    #                             "type": "shingle",
    #                             "min_shingle_size": 2,
    #                             "max_shingle_size": 3
    #                         }
    #                     }
    #                 }                        
    #             }
    #         },
    #         "mappings": {
    #             "properties": {
    #                 "word": { 
    #                     "type": "text",
    #                     "analyzer": "phrase"
    #                 }                    
    #             }
    #         }
    #     }
    # )


    data = json.dumps(
        {
            "mappings": {
                "properties": {
                    "word": { 
                        "type": "completion"
                    }                    
                }
            }
        }
    )
    r = requests.put(f'http://localhost:9200/{index}', headers=headers, data=data)
    if r.status_code == 200:
        print(f"Info: Succesfully created index '{index}'")
        print(f"Info: {r.json()}")
    else:
        raise Exception(f"Error: could not create index '{index}' with reason: {r.json()} ")
    print("***** End create '{index}' index ******")
    print("")
    print("")


print("***** Begin check '{index}' index size *****")
r = requests.get(f'http://localhost:9200/{index}/_stats')
if r.status_code == 200:
    index_size = r.json()['indices']['dictionary']['total']['docs']['count']
    print(f"Info: Index '{index}' size is {index_size} docs")
else:
    raise Exception(f"Error: request could not get index '{index}' stats")
print("***** End check '{index}' index size *****")
print("")
print("")


if index_size == 0:
    print("***** Begin add docs to '{index}' index *****")
    with open('words_alpha.txt') as f:
        words = f.read().split()
        #words = words[0:50000]
        dictionary_size = len(words)

    print(f"Info: Read dictionary with size {dictionary_size} words")
    for i in range(dictionary_size):
        data = json.dumps(
            {
                "word":words[i]
            }
        )
        r = requests.put(f'http://localhost:9200/{index}/_doc/{i+1}', headers=headers, data=data)
        if r.status_code != 201:
            raise Exception(f"Error: could not put word '{words[i]}' with position {i} to '{index}' index")

    print(f"Info: Put {dictionary_size} words to '{index}' index")

    
    print("***** End add docs to '{index}' index *****")
    print("")
    print("")

print("Exit")
print("Good bye")


# data = json.dumps(
#     {
#         "suggest": {
#             "word_suggest": {
#                 "text": "blue",
#                 "term": {
#                     "field": "word",
#                     "size": 10,
#                     "sort": "score",
#                     "suggest_mode": "always",
#                     "max_edits": 2,
#                     "prefix_length": 1,
#                     "min_word_length": 3,
#                     "string_distance": "levenshtein"
#                 }
#             }
#         }
#     }
# )

data = json.dumps(
    {
        "suggest": {
            "word_suggest": {
                "prefix": "aux",
                "completion": {
                    "field": "word",
                    "size": 5,
                    "skip_duplicates": "true",
                    "fuzzy": {
                        "fuzziness": "auto:1,3",
                        "transpositions": "true",
                        "min_length": 3,
                        "prefix_length": 2
                    }
                }
            }
        }
    }
)
r = requests.get(f'http://localhost:9200/{index}/_search', headers=headers, data=data)
print(r.status_code)
print(r.json())