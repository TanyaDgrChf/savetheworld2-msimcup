#This is a placeholder using a third party ai before the website is fully developed
import requests
import sqlite3
from apiKeys import key, secret

IMAGGA_API_KEY = key
IMAGGA_API_SECRET = secret

def sendImage(image_url):
    response = requests.get(
        f'https://api.imagga.com/v2/tags?image_url={image_url}&language=en',
        auth=(IMAGGA_API_KEY, IMAGGA_API_SECRET)
    )
    if response.status_code == 200:
        tags = response.json()['result']['tags']
        guesses = [tag['tag'] for tag in tags]
        return guesses
    else:
        return []

def checkText(tags):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("SELECT keyword FROM keywords")
    keywords = c.fetchall()
    conn.close()

    results = []

    for tag in tags:
        found = False
        for keyword in keywords:
            if tag.lower() == keyword[0].lower():
                results.append(keyword[0])
                found = True
                break
        if not found:
            results.append('not in archive')
    
    return results
