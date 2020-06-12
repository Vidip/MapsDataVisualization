from flask import Flask, render_template, request, session, redirect
import requests
import base64
import json
from datetime import date
from tweepy import API
from tweepy import OAuthHandler

import credentials
import numpy as np
import pandas as pd
import re

app = Flask(__name__)
CLIENT_SECRET = ''
app.secret_key = "visualize"


class CreateTwitterClient:
    def __init__(self):
        self.auth = TwitterAuthenticator().authenticate_twitter_app()
        self.twitter_client = API(self.auth)

    def get_twitter_client_api(self):
        return self.twitter_client


class TwitterAuthenticator:

    def authenticate_twitter_app(self):
        auth = OAuthHandler(credentials.CONSUMER_KEY, credentials.CONSUMER_SECRET)
        auth.set_access_token(credentials.ACCESS_TOKEN, credentials.ACCESS_TOKEN_SECRET)
        return auth


class TweetAnalyzer:

    def tweet_text_only(selfs, tweets):
        df = pd.DataFrame(
            data=[re.sub(r"[^a-zA-Z0-9@.!#$&':<>%()]+", ' ', re.sub(r'http=\S+', '', tweet.text)) for tweet in tweets],
            columns=['Tweets'])
        df['profile_image_url'] = np.array([tweet.user.profile_image_url_https for tweet in tweets])

        return df


twitter_client = CreateTwitterClient()
tweet_analyzer = TweetAnalyzer()
api = twitter_client.get_twitter_client_api()


@app.route("/")
def index():
    res = requests.get("http://ec2-3-81-211-29.compute-1.amazonaws.com:9500/problem/")
    new_dict = dict()
    issue_list = []
    print(res.json())
    for a in res.json():
        new_dict['description'] = a['description']
        new_dict['type'] = a['type']
        new_dict['location'] = a['location']
        issue_list.append(new_dict)
        new_dict = {}
    return render_template('index.html', issues=issue_list)


@app.route("/home", methods=['GET'])
def home():
    print(request.args['survey'])
    response = requests.get("http://ec2-3-81-211-29.compute-1.amazonaws.com:9500/" + request.args['survey'])
    print(response.json())
    count_of_first = 0
    count_of_first_not = 0
    count_of_second_not = 0
    count_of_third_not = 0
    count_of_second = 0
    count_of_third = 0
    count_of_first_agegroup = 0
    count_of_second_agegroup = 0
    count_of_thrid_agegroup = 0
    count_of_fourth_agegroup = 0
    data4 = []
    data5 = []
    for r in response.json():
        if r['first'] == 'Yes':
            count_of_first += 1
        else:
            count_of_first_not += 1
        if r['second'] == 'Yes':
            count_of_second += 1
        else:
            count_of_second_not = 0
        if r['third'] == 'Yes':
            count_of_third += 1
        else:
            count_of_third_not = 0
        if r['sixth'] == 'Less than 20':
            count_of_first_agegroup += 1
        elif r['sixth'] == '20-30':
            count_of_second_agegroup += 1
        elif r['sixth'] == '30-50':
            count_of_thrid_agegroup += 1
        else:
            count_of_fourth_agegroup += 1
        loc = r['fourth']
        location = requests.get(
            "http://www.mapquestapi.com/geocoding/v1/address?key=17sWk6Q67A5GgdBYjpDCswbCHAMnUAqc&location=" + loc + ",Halifax,Canada")
        print(location.json()['results'][0]['locations'][0]['latLng'])
        if r['first'] == 'Yes' and r['second'] == 'Yes':
            data4.append([location.json()['results'][0]['locations'][0]['latLng']['lat'],
                          location.json()['results'][0]['locations'][0]['latLng']['lng']])
        else:
            data5.append([location.json()['results'][0]['locations'][0]['latLng']['lat'],
                          location.json()['results'][0]['locations'][0]['latLng']['lng']])
    data = [{"group": "Yes", "value": count_of_first}, {"group": "No", "value": count_of_first_not}]
    data2 = [{"group": "Yes", "value": count_of_second}, {"group": "No", "value": count_of_second_not}]
    data3 = [{"group": "Yes", "value": count_of_third}, {"group": "No", "value": count_of_third_not}]
    user = ''
    if session.get('token_id'):
        user = session['token_id']
    data6 = {"A": count_of_first_agegroup, "B": count_of_second_agegroup, "C": count_of_thrid_agegroup,
             "D": count_of_fourth_agegroup}

    query_strings = ["Halifax Transport", "hfxtransit"]

    for qu in query_strings:
        tweets = api.search(q=qu, count=10, result_type='recent', lang="en")
        df1 = tweet_analyzer.tweet_text_only(tweets)

    tweet_text = df1['Tweets'].values.tolist()
    tweet_image_url = df1['profile_image_url'].values.tolist()
    tweet_info = zip(tweet_text, tweet_image_url)

    return render_template('home.html', data=data, val=10, data2=data2, data3=data3, geodata=data4,
                           negativegeodata=data5, agegroup=data6, survey="Halifax Transit Tracker",
                           tweet_info=tweet_info)


