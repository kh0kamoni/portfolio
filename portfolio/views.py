from django.shortcuts import render
from django.views.generic import TemplateView, ListView
from django.contrib import messages
from .models import Profile, ResearchArea, Publication, Experience, Skill, Statistic, ContactMessage
from django.views.generic import TemplateView
from .models import (
    AcademicDegree, AcademicInstitution, AcademicHonor, 
    AcademicTimelineEvent, AcademicHighlight, Course,
    Affiliation, ProfessionalService, MOOCCourse, MOOCProvider, MOOCCategory


)
from django.views.generic import ListView, DetailView, CreateView
from django.contrib import messages
from django.shortcuts import get_object_or_404
from .models import BlogPost, BlogCategory, BlogTag, BlogComment, BlogSeries


class HomeView(TemplateView):
    template_name = 'portfolio/home.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = Profile.objects.first()
        context['research_areas'] = ResearchArea.objects.all()[:4]
        context['publications'] = Publication.objects.filter(featured=True)[:3]
        context['experiences'] = Experience.objects.all()[:3]
        context['statistics'] = Statistic.objects.all()
        context['skills'] = Skill.objects.all()[:8]  # Show first 8 skills on home
        return context

class AcademicsView(TemplateView):
    template_name = 'portfolio/academics.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = Profile.objects.first()
        
        # Get all academic degrees for timeline
        context['degrees'] = AcademicDegree.objects.select_related('institution').all()
        
        # Get specific degrees
        context['bachelors'] = context['degrees'].filter(degree_type='bachelors').first()
        context['masters'] = context['degrees'].filter(degree_type='masters').first()
        context['phd'] = context['degrees'].filter(degree_type='phd').first()
        context['hsc'] = context['degrees'].filter(degree_type='hsc').first()
        context['ssc'] = context['degrees'].filter(degree_type='ssc').first()
        context['jsc'] = context['degrees'].filter(degree_type='jsc').first()
        context['psc'] = context['degrees'].filter(degree_type='psc').first()
        
        # Create courses_by_degree dictionary
        context['courses_by_degree'] = {}
        for degree in context['degrees']:
            context['courses_by_degree'][degree.id] = Course.objects.filter(degree=degree)
        
        # Get all honors and awards
        context['honors'] = AcademicHonor.objects.select_related('institution', 'degree').all()
        
        # Get timeline events
        context['timeline_events'] = AcademicTimelineEvent.objects.select_related('institution').all()
        
        # Get academic highlights
        context['highlights'] = AcademicHighlight.objects.all()
        
        return context
    
# class AcademicsView(TemplateView):
#     template_name = 'portfolio/academics.html'
    
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['profile'] = Profile.objects.first()
        
#         # Get all academic degrees
#         context['degrees'] = AcademicDegree.objects.select_related('institution').all()
        
#         # Get bachelors degree specifically
#         context['bachelors'] = AcademicDegree.objects.filter(
#             degree_type='bachelors'
#         ).select_related('institution').first()
        
#         # Get HSC degree
#         context['hsc'] = AcademicDegree.objects.filter(
#             degree_type='hsc'
#         ).select_related('institution').first()
        
#         # Get all honors and awards
#         context['honors'] = AcademicHonor.objects.select_related('institution', 'degree').all()
        
#         # Get timeline events
#         context['timeline_events'] = AcademicTimelineEvent.objects.select_related('institution').all()
        
#         # Get academic highlights for stats cards
#         context['highlights'] = AcademicHighlight.objects.all()
        
#         # Get courses for bachelors
#         if context['bachelors']:
#             context['bachelors_courses'] = Course.objects.filter(degree=context['bachelors'])
        
#         return context
    
    
class ResearchView(TemplateView):
    template_name = 'portfolio/research.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['research_areas'] = ResearchArea.objects.all()
        context['profile'] = Profile.objects.first()
        return context

# class PublicationsView(ListView):
#     model = Publication
#     template_name = 'portfolio/publications.html'
#     context_object_name = 'publications'
#     paginate_by = 5
    
#     def get_queryset(self):
#         return Publication.objects.all().order_by('-year', '-order')

from django.views.generic import ListView
from django.db import models as django_models  # Import Django's models for aggregation
from .models import Publication, Profile  # Import your app models

