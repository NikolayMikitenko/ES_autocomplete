# ES_autocomplete 
 
## 1. Run docker container with Elasticsearch 
`docker-compose up` 
 
## 2. Create index and add documents 
`python create_index_load_data.py` 
 
## 3. See suggest help 
`python suggest.py --help`
 
Output 
```
usage: suggest.py [-h] [-p PREFIX] [-s SIZE] [-f FUZZINESS] [-m FUZZY_MIN_LENGTH] [-l FUZZY_PREFIX_LENGTH]

optional arguments:
  -h, --help            show this help message and exit
  -p PREFIX, --prefix PREFIX
                        Suggest on given prefix. Default: value = 'ange'.
  -s SIZE, --size SIZE  Response size. Default: value = 5.
  -f FUZZINESS, --fuzziness FUZZINESS
                        Fuzziness. Avliable options 0, 1, 2 or auto:low,high. Default: value = 'auto:1,3'.
  -m FUZZY_MIN_LENGTH, --fuzzy_min_length FUZZY_MIN_LENGTH
                        Fuzzy min length. Default: value = 3.
  -l FUZZY_PREFIX_LENGTH, --fuzzy_prefix_length FUZZY_PREFIX_LENGTH
                        Fuzzy prefix length. Default: value = 1.
```
 
## 4. Request autocomplete for prefix 
 `python suggest.py -p 'b'` 
 
Output 
```
b
ba
baa
baaed
baahling
``` 
 
 `python suggest.py -p 'ba'` 
 
Output 
```
ba
baa
baaed
baahling
baaing
``` 
 
 `python suggest.py -p 'bas'` 
 
Output 
```
b
ba
baa
baaed
baahling
``` 
 
 `python suggest.py -p 'base'` 
 
Output 
```
ba
baa
baaed
baahling
baaing
``` 
 
 `python suggest.py -p 'baset'` 
 
Output 
```
bas
basad
basal
basale
basalia
``` 
 
 `python suggest.py -p 'baseta'` 
 
Output 
```
base
baseball
baseballdom
baseballer
baseballs
``` 

`python suggest.py -p 'basetal'` 

```
baseball
baseballdom
baseballer
baseballs
baseband
``` 
