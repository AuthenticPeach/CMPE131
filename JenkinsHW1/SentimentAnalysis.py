# write a program that does the following in Python:

# 1. Takes a text string as input

# 2. Outputs a message about the sentiment of the text string, whether it’s “Positive”, “Negative” or “Neutral”.
from textblob import TextBlob

def sentiment_analysis(text):
    analysis = TextBlob(text)
    if analysis.sentiment.polarity > 0:
        return "Positive"
    elif analysis.sentiment.polarity == 0:
        return "Neutral"
    else:
        return "Negative"

text = input("Enter a text string: ")
sentiment = sentiment_analysis(text)
print("Sentiment:", sentiment)

