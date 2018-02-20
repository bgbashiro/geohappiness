import os, sys
import json, csv, re
from datetime import datetime
sys.path.append('TwitterAPI')
from TwitterAPI import TwitterAPI
from TwitterError import *


def init_api():
    fp = open('credentials.json')
    creds = json.load(fp)
    key = creds['Consumer key']
    key_secret = creds['Secret key']
    token = creds['Access key']
    token_secret = creds['Access secret']
    api = TwitterAPI(key, key_secret, token, token_secret)
    return api

def main():
    api = init_api()
    #make first reques without max_id
    res = api.request('search/tweets'
                        , params={ 'q': None  
                                , 'geocode':'55.953251,-3.188267,2mi'
                                , 'count':'1'
                                , 'until':'2018-02-15'})
    maxid = None
    for first_tweet in res.get_iterator():
        maxid = first_tweet['id']

    with open('edinburgh.csv', 'w') as file_edi:
        csv_pen = csv.writer(file_edi)
        while True:
            try:
                res = api.request('search/tweets'
                        , params={ 'q': None  
                                , 'geocode':'55.953251,-3.188267,2mi'
                                , 'count':'100'
                                , 'until':'2018-02-15'
                                , 'max_id':str(maxid)})
                checker = False
                i=0
                for twt in res.get_iterator():
                    checker = True
                    twt_time = twt['created_at']
                    twt_l = map(lambda x:x.strip(), (re.split(r'\+\d{4}', twt_time)))
                    twt_time = datetime.strptime(' '.join(twt_l), '%c')
                    csv_pen.writerow([twt['text'], twt_time.day, twt_time.hour, twt_time.minute])
                    maxid = twt['id']-1
                print(maxid)
                if not checker:
                    break
            except TwitterRequestError as err:
                if (err.status_code == 429):
                    print('Ran out of requests, finishing...')
                    break
                else:
                    print('Error occured. Error code:{}'.format(err.status_code))
                    pass
            

    print('Data scraping finished')


    

main()