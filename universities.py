import urllib.request
import json
import pandas
import os

url = 'http://universities.hipolabs.com/search?country=United+States'

urlconn = urllib.request.urlopen(url)
locdata = urlconn.read()
locdata = locdata.decode()

js = json.loads(locdata)

# print(json.dumps(js, indent=4))
# print('Number of universities listed:', len(js))

universities_df = pandas.DataFrame()

for i in range(len(js)):
    temp_df = pandas.DataFrame([js[i]])
    universities_df = pandas.concat([universities_df, temp_df], 
                           axis = 0,
                           ignore_index = True)

filepath = os.getcwd() + '/' + 'universities.csv'
universities_df.to_csv(filepath)

    