class PublicationsView(ListView):
    model = Publication
    template_name = 'portfolio/publications.html'
    context_object_name = 'publications'
    paginate_by = 5
    
    def get_queryset(self):
        return Publication.objects.all().order_by('-year', '-order')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = Profile.objects.first()
        
        # Get all publications for metrics (not just paginated)
        all_publications = Publication.objects.all()
        
        # Calculate total publications
        context['total_publications'] = all_publications.count()
        
        # Calculate counts by publication type
        context['journal_count'] = all_publications.filter(publication_type='journal').count()
        context['conference_count'] = all_publications.filter(publication_type='conference').count()
        context['book_count'] = all_publications.filter(publication_type='book').count()
        context['preprint_count'] = all_publications.filter(publication_type='preprint').count()
        
        # Get active years range
        years = all_publications.values_list('year', flat=True).distinct().order_by('year')
        if years.exists():
            context['earliest_year'] = years.first()
            context['latest_year'] = years.last()
            context['active_years'] = f"{years.first()}–{years.last()}"
            context['active_years_count'] = years.count()
        else:
            context['earliest_year'] = 2026
            context['latest_year'] = 2026
            context['active_years'] = "2026"
            context['active_years_count'] = 1
        
        # Calculate total citations
        citation_sum = all_publications.aggregate(django_models.Sum('citation_count'))['citation_count__sum']
        context['total_citations'] = citation_sum or 0
        
        # Get featured publications
        context['featured_publications'] = all_publications.filter(featured=True).order_by('-year')[:3]
        
        return context

class ExperienceView(TemplateView):
    template_name = 'portfolio/experience.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['experiences'] = Experience.objects.all().order_by('-start_date')
        context['skills'] = Skill.objects.all().order_by('category', 'order')
        context['profile'] = Profile.objects.first()
        return context

class ContactView(TemplateView):
    template_name = 'portfolio/contact.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = Profile.objects.first()
        return context
    
    def post(self, request, *args, **kwargs):
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        
        ContactMessage.objects.create(
            name=name,
            email=email,
            subject=subject,
            message=message,
            ip_address=request.META.get('REMOTE_ADDR')  # Capture IP address
        )
        
        messages.success(request, 'Thank you for your message! I will get back to you soon.')
        return render(request, self.template_name, self.get_context_data()) 

class AchievementsView(TemplateView):
    template_name = 'portfolio/achievements.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = Profile.objects.first()
        
        # Get all honors and awards
        context['honors'] = AcademicHonor.objects.select_related('institution', 'degree').all()
        
        # Group honors by type
        context['awards'] = AcademicHonor.objects.filter(honor_type='award').select_related('institution')
        context['scholarships'] = AcademicHonor.objects.filter(honor_type='scholarship').select_related('institution')
        context['honors_list'] = AcademicHonor.objects.filter(honor_type='honor').select_related('institution')
        
        # Get timeline events (conferences, workshops, etc.)
        context['achievement_events'] = AcademicTimelineEvent.objects.select_related('institution').all()
        
        # Get statistics for achievements
        context['total_honors'] = AcademicHonor.objects.count()
        context['total_scholarships'] = AcademicHonor.objects.filter(honor_type='scholarship').count()
        context['total_awards'] = AcademicHonor.objects.filter(honor_type='award').count()
        
        return context
    
from django.views.generic import ListView, DetailView
from .models import Project

class ProjectsView(ListView):
    model = Project
    template_name = 'portfolio/projects.html'
    context_object_name = 'projects'
    paginate_by = 6
    
    def get_queryset(self):
        return Project.objects.all().order_by('-featured', '-project_date', '-end_date')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = Profile.objects.first()
        context['featured_projects'] = Project.objects.filter(featured=True)[:3]
        return context

class ProjectDetailView(DetailView):
    model = Project
    template_name = 'portfolio/project_detail.html'
    context_object_name = 'project'
    slug_url_kwarg = 'slug'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = Profile.objects.first()
        # Get related projects (same methods or similar)
        current_project = self.get_object()
        if current_project.methods:
            methods_list = current_project.get_methods_list()
            context['related_projects'] = Project.objects.exclude(
                id=current_project.id
            ).filter(
                featured=True
            )[:3]
        else:
            context['related_projects'] = Project.objects.exclude(
                id=current_project.id
            ).filter(featured=True)[:3]
        return context
    

class AffiliationView(TemplateView):
    template_name = 'portfolio/affiliation.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = Profile.objects.first()
        
        # Get all affiliations grouped by type
        context['academic_positions'] = Affiliation.objects.filter(affiliation_type='academic')
        context['industrial_trainings'] = Affiliation.objects.filter(affiliation_type='industrial')
        context['professional_memberships'] = Affiliation.objects.filter(affiliation_type='professional')
        context['visiting_positions'] = Affiliation.objects.filter(affiliation_type='visiting')
        
        # Get professional services
        context['professional_services'] = ProfessionalService.objects.all()
        
        # If no data exists, provide sample context for display
        if not context['academic_positions'] and not context['industrial_trainings']:
            # This ensures the template shows something even without database data
            context['has_sample_data'] = True
        
        return context
    

