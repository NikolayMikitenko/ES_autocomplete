import json
import requests
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-p", "--prefix", help = "Suggest on given prefix.  Default: value = 'ange'.")
parser.add_argument("-s", "--size", help = "Response size. Default: value = 5.")
parser.add_argument("-f", "--fuzziness", help = "Fuzziness. Avliable options 0, 1, 2 or auto:low,high. Default: value = 'auto:1,3'.")
parser.add_argument("-m", "--fuzzy_min_length", help = "Fuzzy min length. Default: value = 3.")
parser.add_argument("-l", "--fuzzy_prefix_length", help = "Fuzzy prefix length.  Default: value = 1.")

args = parser.parse_args()
prefix = args.prefix if args.prefix else 'ange'
size = args.size if args.size else 5
fuzziness = args.fuzziness if args.fuzziness else 'auto:1,3'
fuzzy_min_length = args.fuzzy_min_length if args.fuzzy_min_length else 3
fuzzy_prefix_length = args.fuzzy_prefix_length if args.fuzzy_prefix_length else 1

# print(args)
# print(prefix)
# print(size)
# print(fuzziness)
# print(fuzzy_min_length)
# print(fuzzy_prefix_length)

index = 'dictionary'
headers = {'content-type': 'application/json'}

data = json.dumps(
    {
        "suggest": {
            "word_suggest": {
                "prefix": prefix,
                "completion": {
                    "field": "word",
                    "size": size,
                    "skip_duplicates": "true",
                    "fuzzy": {
                        "fuzziness": fuzziness,
                        "transpositions": "true",
                        "min_length": fuzzy_min_length,
                        "prefix_length": fuzzy_prefix_length
                    }
                }
            }
        }
    }
)
r = requests.get(f'http://localhost:9200/{index}/_search', headers=headers, data=data)
if r.status_code == 200:
    options = r.json()['suggest']['word_suggest'][0]['options']
    if len(options) > 0:
        for i in range(len(options)):
            print(options[i]['text'])
    else:
        print('NOTHING')
else:
    raise Exception("Error: could not request prefix '{prefix}' suggestion.")