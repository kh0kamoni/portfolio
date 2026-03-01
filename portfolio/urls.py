from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('research/', views.ResearchView.as_view(), name='research'),
    path('publications/', views.PublicationsView.as_view(), name='publications'),
    path('experience/', views.ExperienceView.as_view(), name='experience'),
    path('academics/', views.AcademicsView.as_view(), name='academics'),
    path('achievements/', views.AchievementsView.as_view(), name='achievements'),
    path('projects/', views.ProjectsView.as_view(), name='projects'),
    path('projects/<slug:slug>/', views.ProjectDetailView.as_view(), name='project_detail'),
    path('mooc/', views.MOOCView.as_view(), name='mooc'),
    path('contact/', views.ContactView.as_view(), name='contact'),
    path('affiliation/', views.AffiliationView.as_view(), name='affiliation'),
    # Blog URLs
    path('blog/', views.BlogListView.as_view(), name='blog_list'),
    path('blog/<slug:slug>/', views.BlogDetailView.as_view(), name='blog_detail'),
    path('blog/category/<slug:slug>/', views.BlogCategoryView.as_view(), name='blog_category'),
    path('blog/tag/<slug:slug>/', views.BlogTagView.as_view(), name='blog_tag'),
    path('blog/series/<slug:slug>/', views.BlogSeriesView.as_view(), name='blog_series'),
    path('cves/', views.CVEListView.as_view(), name='cve_list'),
    path('cves/<str:cve_id>/', views.CVEDetailView.as_view(), name='cve_detail'),
]