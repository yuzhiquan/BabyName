# coding:utf-8
import os
import random
import time

import requests


prefix = "于"
sex = "male" # or female
dict_path = "./dicts"
api_url = "http://route.showapi.com/1026-2"
app_secret=""
appid=""

def make_baby_name(single=True, sex="male"):
    sex_str = "boys" if sex == "male" else "girls"
    name_count = "single" if single else "double"

    dict_name = "names_{sex_str}_{name_count}.txt".format(sex_str=sex_str, name_count=name_count)

    with open(os.path.join(dict_path, dict_name)) as name_dict:
        names = name_dict.readlines()

    return names[random.randint(0,len(names))]

def make_baby_name_random(sex="male"):
    dict_name=["names_boys_single.txt","names_girls_single.txt"]
    names=[]
    for txt in dict_name:
        with open(os.path.join(dict_path, txt)) as name_dict:
            names.append(name_dict.readlines())
    return names[random.randint(0,len(names)/2)] + names[random.randint(len(names)/2, len(names)-1)]



def get_name_score(name, prefix=prefix):

    data = {
        "showapi_appid":appid,
        "showapi_sign":app_secret,
        "xing":prefix,
        "name":name,
    }
    resp = requests.post(api_url, data=data)
    # print resp.json()
    score = resp.json().get("showapi_res_body").get("item").get("score")
    jp = resp.json().get("showapi_res_body").get("item").get("jp").encode("utf-8")
    # print resp.status_code
    # print resp.json().get("showapi_res_body").get("item").get("score")
    # print resp.json().get("showapi_res_body").get("item").get("jp").encode("utf-8")
    return  score,jp



if __name__ == "__main__":
    print "name,score,jp"
    for i in xrange(1000):
        if i%3 == 0:
            name=make_baby_name_random(sex="male")
        else:
            name=make_baby_name(sex="male",single=False)
        try:
            score, jp=get_name_score(name)
        except Exception as e:
            continue
        else:
            print prefix+name, score, jp
            # if int(score) > 90:
            #     print prefix+name, score, jp
        time.sleep(1)
