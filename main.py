import requests
from bs4 import BeautifulSoup
import re
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation
import spacy
from geotext import GeoText
import folium
from geopy.geocoders import Nominatim
import smtplib


class EnvironmentalNewsAnalysisBot:

    def __init__(self):
        self.news_articles = []
        self.cleaned_articles = []
        self.keywords = []
        self.sentiments = []
        self.geo_locations = []
        self.reports = []
        self.user_preferences = []

    def web_scraping(self, urls):
        for url in urls:
            response = requests.get(url)
            soup = BeautifulSoup(response.content, 'html.parser')
            articles = soup.find_all('article')
            for article in articles:
                text = article.get_text()
                self.news_articles.append(text)

    def data_cleaning(self):
        for article in self.news_articles:
            # Remove advertisements
            article = re.sub(r'Advertisement', '', article)
            # Remove duplicate articles
            if article not in self.cleaned_articles:
                self.cleaned_articles.append(article)

    def natural_language_processing(self):
        # Extract relevant keywords
        tokenizer = nltk.tokenize.RegexpTokenizer(r'\w+')
        vec = CountVectorizer(tokenizer=tokenizer.tokenize)
        matrix = vec.fit_transform(self.cleaned_articles)
        self.keywords = vec.get_feature_names()

        # Perform sentiment analysis
        sid = SentimentIntensityAnalyzer()
        for article in self.cleaned_articles:
            sentiment = sid.polarity_scores(article)
            self.sentiments.append(sentiment)

        # Named Entity Recognition
        nlp = spacy.load('en_core_web_sm')
        for article in self.cleaned_articles:
            doc = nlp(article)
            entities = [ent.text for ent in doc.ents if ent.label_ == 'GPE']
            self.geo_locations.append(entities)

    def topic_modeling(self):
        vec = CountVectorizer(max_df=0.8, min_df=2, stop_words='english')
        matrix = vec.fit_transform(self.cleaned_articles)
        lda = LatentDirichletAllocation(n_components=5, random_state=0)
        lda.fit(matrix)
        self.topics = lda.components_

    def sentiment_analysis(self):
        positive = 0
        negative = 0
        neutral = 0
        for sentiment in self.sentiments:
            if sentiment['compound'] > 0:
                positive += 1
            elif sentiment['compound'] < 0:
                negative += 1
            else:
                neutral += 1
        print(f"Positive articles: {positive}")
        print(f"Negative articles: {negative}")
        print(f"Neutral articles: {neutral}")

    def geo_tagging_mapping(self):
        geolocator = Nominatim(user_agent="environment_bot")
        for locations in self.geo_locations:
            coordinates = []
            for location in locations:
                location_data = geolocator.geocode(location)
                if location_data is not None:
                    coordinates.append([location_data.latitude, location_data.longitude])
            folium.Map(location=[0, 0], zoom_start=2).add_child(
                folium.PolyLine(coordinates, color="red", weight=2.5, opacity=1)).save("map.html")

    def automated_reporting_alerting(self):
        for article in self.cleaned_articles:
            for preference in self.user_preferences:
                if preference in article:
                    self.reports.append(article)
                    break

    def user_interaction(self):
        keyword = input("Enter a keyword to search: ")
        relevant_articles = []
        for article in self.cleaned_articles:
            if keyword in article:
                relevant_articles.append(article)
        for article in relevant_articles:
            print(article)

    def integrate_external_applications(self):
        email = input("Enter your email address: ")
        message = "\r\n".join(self.reports)
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login("your_email_address", "your_password")
        server.sendmail("your_email_address", email, message)
        server.quit()

    def continuous_learning_improvement(self):
        feedback = input("Do you find this article relevant? (yes/no): ")
        if feedback.lower() == "yes":
            self.user_preferences.append(self.keywords[-1])


bot = EnvironmentalNewsAnalysisBot()
bot.web_scraping(['https://example.com'])
bot.data_cleaning()
bot.natural_language_processing()
bot.topic_modeling()
bot.sentiment_analysis()
bot.geo_tagging_mapping()
bot.automated_reporting_alerting()
bot.user_interaction()
bot.integrate_external_applications()
bot.continuous_learning_improvement()