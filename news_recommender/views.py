from django.shortcuts import render
from .models import NewsArticle
from .recommender import NewsRecommender

def home(request):
    articles = NewsArticle.objects.all()
    recommendations = []
    selected_article_id = None

    if request.method == 'POST':
        selected_article_id = int(request.POST.get('article_id'))
        print(f"Selected Article ID: {selected_article_id}")  # Debugging line
        recommender = NewsRecommender()
        recommendations = recommender.recommend(selected_article_id, top_n=5)
        print(f"Recommendations: {recommendations}")  # Debugging line

    return render(request, 'home.html', {
        'articles': articles,
        'recommendations': recommendations,
        'selected_article_id': selected_article_id,
    })