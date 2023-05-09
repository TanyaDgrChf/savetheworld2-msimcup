import requests
from apiKeys import imgBB
api_key = imgBB
def sendImage(image_url):
    response = requests.post(
        f'https://api.imagga.com/v2/tags?image_url={image_url}&language=en',
        auth=(api_key)
    )