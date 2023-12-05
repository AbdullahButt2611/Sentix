from django.shortcuts import render

import spacy, nltk, requests, openai, json, re
from nltk.sentiment import SentimentIntensityAnalyzer



def indexPage(request):
    data_dict = {}

    return render(request, 'index.html', data_dict)





def dashboardPage(request):
    data_dict = {}

    nltk.download('vader_lexicon')


    mixed_reviews = [
        "While the company's revenue increased, the rising expenses were a cause for concern among investors.",
        "Despite a slight dip in profits, the management's strategic initiatives have positioned the company well for future growth.",
        "Investors are skeptical about the recent stock market rally, fearing a potential correction in the coming months.",
        "The bond market saw some turbulence, but savvy investors capitalized on the volatility to secure attractive yields.",
        "The government's new tax policies received mixed reactions, with some applauding the simplification while others criticized the impact on businesses.",
        "The IPO generated excitement initially, but concerns about the company's long-term sustainability led to a sell-off in the secondary market.",
        "Analysts are divided on the cryptocurrency outlook, with some predicting a continued bull market and others warning of a potential bubble burst.",
        "The central bank's decision to raise interest rates disappointed borrowers but pleased savers looking for higher returns on deposits.",
        "Despite credit rating downgrades, the company's management remains optimistic about its ability to weather economic challenges.",
        "Market volatility created opportunities for day traders, but long-term investors remained cautious, awaiting more stable conditions.",
    ]

    data_dict['total_reviews'] = len(mixed_reviews)
    sentiments = []

    for rev in mixed_reviews:
        sentiments.append(analyze_sentiment(rev))

    data_dict['positive_reviews'] = sentiments.count("positive")
    data_dict['negative_reviews'] = sentiments.count("negative")

    if(data_dict['positive_reviews'] >= data_dict['negative_reviews']):
        data_dict['overall'] = "Good"
    else:
        data_dict['overall'] = "Bad"
    
    return render(request, 'dashboard.html', data_dict)





def reviewsPage(request):
    data_dict = {}

    mixed_reviews = [
        "While the company's revenue increased, the rising expenses were a cause for concern among investors.",
        "Despite a slight dip in profits, the management's strategic initiatives have positioned the company well for future growth.",
        "Investors are skeptical about the recent stock market rally, fearing a potential correction in the coming months.",
        "The bond market saw some turbulence, but savvy investors capitalized on the volatility to secure attractive yields.",
        "The government's new tax policies received mixed reactions, with some applauding the simplification while others criticized the impact on businesses.",
        "The IPO generated excitement initially, but concerns about the company's long-term sustainability led to a sell-off in the secondary market.",
        "Analysts are divided on the cryptocurrency outlook, with some predicting a continued bull market and others warning of a potential bubble burst.",
        "The central bank's decision to raise interest rates disappointed borrowers but pleased savers looking for higher returns on deposits.",
        "Despite credit rating downgrades, the company's management remains optimistic about its ability to weather economic challenges.",
        "Market volatility created opportunities for day traders, but long-term investors remained cautious, awaiting more stable conditions.",
    ]

    data_dict['reviews_sent'] = []

    for rev in mixed_reviews:
        sentiment = analyze_sentiment(rev)
        data_dict['reviews_sent'].append({
            "review": rev,
            "sentiment": sentiment
        })
        

    return render(request, 'reviews.html', data_dict)






def suggestionPage(request, sentiment, review):
    data_dict = {}

    data_dict['sentiment'] = sentiment
    data_dict['review'] = review

    openai.api_key = "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"
    URL = "https://api.openai.com/v1/chat/completions"

    prompt = f""" '{review}' \n\nFor the review provided to you kindly provide what changes can be done in the system to make it better according to the review. Add new line character for each new line if points are there"""

    payload = {
        "model": "gpt-3.5-turbo",
        "messages":
        [
            {
                "role": "user",
                "content": prompt,
            }
        ],
        "temperature" : 1.0,
        "top_p":1.0,
        "n" : 1,
        "stream": False,
        "presence_penalty":0,
        "frequency_penalty":0,
    }

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {openai.api_key}"
    }

    response = requests.post(URL, headers=headers, json=payload, stream=False)
    json_data = json.loads(response.content)
    if 'error' in json_data:
        data_dict["generated_error_text"] = json_data['error']['message']
    else:
        data_dict["generated_text"] = json_data['choices'][0]['message']['content']

    return render(request, 'suggestion.html', data_dict)






def analyze_sentiment(text):

    # Loading Spacy's English Model
    nlp = spacy.load("en_core_web_sm")

    sia = SentimentIntensityAnalyzer()

    # Tokenize the text using SpaCy
    tokens = nlp(text)

    # Join the tokens to form a space-separated string 
    # (NLTK's VADER expects a string)
    text = ' '.join([token.text for token in tokens])

    # Analyze sentiment using VADER
    sentiment_score = sia.polarity_scores(text)['compound']

    # Classify sentiment based on the compound score
    if sentiment_score >= 0.05:
        return 'positive'
    elif sentiment_score <= -0.05:
        return 'negative'
    else:
        return 'neutral'