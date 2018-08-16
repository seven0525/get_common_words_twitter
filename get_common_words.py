#!/usr/bin/env python                                                                                                                                             
# -*- coding:utf-8 -*-  
import json
from requests_oauthlib import OAuth1Session
from twitter import Twitter, OAuth
from janome.tokenizer import Tokenizer
import collections
import re
from collections import Counter, defaultdict
import sys, json, time, calendar
from datetime import datetime
from dateutil.relativedelta import relativedelta

#APIキーの設置
CONSUMER_KEY =  'kbIE5ZLubgsSDL1T73SQXH63J'
CONSUMER_SECRET = 'fCO2y2zwcHXgceNNWkE2DLSgy9rf53pOKS7E36YAA5PAKIQkXU'
ACCESS_TOKEN = '2811495061-3vMWEm62DhMuY2blPMgE7tEO4zRd7jdA0Z55XiQ'
ACCESS_SECRET = '3XzJUVD0bAV2WCoLUgpFd2hyDHguvfxGCfbGF3YfUJeMZ'

t = Twitter(auth=OAuth(
    ACCESS_TOKEN,
    ACCESS_SECRET,
    CONSUMER_KEY,
    CONSUMER_SECRET
))
    
twitter = OAuth1Session(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_SECRET)
url = "https://api.twitter.com/1.1/search/tweets.json"
userTweets = []


def final_get_usertweets(user_id, tweet_id):
    remain = True #ループ判定
    max_id = tweet_id
    remainNum = 0
    numberOfTweets = 200 #取ってくるtweetの数
    count = 200 #一度のアクセスで何件取ってくるか
    while remain:
        aTimeLine = t.statuses.user_timeline(user_id = user_id, count=count, max_id=max_id)
        for tweet in aTimeLine:
            if  tweet['text'] in userTweets:
                remain = False
                break
            userTweets.append(tweet['text'])
#         max_id = aTimeLine[-1]['id']-1
#         remainNum = numberOfTweets - len(userTweets)
#         count = remainNum
        if len(userTweets)+1 > numberOfTweets:
            remain = False

            
def YmdHMS(created_at):
    time_utc = time.strptime(created_at, '%a %b %d %H:%M:%S +0000 %Y')
    unix_time = calendar.timegm(time_utc)
    time_local = time.localtime(unix_time)
    japan_time = time.strftime("%Y-%m-%d %H:%M:%S", time_local)
    return japan_time


def get_userstweets(user_id, tweet_id, keyword_posted_at):
    
    #キーツイートの2ヶ月前の日にちを計算して取得
    keyword_posted_at = YmdHMS(keyword_posted_at)
    kdatetime = datetime.strptime(keyword_posted_at, '%Y-%m-%d %H:%M:%S')
    to_dt = kdatetime - relativedelta(months=2)
    
    #2ヶ月前のツイートをsearch
    remain = True #ループ判定
    max_id = tweet_id
    remainNum = 0
    #numberOfTweets = 100 #取ってくるtweetの数
    count = 100 #一度のアクセスで何件取ってくるか
    searched_count = 0
#     aaa = 0
    while remain:
        aTimeLine = t.statuses.user_timeline(user_id = user_id, count=count, max_id=max_id)
        for tweet in aTimeLine:
            #カウント
            searched_count += 1
#             aaa += 1
#             print(aaa)
            
            #datetime型に変換
            created_at = tweet["created_at"]
            time_stamp = YmdHMS(created_at)
            tdatetime = datetime.strptime(time_stamp, '%Y-%m-%d %H:%M:%S')
            
            #キーワード2ヶ月前のツイートを見つけたら、final_get_usertweetsを実施してリストに格納
            if  tdatetime <= to_dt:
                max_id = tweet['id']
                final_get_usertweets(user_id,max_id)
                remain = False
                break
                
            else:
                continue
        
        try:
            max_id = aTimeLine[-1]['id']-1
        except:
            remain = False
# #         remainNum = numberOfTweets - len(userTweets)
# #         count = remainNum
        if searched_count >= 30:
            remain = False


#名詞だけ抽出、単語をカウント
def counter(texts):
    t = Tokenizer()
    words_count = defaultdict(int)
    words = []
    for text in texts:
        text=re.sub(r'https?://[\w/:%#\$&\?\(\)~\.=\+\-…]+', "", text)
        text=re.sub('RT', "", text)
        text=re.sub('お気に入り', "", text)
        text=re.sub('まとめ', "", text)
        text=re.sub(r'[!-~]', "", text)#半角記号,数字,英字
        text=re.sub(r'[︰-＠]', "", text)#全角記号
        text=re.sub('\n', "", text)#改行文字
        tokens = t.tokenize(text)
        for token in tokens:
            #品詞から名詞だけ抽出
            pos = token.part_of_speech.split(',')[0]
            if pos == '名詞':
                words_count[token.base_form] += 1
                words.append(token.base_form)
    string_words = ','.join(words)
    string_words = re.sub(',', "", string_words)
    c = collections.Counter(t.tokenize(string_words, wakati=True))
    mc = c.most_common()
    return mc


#キーワードを含むツイートを３つ取得
def catch_3_tweets(word):
    tweets_list = []
    for tweet in userTweets:
        if word in tweet:
            tweets_list.append(tweet)
    return(tweets_list[0:3])
    

#検索したい文字を指定 
print("何を調べますか?")
keyword = input('>> ')
print('----------------------------------------------------')


params = {'q' : keyword, 'count' : 20}
req = twitter.get(url, params = params)
userTweets = [] #tweetの格納先
number_keypeople = 0
number_gotpeople = 0

if req.status_code == 200:
    search_timeline = json.loads(req.text)
    for tweet in search_timeline['statuses']:
        number_keypeople += 1
        user_id = tweet["user"]["id"]
        tweet_id = tweet["id"]
        created_at = tweet['created_at']
        get_userstweets(user_id,tweet_id,created_at)
else:
    print("ERROR: %d" % req.status_code)


common_word = counter(userTweets)
top_common_word = common_word[0:10]

key_tweets = []
for key_word in  top_common_word:
    word = key_word[0]
    keytweet = catch_3_tweets(word)
    key_tweets.append(keytweet)
    
#key_tweetsにそれぞれのワードを含むツイートが３つずつ含まれているので好きに抽出してください    
print(top_common_word)


