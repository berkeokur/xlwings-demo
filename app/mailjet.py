# import the mailjet wrapper
from mailjet_rest import Client
import sys
import os

from dotenv import load_dotenv
load_dotenv()

# Get your environment Mailjet keys
api_key = os.getenv('MJ_APIKEY_PUBLIC')
api_secret = os.getenv('MJ_APIKEY_PRIVATE')

print(api_key, api_secret)
sender_email = "mng.fusion.cuisine@gmail.com"


def email_body(guest_name, manager_name, recipient_email, language, review_body, review_title):
    mailjet = Client(auth=(api_key, api_secret), version='v3.1')

    if language == "it":
        intro = "<html><body><p>Gentile " + guest_name \
        +",<p>Ti chiediamo cortesemente di dedicare qualche minuto del tuo prezioso tempo per aiutarci.  " \
        + manager_name + ", il nostro General Manager," \
        + " ci ha detto che questo Venerdì hai avuto un'ottima esperienza presso M&G Fusion Cuisine" \
        + ". </p><p> Ci farebbe immmenso piacerebbe se tu condividessi la tua esperienza.\
        Basandoci sulla tua conversazione con " + manager_name + " abbiamo redatto una possibile recensioni per te. \
        Saresti così gentile da copiarla e pubblicarla su \
        <a href='https://goo.gl/maps/rDbvTLUDbQe45Sdh6'>Google</a>, \
        o il tuo sito di recensioni online preferito? </p><p> Naturalmente puoi modificare la recensione come preferisci. \
        <i>Ti ringraziamo anticipatamente per il tuo prezioso aiuto, e speriamo di rivederti prestissimo!</i></p>"
        closing = "<p>I tuoi amici di M&G Fusion Cuisine!</p></body></html>"
        title = "<p><b>" + review_title + "</b></p>"
        review = "<p><i>" + review_body + "</i></p>"
        content = title + review
        body = intro + content + closing

        subject = f"{guest_name}: Aiutaci a condividere la tua esperienza presso M&G Fusion Cuisine!"

    else: 
        intro = "<html><body><p>Dear " + guest_name \
        +",<p>We hope you will take a few minutes to help us spread the word about our restaurant.  " \
        + manager_name+ ", our " + "General Manager" \
        + " told us you had a nice time at M&G Fusion Cuisine last " \
        + "day" + ". </p><p> We would love your help to let everyone know about your experience. \
        Based on your discussion with " + manager_name + " we drafted three possible reviews for you. \
        Would you be so kind to copy and post the one you prefer to \
        <a href='https://www.yelp.com/writeareview/biz/n-HwtvIHbogu2iCsOc5MQA?return_url=%2Fbiz%2Fn-HwtvIHbogu2iCsOc5MQA&review_origin=biz-details-war-button'>Yelp</a>, \
        <a href='https://www.tripadvisor.com/UserReviewEdit-g40024-d7359790-City_Pork_Jefferson-Baton_Rouge_Louisiana.html'>Tripadvisor</a>, \
        <a href='https://goo.gl/maps/rDbvTLUDbQe45Sdh6'>Google</a>, \
        or your favorite online review site? </p><p> You can of course edit the review as you see fit. \
        <i>Anything you can do to help would be great and we thank you for it!</i></p>"
        closing = "<p>Your friends at M&G Fusion Cuisine!</p></body></html>"
        title = "<p><b>" + review_title + "</b></p>"
        review = "<p><i>" + review_body + "</i></p>"
        content = title + review
        body = intro + content + closing

        subject =  f"{guest_name}: Help us share your experience at M&G Fusion Cuisine!"

    data = {
    'Messages': [
        {
        "From": {
            "Email": sender_email,
            "Name": "M&G Fusion Cuisine Restaturant"
        },
        "To": [
            {
            "Email": recipient_email,
            "Name": guest_name
            }
        ],
        "Bcc": [
        {
          "Email": sender_email,
          "Name": "M&G Fusion Cuisine Restaturant"
        }
        ],
        "Subject": subject,
        "TextPart": "In this prototype email only goes as HTML, if you have text email it won't work",
        "HTMLPart": body
        }
    ]
    }

    result = mailjet.send.create(data=data)
    print("Status code: ", result.status_code)
    print("Result Json: ", result.json())