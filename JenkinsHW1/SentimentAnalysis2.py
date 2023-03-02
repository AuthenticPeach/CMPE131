# write a program that does the following in Python, without a library:

# 1. Takes a text string as input

# 2. Outputs a message about the sentiment of the text string, whether it’s “Positive”, “Negative” or “Neutral”.

positive_words = ["good", "great", "excellent", "amazing", "love", "nice", "fantastic", "happy", "pleased", "delighted"]
negative_words = ["bad", "terrible", "awful", "hate", "dislike", "not good", "sad", "unhappy", "displeased", "depressed"]

def sentiment_analysis(text):
    words = text.lower().split()
    positive_count = 0
    negative_count = 0
    for word in words:
        if word in positive_words:
            positive_count += 1
        elif word in negative_words:
            negative_count += 1
    if positive_count > negative_count:
        return "Positive"
    elif positive_count < negative_count:
        return "Negative"
    else:
        return "Neutral"

text = input("Enter a text string: ")
sentiment = sentiment_analysis(text)
print("Sentiment:", sentiment)
