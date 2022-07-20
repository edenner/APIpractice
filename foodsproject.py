import urllib.request
import json
import pandas as pd
from socket import timeout
import os

serviceurl = 'https://api.nal.usda.gov/fdc/v1/foods/'
api_key = 'G4700fz4bJNhfZEcfHErW7795PSfY1Mh3HHVlsnV'

def f_json(task, p):
    url = serviceurl + task + '?api_key=' + api_key + '&pageNumber=' + str(p)
    try: 
        urlconn = urllib.request.urlopen(url)
    except timeout:
        print('socket timed out ')
        return 1
    
    data = urlconn.read()
    data = data.decode()    
    js = json.loads(data)
    return js


def extract_categories(p):
    task = 'search' 
    js = f_json(task, p)
    if js == 1:
        return pd.DataFrame()
    
    entries = js['foodSearchCriteria']['numberOfResultsPerPage']
    
    foods = list()
    for i in range(entries):
        if 'foodCategory' in js['foods'][i]:
            foods.append([js['foods'][i]['fdcId'],
                          js['foods'][i]['foodCategory']])
        else:
            foods.append([js['foods'][i]['fdcId'],
                          'NA'])
        
    ctgs = pd.DataFrame(foods, columns = ['fdcId', 'foodCategory'])
    return ctgs 


def extract_nutrition(p):
    task = 'list'
    js = f_json(task, p)    
    if js == 1:
        return pd.DataFrame()
    
    foods = list()        
    for i in range(len(js)):
         foods.append([js[i]['fdcId'], 
                       js[i]['description'], 
                       js[i]['foodNutrients']])

    nutrn = pd.DataFrame(foods, columns = ['fdcId', 'description', 'foodNutrients'])
    return nutrn


# main
js = f_json('search', 1)
if js == 1:
    exit()

entries_per_page = js['foodSearchCriteria']['numberOfResultsPerPage']
number_of_pages = js['totalPages']

food_df = pd.DataFrame()

first_page = input('Enter first page to be extracted: ')
last_page = input('Enter last page to be extracted: ')

p = first_page
while p <= last_page:
    ntrn = extract_nutrition(p)
    ctgs = extract_categories(p)
    if ntrn.empty or ctgs.empty:
        break
    
    temp_df = pd.merge(ntrn, ctgs, how = 'outer', 
                       left_on = 'fdcId', right_on = 'fdcId')
    food_df = pd.concat([food_df, temp_df], axis = 0, ignore_index = True)
    p+= 1
    
pages = str(first_page) + '-' + str(last_page)
filepath = os.getcwd() + '/nutrition' + pages + '.csv'
food_df.to_csv(filepath)
    
pd.read_csv(filepath)


