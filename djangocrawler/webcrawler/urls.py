from django.urls import path
from webcrawler import views

urlpatterns = [

    path('crawl/',views.crawl, name='crawl'),

]
