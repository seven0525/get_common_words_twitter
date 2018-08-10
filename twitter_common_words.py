#!/usr/bin/env python                                                                                                                                             
# -*- coding:utf-8 -*-  
import json
from requests_oauthlib import OAuth1Session
from twitter import Twitter, OAuth
from janome.tokenizer import Tokenizer
import collections
import re
from collections import Counter, defaultdict

#APIキーの設置
CONSUMER_KEY =  'kbIE5ZLubgsSDL1T73SQXH63J'
CONSUMER_SECRET = 'fCO2y2zwcHXgceNNWkE2DLSgy9rf53pOKS7E36YAA5PAKIQkXU'
ACCESS_TOKEN = '2811495061-3vMWEm62DhMuY2blPMgE7tEO4zRd7jdA0Z55XiQ'
ACCESS_SECRET = '3XzJUVD0bAV2WCoLUgpFd2hyDHguvfxGCfbGF3YfUJeMZ'

twitter = OAuth1Session(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_SECRET)
url = "https://api.twitter.com/1.1/search/tweets.json"

def get_userstweets(user_id, tweet_id):
    t = Twitter(auth=OAuth(
        ACCESS_TOKEN,
        ACCESS_SECRET,
        CONSUMER_KEY,
        CONSUMER_SECRET
    ))

    remain = True #ループ判定
    max_id = tweet_id
    remainNum = 0
    numberOfTweets = 10 #取ってくるtweetの数
    count = 5 #一度のアクセスで何件取ってくるか
    while remain:
        aTimeLine = t.statuses.user_timeline(user_id = user_id, count=count, max_id=max_id)
        for tweet in aTimeLine:
            userTweets.append(tweet['text'])
        max_id = aTimeLine[-1]['id']-1
        remainNum = numberOfTweets - len(userTweets)
        count = remainNum
        if len(userTweets)+1 > numberOfTweets:
            #print(userTweets)
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


#検索したい文字を指定 
print("何を調べますか?")
keyword = input('>> ')
print('----------------------------------------------------')


params = {'q' : keyword, 'count' : 30}
req = twitter.get(url, params = params)
userTweets = [] #tweetの格納先

if req.status_code == 200:
    search_timeline = json.loads(req.text)
    for tweet in search_timeline['statuses']:
        user_id = tweet["user"]["id"]
        tweet_id = tweet["id"]
        get_userstweets(user_id,tweet_id)
    #print(userTweets)
else:
    print("ERROR: %d" % req.status_code)



result = counter(userTweets)
print(result[0:10])


