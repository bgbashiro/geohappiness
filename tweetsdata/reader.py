import os, sys
import json, csv, re
from datetime import datetime
from TwitterAPI import TwitterAPI
from TwitterAPI.TwitterError import *

def init_api():
    fp = open('credentials.json')
    creds = json.load(fp)
    key = creds['Consumer key']
    key_secret = creds['Secret key']
    token = creds['Access key']
    token_secret = creds['Access secret']
    api = TwitterAPI(key, key_secret, token, token_secret)
    return api

def get_time(twt_time):
    splitted = re.split(r'\+\d{4}', twt_time)
    splitted = map(lambda s:s.strip(), splitted)
    time_str = ' '.join(splitted)
    time = datetime.strptime(time_str, '%c')
    return time.day, time.hour, time.minute

def get_coor(coors):
    try:
        return coors['coordinates'][0], coors['coordinates'][1]
    except:
        # print('no coordinate data, ignoring...')
        return None, None


def main():
    api = init_api()
    #make first reques without max_id
    try:
        res = api.request('search/tweets'
                            , params= { 'q': None  
                                , 'geocode':'55.953251,-3.188267,2mi'
                                , 'count':'1'
                                , 'until':'2018-02-18'})
    except TwitterRequestError as err:
        if (err.status_code == 429):
            print('Ran out of requests, stopping...')
    
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
                                , 'until':'2018-02-18'
                                , 'max_id':str(maxid)})
                checker = False
                
                for twt in res.get_iterator():
                    checker = True
                    day, hour, minute = get_time(twt['created_at'])
                    # print(twt['coordinates'])
                    lat = None
                    lon = None
                    if twt['coordinates']:
                        lat, lon = get_coor(twt['coordinates'])
                        print(str(lat) + ' -- ' + str(lon))
                    
                    csv_pen.writerow([twt['text']
                                    , day
                                    , hour
                                    , minute
                                    , lat
                                    , lon])
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