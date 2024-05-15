from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

client = OpenAI(api_key = os.environ.get("OPENAI_API_KEY"),
)


def get_completion_from_messages(messages):
    response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=messages
    )
    return response.choices[0].message.content

def generate_review(note, lang):
    notes = f""" 
    {note} 
    """
    if lang == "en":
        prompt = f"""
        Write an online review for the restaurant M&G Fusion Cuisine. \
        Base the review on the notes delimited by ``` \
        Do not add any information that is not in these notes: ```{notes}```\
        Never use these adjectives: blown away, lovely, incredible, delightful, indulged in, fantastic, perfect, excellent, wonderful, above and beyond.\
        Make sure the adjectives you use are not repetitive.\
        Don't describe the atmoshpere. \
        Don't generate a review that is incomplete.\
        Anonymize customer names in the notes.\
        Make sure your sentences sound genuine and not forced.\
        Ignore any details of customers that are not related to the restaurant.\
        Don't add motivational quotes for the restaurant.\
        """

        messages =  [  
        {'role':'system', 
        'content':"""You are a customer who writes online reviews to support businesses.\
        You write your reviews with a neutral positive attitude, avoiding exaggerated statements. Your reviews are usually between 40 to 100 words long."""},    
        {'role':'user', 
        'content':prompt},  
        ]
    elif lang == "it":
        prompt = f"""
        Scrivi una recensione online per il ristorante M&G Fusion Cuisine. \
        Basati sulle note delimitate da ``` \
        Non aggiungere alcuna informazione che non sia presente in queste note: ```{notes}```\
        Assicurati che gli aggettivi che utilizzi non siano ripetitivi.\
        Non descrivere l'atmosfera. \
        Non generare una recensione incompleta.\
        Anonimizza i nomi dei clienti nelle note.\
        Assicurati che le tue frasi suonino genuine e non forzate.\
        Ignora eventuali dettagli dei clienti non relativi al ristorante.\
        Non aggiungere citazioni motivazionali per il ristorante.\
        """

        messages =  [  
        {'role':'system', 
        'content':"""Sei un cliente che scrive recensioni online per sostenere le attività commerciali.\
        Scrivi le tue recensioni con un atteggiamento positivo neutro, evitando dichiarazioni esagerate. Di solito le tue recensioni sono lunghe tra i 40 e i 100 parole."""},    
        {'role':'user', 
        'content':prompt},  
        ]
    else:
        print("Unknown language:", lang)

    response = get_completion_from_messages(messages)#type: ignore
    return response

def generate_title(review, language):
    #Create the prompt for the title using a base and the  review text
    if language == "it":
        prompt_title = f"Scrivi un titolo di meno di 10 parole per la seguente recensione del ristorante. \
         Assicurati che il tuo titolo suoni neutro positivo. La recensione è: {review}"
        messages =  [  
            {'role':'system', 
            'content':"Il tuo lavoro è scrivere titoli per le recensioni dei ristoranti"},    
            {'role':'user', 
            'content':prompt_title},  
            ]
    else:
        prompt_title = f"Write a title of less than 10 words for the following \
        restaurant review. Make sure your title sounds neutral positive. The review is: {review}"
        messages =  [  
            {'role':'system', 
            'content':"Your job is to write titles for restaurant reviews"},    
            {'role':'user', 
            'content':prompt_title},  
            ]
    response = get_completion_from_messages(messages)
    return response