@app.route("/home/health", methods=['GET'])
def home_secondsurvey():
    print(request.args['survey'])
    response = requests.get("http://ec2-3-81-211-29.compute-1.amazonaws.com:9500/covSurvey")
    print(response.json())
    count_of_first = 0
    count_of_first_not = 0
    count_of_second_not = 0
    count_of_third_not = 0
    count_of_second = 0
    count_of_third = 0
    count_of_first_agegroup = 0
    count_of_second_agegroup = 0
    count_of_thrid_agegroup = 0
    count_of_fourth_agegroup = 0
    data4 = []
    data5 = []
    for r in response.json():
        if r['first'] == 'Yes':
            count_of_first += 1
        else:
            count_of_first_not += 1
        if r['second'] == 'Yes':
            count_of_second += 1
        else:
            count_of_second_not = 0
        if r['third'] == 'Yes':
            count_of_third += 1
        else:
            count_of_third_not = 0
        if r['sixth'] == 'Less than 20':
            count_of_first_agegroup += 1
        elif r['sixth'] == '20-30':
            count_of_second_agegroup += 1
        elif r['sixth'] == '30-50':
            count_of_thrid_agegroup += 1
        else:
            count_of_fourth_agegroup += 1
        loc = "Spring Garden"
        location = requests.get(
            "http://www.mapquestapi.com/geocoding/v1/address?key=17sWk6Q67A5GgdBYjpDCswbCHAMnUAqc&location=" + loc + ",Halifax,Canada")
        print(location.json()['results'][0]['locations'][0]['latLng'])
        if r['first'] == 'Yes':
            data4.append([location.json()['results'][0]['locations'][0]['latLng']['lat'],
                          location.json()['results'][0]['locations'][0]['latLng']['lng']])
        else:
            data5.append([location.json()['results'][0]['locations'][0]['latLng']['lat'],
                          location.json()['results'][0]['locations'][0]['latLng']['lng']])
    data = [{"group": "Yes", "value": count_of_first}, {"group": "No", "value": count_of_first_not}]
    data2 = [{"group": "Yes", "value": count_of_second}, {"group": "No", "value": count_of_second_not}]
    data3 = [{"group": "Yes", "value": count_of_third}, {"group": "No", "value": count_of_third_not}]
    user = ''
    if session.get('token_id'):
        user = session['token_id']
    data6 = {"A": count_of_first_agegroup, "B": count_of_second_agegroup, "C": count_of_thrid_agegroup,
             "D": count_of_fourth_agegroup}

    query_strings = ["Nova Scotia Covid19", "nsgov"]

    for qu in query_strings:
        tweets = api.search(q=qu, count=10, result_type='recent', lang="en")
        df1 = tweet_analyzer.tweet_text_only(tweets)

    tweet_text = df1['Tweets'].values.tolist()
    tweet_image_url = df1['profile_image_url'].values.tolist()
    tweet_info = zip(tweet_text, tweet_image_url)

    return render_template('home.html', data=data, val=10, data2=data2, data3=data3, geodata=data4,
                           negativegeodata=data5, agegroup=data6, survey="COVID-19 Response Tracker",
                           tweet_info=tweet_info)


@app.route("/get/issues")
def get_issues():
    res = requests.get("http://ec2-3-81-211-29.compute-1.amazonaws.com:9500/problem/")
    new_dict = dict()
    issue_list = []
    print(res.json())
    for a in res.json():
        new_dict['description'] = a['description']
        new_dict['type'] = a['type']
        new_dict['location'] = a['location']
        issue_list.append(new_dict)
        return render_template('index.html', issues=issue_list)


@app.route("/get/surveydata", methods=['GET'])
def getallcities():
    results = requests.get("http://ec2-3-81-211-29.compute-1.amazonaws.com:9500/busSurvey")
    print(results)
    return render_template('home.html')


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