class MOOCView(TemplateView):
    template_name = 'portfolio/mooc.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = Profile.objects.first()
        
        # Get all courses
        context['courses'] = MOOCCourse.objects.select_related('provider').all()
        
        
        # Get featured courses
        context['featured_courses'] = MOOCCourse.objects.filter(featured=True).select_related('provider')[:4]
        
        # Get providers for stats
        context['providers'] = MOOCProvider.objects.all()
        context['total_courses'] = MOOCCourse.objects.count()
        context['total_providers'] = MOOCProvider.objects.count()
        
        # Group by provider
        context['courses_by_provider'] = {}
        for provider in context['providers']:
            context['courses_by_provider'][provider.name] = MOOCCourse.objects.filter(provider=provider)
        
        # Get categories
        context['categories'] = MOOCCategory.objects.all()
        
        # Collect all unique skills
        all_skills = []
        for course in context['courses']:
            all_skills.extend(course.get_skills_list())
        context['all_skills'] = list(set(all_skills))  # Remove duplicates
        
        return context
    

from django.db.models import Sum, Q
from django.views.generic import ListView, DetailView
from .models import BlogPost, BlogCategory, BlogTag, Profile

class BlogListView(ListView):
    model = BlogPost
    template_name = 'portfolio/blog_list.html'
    context_object_name = 'posts'
    paginate_by = 6
    
    def get_queryset(self):
        queryset = BlogPost.objects.filter(status='published')
        
        # Filter by category
        category_slug = self.request.GET.get('category')
        if category_slug:
            queryset = queryset.filter(categories__slug=category_slug)
        
        # Filter by tag
        tag_slug = self.request.GET.get('tag')
        if tag_slug:
            queryset = queryset.filter(tags__slug=tag_slug)
        
        # Search
        search_query = self.request.GET.get('q')
        if search_query:
            queryset = queryset.filter(
                Q(title__icontains=search_query) |
                Q(content__icontains=search_query) |
                Q(excerpt__icontains=search_query)
            )
        
        return queryset.distinct()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Add profile
        context['profile'] = Profile.objects.first()
        
        # Add categories and tags
        context['categories'] = BlogCategory.objects.all()
        context['tags'] = BlogTag.objects.all()
        
        # Add featured posts
        context['featured_posts'] = BlogPost.objects.filter(
            status='published', featured=True
        )[:3]
        
        # Add recent posts
        context['recent_posts'] = BlogPost.objects.filter(
            status='published'
        )[:5]
        
        # Calculate total views across ALL published posts
        total_views = BlogPost.objects.filter(
            status='published'
        ).aggregate(Sum('views'))['views__sum'] or 0
        
        # Debug print to console
        print(f"Total views calculated: {total_views}")
        
        # Add to context
        context['total_views'] = total_views
        
        return context

class BlogDetailView(DetailView):
    model = BlogPost
    template_name = 'portfolio/blog_detail.html'
    context_object_name = 'post'
    slug_url_kwarg = 'slug'
    
    def get_queryset(self):
        if self.request.user.is_authenticated:
            return BlogPost.objects.all()
        return BlogPost.objects.filter(status='published')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.get_object()
        
        # Increment view count
        post.views += 1
        post.save()
        
        context['profile'] = Profile.objects.first()
        context['related_posts'] = BlogPost.objects.filter(
            status='published',
            categories__in=post.categories.all()
        ).exclude(id=post.id).distinct()[:3]
        
        context['approved_comments'] = post.comments.filter(
            is_approved=True, parent=None
        )
        
        # Get series information
        context['series'] = post.series.first()
        
        return context
    
    def post(self, request, *args, **kwargs):
        post = self.get_object()
        
        # Handle comment submission
        if 'comment' in request.POST:
            name = request.POST.get('name')
            email = request.POST.get('email')
            content = request.POST.get('content')
            parent_id = request.POST.get('parent_id')
            
            comment = BlogComment(
                post=post,
                name=name,
                email=email,
                content=content,
                ip_address=request.META.get('REMOTE_ADDR')
            )
            
            if parent_id:
                comment.parent_id = parent_id
            
            comment.save()
            messages.success(request, 'Your comment has been submitted and is awaiting approval.')
        
        return self.get(request, *args, **kwargs)

