import requests
from random import *
from string import *
from bs4 import BeautifulSoup
from json import loads as JSON

def spamForm(url, responseCount):
    questionTypes = {
        0 : 'Short answer',
        1 : 'Paragraph',
        2 : 'Multiple choice',
        3 : 'Dropdown',
        4 : 'Checkboxes',
        9 : 'Date',
        10 : 'Time',
    }
    r = requests.get(url).text
    soup = BeautifulSoup(r, 'html.parser')
    formInfo = soup.find('script', type='text/javascript').text
    x = formInfo.find('FB_PUBLIC_LOAD_DATA_ = ') + 23
    y = formInfo.rfind(';', x)
    formInfo = formInfo[x:y].strip()
    parsed = JSON(formInfo)
    questions = {}
    for text in parsed[1][1]:
        questions[text[4][0][0]] = {'question' : text[1], 'type' : questionTypes[text[3]], 'required' : text[4][0][2]}
        # handles constrained response fields
        if text[3] in [2,3,4]:
            questions[text[4][0][0]]['options'] = []
            for option in text[4][0][1]:
                questions[text[4][0][0]]['options'].append(option[0])
    
    for i in range(responseCount):
        postUrl = url.replace('viewform', 'formResponse?')
        for field in questions:
            if questions[field]['type'] in ['Multiple choice', 'Dropdown', 'Checkboxes']:
                answer = questions[field]['options'][randint(0, len(questions[field]['options'])-1)]
                answer = answer.replace(' ', '+')
            elif questions[field]['type'] in ['Short answer', 'Paragraph']:
                answer = ''.join(choices(ascii_uppercase, k=randint(1, 10)))
            else:
                raise Exception('Unsupported field type')
            postUrl = postUrl + '&entry.' + str(field) + '=' + answer
        requests.get(postUrl)
        print('response sent!')

spamForm('https://docs.google.com/forms/d/e/1FAIpQLSfizuLrxRVxct-KgN6ust-TGedrqgUWpnNxZQn2OhUVDQPBxw/viewform', 100)