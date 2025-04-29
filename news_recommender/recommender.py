import nltk
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from news_recommender.models import NewsArticle
import numpy as np

nltk.download('stopwords')
from nltk.corpus import stopwords

# Preprocessing function
def preprocess(text):
    if text:
        processed_text = text.lower()
        return processed_text
    return ""

# Build the recommender engine
class NewsRecommender:
    def __init__(self):
        # Load all articles from the database
        self.articles = list(NewsArticle.objects.all())
        print(f"Number of articles loaded: {len(self.articles)}")  # Debugging line

        if not self.articles:
            print("No articles found. Please check the database.")
            return

        self.vectorizer = TfidfVectorizer(stop_words=stopwords.words('english'))

        # Preprocess descriptions and fit the TF-IDF vectorizer
        self.article_descriptions = [preprocess(article.description) for article in self.articles]
        self.tfidf_matrix = self.vectorizer.fit_transform(self.article_descriptions)  # Sparse matrix

    def recommend(self, article_id, top_n=5, sort_by=None):
        # Find the article index
        idx = next((index for (index, d) in enumerate(self.articles) if d.id == article_id), None)
        
        if idx is None:
            print(f"Article ID {article_id} not found.")  # Debugging line
            return ["No recommendations available. The selected article ID is invalid."]

        # Compute similarity scores on-the-fly
        article_vector = self.tfidf_matrix[idx]
        similarity_scores = cosine_similarity(article_vector, self.tfidf_matrix).flatten()

        # Get the top N similar articles
        similarity_scores = list(enumerate(similarity_scores))
        similarity_scores = sorted(similarity_scores, key=lambda x: x[1], reverse=True)
        top_articles = similarity_scores[1:top_n + 1]

        recommendations = []
        for i, score in top_articles:
            recommendations.append(self.articles[i])
            print(f"Recommended article ID: {self.articles[i].id}, Score: {score}")  # Debugging line

        # Sort recommendations by pubDate if specified
        if sort_by == 'date':
            recommendations.sort(key=lambda rec: rec.pubDate, reverse=True)

        if not recommendations:
            return ["No recommendations available based on similarity."]

        return recommendations