class BlogCategoryView(ListView):
    model = BlogPost
    template_name = 'portfolio/blog_category.html'
    context_object_name = 'posts'
    paginate_by = 6
    
    def get_queryset(self):
        self.category = get_object_or_404(BlogCategory, slug=self.kwargs['slug'])
        return BlogPost.objects.filter(
            status='published',
            categories=self.category
        )
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.category
        context['profile'] = Profile.objects.first()
        return context

class BlogTagView(ListView):
    model = BlogPost
    template_name = 'portfolio/blog_tag.html'
    context_object_name = 'posts'
    paginate_by = 6
    
    def get_queryset(self):
        self.tag = get_object_or_404(BlogTag, slug=self.kwargs['slug'])
        return BlogPost.objects.filter(
            status='published',
            tags=self.tag
        )
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tag'] = self.tag
        context['profile'] = Profile.objects.first()
        return context

class BlogSeriesView(DetailView):
    model = BlogSeries
    template_name = 'portfolio/blog_series.html'
    context_object_name = 'series'
    slug_url_kwarg = 'slug'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['posts'] = self.object.posts.filter(status='published')
        context['profile'] = Profile.objects.first()
        return context
    

class BlogCategoryView(ListView):
    model = BlogPost
    template_name = 'portfolio/blog_category.html'  # Explicitly set
    context_object_name = 'posts'
    paginate_by = 6
    
    def get_queryset(self):
        self.category = get_object_or_404(BlogCategory, slug=self.kwargs['slug'])
        return BlogPost.objects.filter(
            status='published',
            categories=self.category
        )
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.category
        context['profile'] = Profile.objects.first()
        
        # Calculate total views and reading time
        posts = context['posts']
        context['total_views'] = sum(p.views for p in posts)
        context['reading_time'] = sum(p.reading_time_minutes for p in posts)
        
        return context

class BlogTagView(ListView):
    model = BlogPost
    template_name = 'portfolio/blog_tag.html'  # Explicitly set
    context_object_name = 'posts'
    paginate_by = 6
    
    def get_queryset(self):
        self.tag = get_object_or_404(BlogTag, slug=self.kwargs['slug'])
        return BlogPost.objects.filter(
            status='published',
            tags=self.tag
        )
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tag'] = self.tag
        context['profile'] = Profile.objects.first()
        return context

class BlogSeriesView(DetailView):
    model = BlogSeries
    template_name = 'portfolio/blog_series.html'  # Explicitly set
    context_object_name = 'series'
    slug_url_kwarg = 'slug'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['posts'] = self.object.posts.filter(status='published')
        context['profile'] = Profile.objects.first()
        
        # Calculate total reading time
        posts = context['posts']
        context['total_reading_time'] = sum(p.reading_time_minutes for p in posts)
        
        return context
    
from .models import CVE
from django.db.models import Q, Count
from django.views.generic import ListView, DetailView

class CVEListView(ListView):
    model = CVE
    template_name = 'portfolio/cve_list.html'
    context_object_name = 'cves'
    paginate_by = 10
    
    def get_queryset(self):
        queryset = CVE.objects.all()
        
        # Filter by severity
        severity = self.request.GET.get('severity')
        if severity:
            queryset = queryset.filter(severity=severity)
        
        # Filter by year
        year = self.request.GET.get('year')
        if year:
            queryset = queryset.filter(published_date__year=year)
        
        # Search
        search_query = self.request.GET.get('q')
        if search_query:
            queryset = queryset.filter(
                Q(cve_id__icontains=search_query) |
                Q(title__icontains=search_query) |
                Q(description__icontains=search_query) |
                Q(affected_products__icontains=search_query)
            )
        
        return queryset.distinct()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = Profile.objects.first()
        
        # Statistics
        context['total_cves'] = CVE.objects.count()
        context['critical_count'] = CVE.objects.filter(severity='critical').count()
        context['high_count'] = CVE.objects.filter(severity='high').count()
        context['medium_count'] = CVE.objects.filter(severity='medium').count()
        context['low_count'] = CVE.objects.filter(severity='low').count()
        
        # Years for filter
        context['years'] = CVE.objects.dates('published_date', 'year', order='DESC')
        
        # Featured CVEs
        context['featured_cves'] = CVE.objects.filter(featured=True)[:3]
        
        return context

class CVEDetailView(DetailView):
    model = CVE
    template_name = 'portfolio/cve_detail.html'
    context_object_name = 'cve'
    slug_field = 'cve_id'
    slug_url_kwarg = 'cve_id'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = Profile.objects.first()
        
        # Related CVEs (same severity or same year)
        cve = self.get_object()
        context['related_cves'] = CVE.objects.filter(
            Q(severity=cve.severity) | Q(published_date__year=cve.published_date.year)
        ).exclude(id=cve.id)[:3]
        
        return context