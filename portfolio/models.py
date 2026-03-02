from django.db import models
from django.utils import timezone

class Profile(models.Model):
    """Main profile information"""
    name = models.CharField(max_length=100, default="Khoka Moni")
    alias = models.CharField(max_length=100, blank=True, help_text="Nickname or alias")
    title = models.CharField(max_length=200, default="Security Researcher · MEC CSE")
    email = models.EmailField(default="sourav@stanford.edu")
    university = models.CharField(max_length=200, default="University of Dhaka")
    school = models.CharField(max_length=200, default="Mymensingh Engineering College")
    department = models.CharField(max_length=200, default="Computer Science & Engineering")
    bio = models.TextField()
    profile_image = models.ImageField(upload_to='profile/', blank=True, null=True)
    bio_image = models.ImageField(upload_to='profile/', blank=True, null=True)
    orcid_id = models.URLField(blank=True)
    linkedin_url = models.URLField(blank=True)
    github_url = models.URLField(blank=True)
    google_scholar_url = models.URLField(blank=True)
    cv_file = models.FileField(upload_to='cv/', blank=True, null=True)
    
    class Meta:
        verbose_name_plural = "Profile"
    
    def __str__(self):
        return self.name

class ResearchArea(models.Model):
    """Research areas/interests"""
    title = models.CharField(max_length=200)
    description = models.TextField()
    icon_class = models.CharField(max_length=50, help_text="Font Awesome icon class", 
                                 default="fa-solid fa-battery-half")
    order = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['order']
    
    def __str__(self):
        return self.title

class Publication(models.Model):
    """Publications"""
    PUBLICATION_TYPES = [
        ('journal', 'Journal Article'),
        ('conference', 'Conference Paper'),
        ('book', 'Book Chapter'),
        ('preprint', 'Preprint'),
    ]
    
    title = models.CharField(max_length=500)
    authors = models.CharField(max_length=500)
    journal = models.CharField(max_length=300, blank=True)
    year = models.IntegerField()
    publication_type = models.CharField(max_length=20, choices=PUBLICATION_TYPES)
    doi = models.CharField(max_length=100, blank=True)
    url = models.URLField(blank=True)
    citation_count = models.IntegerField(default=0)
    featured = models.BooleanField(default=False)
    order = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['-year', 'order']
    
    def __str__(self):
        return f"{self.title} ({self.year})"

class Experience(models.Model):
    """Work experience and education"""
    EXPERIENCE_TYPES = [
        ('education', 'Education'),
        ('work', 'Work Experience'),
        ('teaching', 'Teaching'),
    ]
    
    title = models.CharField(max_length=200)
    organization = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    experience_type = models.CharField(max_length=20, choices=EXPERIENCE_TYPES)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    current = models.BooleanField(default=False)
    order = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['-start_date', 'order']
    
    def __str__(self):
        return f"{self.title} at {self.organization}"

class Skill(models.Model):
    """Skills and tools"""
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=50, default="Technical")
    proficiency = models.IntegerField(help_text="1-100", default=80)
    order = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['category', 'order']
    
    def __str__(self):
        return self.name

class Statistic(models.Model):
    """Statistics/achievements"""
    label = models.CharField(max_length=100)
    value = models.CharField(max_length=50)
    description = models.TextField(blank=True)
    icon_class = models.CharField(max_length=50, blank=True)
    order = models.IntegerField(default=0)
    
    class Meta:
        verbose_name_plural = "Statistics"
        ordering = ['order']
    
    def __str__(self):
        return self.label

class ContactMessage(models.Model):
    """Contact form messages"""
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    ip_address = models.GenericIPAddressField(blank=True, null=True)  # Add this line
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.name} - {self.subject}"

class AcademicInstitution(models.Model):
    """Academic institutions"""
    INSTITUTION_TYPES = [
        ('university', 'University'),
        ('college', 'College'),
        ('High school', 'High School'),
        ('Kindergarten', 'Kindergarten'),
    ]
    
    name = models.CharField(max_length=200)
    short_name = models.CharField(max_length=50, blank=True)
    institution_type = models.CharField(max_length=20, choices=INSTITUTION_TYPES)
    location = models.CharField(max_length=200, blank=True)
    logo = models.ImageField(upload_to='institutions/', blank=True, null=True)
    website = models.URLField(blank=True)
    order = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['order']
    
    def __str__(self):
        return self.name

class AcademicDegree(models.Model):
    """Academic degrees and certifications"""
    DEGREE_TYPES = [
        ('phd', 'PhD'),
        ('masters', 'Masters'),
        ('bachelors', 'Bachelors'),
        ('hsc', 'Higher Secondary'),
        ('ssc', 'Secondary'),
        ('jsc', "Junior"),
        ('psc', 'Primary'),
    ]
    
    degree_type = models.CharField(max_length=20, choices=DEGREE_TYPES)
    degree_name = models.CharField(max_length=200)
    field_of_study = models.CharField(max_length=200)
    institution = models.ForeignKey(AcademicInstitution, on_delete=models.CASCADE, related_name='degrees')
    
    # Duration
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    is_current = models.BooleanField(default=False)
    
    # Grades
    grade_value = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)
    grade_scale = models.DecimalField(max_digits=4, decimal_places=2, default=4.00)
    grade_display = models.CharField(max_length=50, blank=True, help_text="e.g., '5.00 / 5.00'")
    
    # Rankings
    class_rank = models.IntegerField(null=True, blank=True)
    class_size = models.IntegerField(null=True, blank=True)
    rank_percentile = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    
    # Additional info
    description = models.TextField(blank=True)
    achievements = models.TextField(blank=True, help_text="Notable achievements during this degree")
    transcript_file = models.FileField(upload_to='transcripts/', blank=True, null=True)
    order = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['-start_date', 'order']
    
    def __str__(self):
        return f"{self.get_degree_type_display()} in {self.field_of_study} at {self.institution}"
    
    def get_class_percentage(self):
        """Calculate class rank percentage"""
        if self.class_rank and self.class_size:
            return (self.class_rank / self.class_size) * 100
        return None
    
    def get_grade_percentage(self):
        """Calculate grade as percentage"""
        if self.grade_value and self.grade_scale:
            return (self.grade_value / self.grade_scale) * 100
        return None

class Course(models.Model):
    """Courses taken during academic programs"""
    degree = models.ForeignKey(AcademicDegree, on_delete=models.CASCADE, related_name='courses')
    course_code = models.CharField(max_length=20, blank=True)
    course_name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    grade = models.CharField(max_length=10, blank=True)
    is_core = models.BooleanField(default=True)
    order = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['order']
    
    def __str__(self):
        return f"{self.course_code} - {self.course_name}"

class AcademicHonor(models.Model):
    """Honors, awards, and scholarships"""
    HONOR_TYPES = [
        ('award', 'Award'),
        ('scholarship', 'Scholarship'),
        ('honor', 'Honor'),
        ('prize', 'Prize'),
    ]
    
    title = models.CharField(max_length=200)
    honor_type = models.CharField(max_length=20, choices=HONOR_TYPES)
    institution = models.ForeignKey(AcademicInstitution, on_delete=models.CASCADE, null=True, blank=True)
    degree = models.ForeignKey(AcademicDegree, on_delete=models.CASCADE, related_name='honors', null=True, blank=True)
    date_received = models.DateField()
    description = models.TextField(blank=True)
    
    # Icon/color for display
    icon_class = models.CharField(max_length=50, default="fa-solid fa-medal")
    color_gradient = models.CharField(max_length=100, default="linear-gradient(145deg, #ffd700, #ffed4e)")
    text_color = models.CharField(max_length=20, default="#8B4513")
    order = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['-date_received', 'order']
    
    def __str__(self):
        return self.title

class AcademicTimelineEvent(models.Model):
    """Additional timeline events (conferences, workshops, etc.)"""
    EVENT_TYPES = [
        ('conference', 'Conference'),
        ('workshop', 'Workshop'),
        ('training', 'Training'),
        ('exchange', 'Exchange Program'),
        ('other', 'Other'),
    ]
    
    title = models.CharField(max_length=200)
    event_type = models.CharField(max_length=20, choices=EVENT_TYPES)
    institution = models.ForeignKey(AcademicInstitution, on_delete=models.CASCADE, null=True, blank=True)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    description = models.TextField(blank=True)
    certificate_file = models.FileField(upload_to='certificates/', blank=True, null=True)
    order = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['-start_date', 'order']
    
    def __str__(self):
        return self.title

class AcademicHighlight(models.Model):
    """Statistics highlights shown in cards"""
    label = models.CharField(max_length=100)
    value = models.CharField(max_length=50)
    description = models.CharField(max_length=200, blank=True)
    icon_class = models.CharField(max_length=50, default="fa-solid fa-star")
    order = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['order']
    
    def __str__(self):
        return self.label
    
class Project(models.Model):
    """Research projects"""
    PROJECT_STATUS = [
        ('completed', 'Completed'),
        ('ongoing', 'Ongoing'),
        ('proposed', 'Proposed'),
    ]
    
    title = models.CharField(max_length=300)
    slug = models.SlugField(max_length=300, unique=True, blank=True)
    subtitle = models.CharField(max_length=300, blank=True)
    
    # Dates
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    project_date = models.CharField(max_length=100, blank=True, help_text="Display date like 'March 2024'")
    
    # Description
    description = models.TextField()
    short_description = models.TextField(max_length=500, blank=True)
    
    # Technologies/Methods
    methods = models.CharField(max_length=500, blank=True, help_text="Comma-separated list of methods/tools")
    
    # Status
    status = models.CharField(max_length=20, choices=PROJECT_STATUS, default='completed')
    featured = models.BooleanField(default=False)
    
    # Media
    image = models.ImageField(upload_to='projects/', blank=True, null=True)
    pdf_file = models.FileField(upload_to='projects/pdfs/', blank=True, null=True)
    
    # Links
    doi = models.URLField(blank=True, help_text="DOI URL")
    github_url = models.URLField(blank=True)
    presentation_url = models.URLField(blank=True)
    
    # Ordering
    order = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['-project_date', '-end_date', 'order']
    
    def __str__(self):
        return self.title
    
    def get_methods_list(self):
        """Return methods as a list"""
        if self.methods:
            return [m.strip() for m in self.methods.split(',')]
        return []
    
    def save(self, *args, **kwargs):
        if not self.slug:
            from django.utils.text import slugify
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

class ProjectImage(models.Model):
    """Additional images for a project"""
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='additional_images')
    image = models.ImageField(upload_to='projects/additional/')
    caption = models.CharField(max_length=200, blank=True)
    order = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['order']
    
    def __str__(self):
        return f"{self.project.title} - Image {self.order}"

class ProjectCollaborator(models.Model):
    """Collaborators on a project"""
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='collaborators')
    name = models.CharField(max_length=200)
    institution = models.CharField(max_length=200, blank=True)
    role = models.CharField(max_length=200, blank=True)
    order = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['order']
    
    def __str__(self):
        return f"{self.name} - {self.project.title}"
    


class Affiliation(models.Model):
    """Professional affiliations and positions"""
    AFFILIATION_TYPES = [
        ('academic', 'Academic Position'),
        ('industrial', 'Industrial Training'),
        ('professional', 'Professional Membership'),
        ('visiting', 'Visiting Position'),
        ('other', 'Other'),
    ]
    
    title = models.CharField(max_length=200)
    organization = models.CharField(max_length=200)
    department = models.CharField(max_length=200, blank=True)
    affiliation_type = models.CharField(max_length=20, choices=AFFILIATION_TYPES)
    
    # Duration
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    is_current = models.BooleanField(default=False)
    display_date = models.CharField(max_length=100, blank=True, help_text="Custom date display like 'August 2024 - June 2025'")
    
    # Description
    description = models.TextField(blank=True)
    responsibilities = models.TextField(blank=True, help_text="Key responsibilities")
    
    # Media
    logo = models.ImageField(upload_to='affiliations/', blank=True, null=True)
    certificate_file = models.FileField(upload_to='certificates/', blank=True, null=True)
    
    # Links
    website_url = models.URLField(blank=True)
    
    # Ordering
    order = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['-start_date', 'order']
    
    def __str__(self):
        return f"{self.title} at {self.organization}"

class TaughtCourse(models.Model):
    """Courses taught (separate from academic courses)"""
    affiliation = models.ForeignKey(Affiliation, on_delete=models.CASCADE, related_name='courses_taught', null=True, blank=True)
    course_code = models.CharField(max_length=20)
    course_name = models.CharField(max_length=200)
    level = models.CharField(max_length=50, blank=True, help_text="e.g., Undergraduate, Graduate")
    semester = models.CharField(max_length=50, blank=True)
    description = models.TextField(blank=True)
    order = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['order']
        verbose_name = "Taught Course"
        verbose_name_plural = "Taught Courses"
    
    def __str__(self):
        return f"{self.course_code} - {self.course_name}"
    

class ProfessionalService(models.Model):
    """Professional services (reviewer, committee member, etc.)"""
    SERVICE_TYPES = [
        ('reviewer', 'Journal Reviewer'),
        ('committee', 'Committee Member'),
        ('board', 'Advisory Board'),
        ('organizer', 'Conference Organizer'),
        ('member', 'Professional Member'),
    ]
    
    title = models.CharField(max_length=200)
    organization = models.CharField(max_length=200)
    service_type = models.CharField(max_length=20, choices=SERVICE_TYPES)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    is_current = models.BooleanField(default=False)
    description = models.TextField(blank=True)
    order = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['-start_date', 'order']
    
    def __str__(self):
        return f"{self.title} - {self.organization}"
    

class MOOCProvider(models.Model):
    """MOOC platform providers (Coursera, edX, MathWorks, etc.)"""
    name = models.CharField(max_length=100)
    logo = models.ImageField(upload_to='mooc/logos/', blank=True, null=True)
    website = models.URLField(blank=True)
    description = models.TextField(blank=True)
    order = models.IntegerField(default=0)
    
    class Meta:
        verbose_name = "MOOC Provider"
        verbose_name_plural = "MOOC Providers"
        ordering = ['order', 'name']
    
    def __str__(self):
        return self.name

class MOOCCourse(models.Model):
    """Online courses and certifications"""
    DIFFICULTY_LEVELS = [
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
    ]
    
    title = models.CharField(max_length=200)
    provider = models.ForeignKey(MOOCProvider, on_delete=models.CASCADE, related_name='courses')
    instructor = models.CharField(max_length=200, blank=True, help_text="Course instructor(s)")
    
    # Course details
    description = models.TextField(blank=True)
    skills = models.CharField(max_length=500, blank=True, help_text="Comma-separated skills learned")
    difficulty = models.CharField(max_length=20, choices=DIFFICULTY_LEVELS, default='intermediate')
    
    # Completion info
    completion_date = models.DateField()
    completion_percentage = models.IntegerField(default=100, help_text="Percentage completed")
    credential_id = models.CharField(max_length=100, blank=True, help_text="Certificate ID")
    credential_url = models.URLField(blank=True, help_text="Link to verify credential")
    
    # Certificate file
    certificate_file = models.FileField(upload_to='mooc/certificates/', blank=True, null=True)
    
    # Course image/icon
    course_image = models.ImageField(upload_to='mooc/images/', blank=True, null=True)
    
    # Duration
    duration_hours = models.IntegerField(default=0, help_text="Estimated duration in hours")
    
    # Featured
    featured = models.BooleanField(default=False)
    order = models.IntegerField(default=0)
    
    class Meta:
        verbose_name = "MOOC Course"
        verbose_name_plural = "MOOC Courses"
        ordering = ['-completion_date', 'order']
    
    def __str__(self):
        return f"{self.title} ({self.provider.name})"
    
    def get_skills_list(self):
        """Return skills as a list"""
        if self.skills:
            return [s.strip() for s in self.skills.split(',')]
        return []

class MOOCCategory(models.Model):
    """Categories for courses (e.g., MATLAB, Python, Data Science)"""
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    order = models.IntegerField(default=0)
    
    class Meta:
        verbose_name = "MOOC Category"
        verbose_name_plural = "MOOC Categories"
        ordering = ['order', 'name']
    
    def __str__(self):
        return self.name

class MOOCCourseCategory(models.Model):
    """Many-to-many relationship between courses and categories"""
    course = models.ForeignKey(MOOCCourse, on_delete=models.CASCADE, related_name='course_categories')
    category = models.ForeignKey(MOOCCategory, on_delete=models.CASCADE, related_name='category_courses')
    
    class Meta:
        unique_together = ('course', 'category')
    
    def __str__(self):
        return f"{self.course.title} - {self.category.name}"\
        


from django.utils.text import slugify
from django.utils import timezone
from django.contrib.auth import get_user_model

User = get_user_model()

class BlogCategory(models.Model):
    """Categories for blog posts"""
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    color = models.CharField(max_length=20, default="#6dbfda", help_text="Hex color code for category")
    order = models.IntegerField(default=0)
    
    class Meta:
        verbose_name = "Blog Category"
        verbose_name_plural = "Blog Categories"
        ordering = ['order', 'name']
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

class BlogTag(models.Model):
    """Tags for blog posts"""
    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50, unique=True)
    
    class Meta:
        ordering = ['name']
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

class BlogPost(models.Model):
    """Academic blog posts"""
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('published', 'Published'),
        ('private', 'Private'),
    ]
    
    POST_TYPES = [
        ('article', 'Research Article'),
        ('tutorial', 'Tutorial'),
        ('note', 'Technical Note'),
        ('review', 'Literature Review'),
        ('opinion', 'Opinion Piece'),
        ('update', 'Project Update'),
    ]
    
    # Basic info
    title = models.CharField(max_length=300)
    slug = models.SlugField(max_length=300, unique=True)
    post_type = models.CharField(max_length=20, choices=POST_TYPES, default='article')
    
    # Author
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts')
    coauthors = models.CharField(max_length=500, blank=True, help_text="Comma-separated list of co-authors")
    
    # Content
    excerpt = models.TextField(max_length=500, blank=True, help_text="Short summary for preview")
    content = models.TextField()
    
    # Media
    featured_image = models.ImageField(upload_to='blog/images/', blank=True, null=True)
    banner_image = models.ImageField(upload_to='blog/banners/', blank=True, null=True)
    
    # Metadata
    categories = models.ManyToManyField(BlogCategory, related_name='posts', blank=True)
    tags = models.ManyToManyField(BlogTag, related_name='posts', blank=True)
    
    # Status and dates
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    published_date = models.DateTimeField(null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    
    # Academic metadata
    doi = models.CharField(max_length=100, blank=True, help_text="DOI if applicable")
    arxiv_id = models.CharField(max_length=100, blank=True, help_text="arXiv ID if applicable")
    citations = models.IntegerField(default=0, help_text="Number of citations")
    
    # Reading time
    reading_time_minutes = models.IntegerField(default=5)
    
    # Engagement
    views = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)
    
    # SEO
    meta_description = models.CharField(max_length=200, blank=True)
    keywords = models.CharField(max_length=500, blank=True, help_text="Comma-separated keywords")
    
    # Featured
    featured = models.BooleanField(default=False)
    pinned = models.BooleanField(default=False)
    order = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['-pinned', '-published_date', '-created_date']
        indexes = [
            models.Index(fields=['-published_date']),
            models.Index(fields=['status', 'published_date']),
        ]
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        if self.status == 'published' and not self.published_date:
            self.published_date = timezone.now()
        super().save(*args, **kwargs)
    
    def get_reading_time(self):
        """Calculate reading time based on word count"""
        word_count = len(self.content.split())
        minutes = max(1, round(word_count / 200))
        return minutes
    
    def get_coauthors_list(self):
        """Return coauthors as a list"""
        if self.coauthors:
            return [a.strip() for a in self.coauthors.split(',')]
        return []
    
    def get_keywords_list(self):
        """Return keywords as a list"""
        if self.keywords:
            return [k.strip() for k in self.keywords.split(',')]
        return []

class BlogComment(models.Model):
    """Comments on blog posts"""
    post = models.ForeignKey(BlogPost, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=100)
    email = models.EmailField()
    website = models.URLField(blank=True)
    content = models.TextField()
    
    # For threaded comments
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')
    
    # Status
    is_approved = models.BooleanField(default=False)
    is_spam = models.BooleanField(default=False)
    
    # Metadata
    created_date = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField(blank=True, null=True)
    
    class Meta:
        ordering = ['created_date']
    
    def __str__(self):
        return f"Comment by {self.name} on {self.post.title}"

class BlogSeries(models.Model):
    """Series of related blog posts"""
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    description = models.TextField()
    banner_image = models.ImageField(upload_to='blog/series/', blank=True, null=True)
    posts = models.ManyToManyField(BlogPost, related_name='series', blank=True)
    order = models.IntegerField(default=0)
    
    class Meta:
        verbose_name = "Blog Series"
        verbose_name_plural = "Blog Series"
        ordering = ['order', 'title']
    
    def __str__(self):
        return self.title

class BlogReference(models.Model):
    """Academic references for blog posts"""
    REFERENCE_TYPES = [
        ('article', 'Journal Article'),
        ('book', 'Book'),
        ('conference', 'Conference Paper'),
        ('thesis', 'Thesis'),
        ('web', 'Website'),
        ('other', 'Other'),
    ]
    
    post = models.ForeignKey(BlogPost, on_delete=models.CASCADE, related_name='references')
    citation_key = models.CharField(max_length=100, help_text="Unique key for citation")
    reference_type = models.CharField(max_length=20, choices=REFERENCE_TYPES, default='article')
    
    # Citation details
    authors = models.CharField(max_length=500)
    title = models.CharField(max_length=500)
    year = models.IntegerField()
    journal = models.CharField(max_length=300, blank=True)
    volume = models.CharField(max_length=50, blank=True)
    issue = models.CharField(max_length=50, blank=True)
    pages = models.CharField(max_length=50, blank=True)
    publisher = models.CharField(max_length=200, blank=True)
    doi = models.CharField(max_length=100, blank=True)
    url = models.URLField(blank=True)
    
    order = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['order']
    
    def __str__(self):
        return f"{self.authors} ({self.year}) - {self.title}"
    


class CVE(models.Model):
    """Common Vulnerabilities and Exposures (CVEs) discovered"""
    SEVERITY_CHOICES = [
        ('critical', 'Critical'),
        ('high', 'High'),
        ('medium', 'Medium'),
        ('low', 'Low'),
        ('none', 'None'),
    ]
    
    STATUS_CHOICES = [
        ('published', 'Published'),
        ('reserved', 'Reserved'),
        ('rejected', 'Rejected'),
        ('disputed', 'Disputed'),
    ]
    
    # CVE ID
    cve_id = models.CharField(max_length=20, unique=True, help_text="e.g., CVE-2024-12345")
    
    # Title and description
    title = models.CharField(max_length=300)
    description = models.TextField()
    
    # Severity and metrics
    severity = models.CharField(max_length=20, choices=SEVERITY_CHOICES, default='medium')
    cvss_score = models.DecimalField(max_digits=3, decimal_places=1, null=True, blank=True, help_text="CVSS v3 score")
    cvss_vector = models.CharField(max_length=100, blank=True, help_text="CVSS vector string")
    
    # Dates
    published_date = models.DateField()
    reserved_date = models.DateField(null=True, blank=True)
    updated_date = models.DateField(auto_now=True)
    
    # Status
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='published')
    
    # Affected products
    affected_products = models.TextField(help_text="Comma-separated list of affected products/versions")
    
    # Vulnerability type
    vulnerability_type = models.CharField(max_length=100, blank=True, help_text="e.g., Buffer Overflow, XSS, SQLi")
    
    # Links
    nvd_url = models.URLField(blank=True, help_text="NVD link")
    mitre_url = models.URLField(blank=True, help_text="MITRE link")
    github_advisory_url = models.URLField(blank=True)
    
    # Proof of Concept
    has_poc = models.BooleanField(default=False)
    poc_url = models.URLField(blank=True, help_text="Link to PoC code")
    poc_file = models.FileField(upload_to='cve/poc/', blank=True, null=True)
    
    # Credits
    credit_line = models.CharField(max_length=500, blank=True, help_text="How credit was given")
    
    # References
    references = models.TextField(blank=True, help_text="Additional references, one per line")
    
    # Featured
    featured = models.BooleanField(default=False)
    order = models.IntegerField(default=0)
    
    # Timeline
    discovery_date = models.DateField(null=True, blank=True)
    disclosure_date = models.DateField(null=True, blank=True)
    
    class Meta:
        verbose_name = "CVE"
        verbose_name_plural = "CVEs"
        ordering = ['-published_date', '-discovery_date', 'order']
        indexes = [
            models.Index(fields=['-published_date']),
            models.Index(fields=['severity']),
            models.Index(fields=['cve_id']),
        ]
    
    def __str__(self):
        return f"{self.cve_id} - {self.title}"
    
    def get_affected_products_list(self):
        """Return affected products as a list"""
        if self.affected_products:
            return [p.strip() for p in self.affected_products.split(',')]
        return []
    
    def get_references_list(self):
        """Return references as a list"""
        if self.references:
            return [r.strip() for r in self.references.split('\n') if r.strip()]
        return []
    
    def get_cvss_color(self):
        """Return color based on CVSS score"""
        if not self.cvss_score:
            return "var(--w-current)"
        score = float(self.cvss_score)
        if score >= 9.0:
            return "#d32f2f"  # Critical - Red
        elif score >= 7.0:
            return "#f57c00"  # High - Orange
        elif score >= 4.0:
            return "#fbc02d"  # Medium - Yellow
        else:
            return "#388e3c"  # Low - Green

class CVEAffectedVersion(models.Model):
    """Specific affected versions for a CVE"""
    cve = models.ForeignKey(CVE, on_delete=models.CASCADE, related_name='versions')
    product = models.CharField(max_length=200)
    version = models.CharField(max_length=100)
    version_type = models.CharField(max_length=50, blank=True, help_text="e.g., '=' , '<=', '>='")
    
    class Meta:
        ordering = ['product', 'version']
    
    def __str__(self):
        return f"{self.product} {self.version_type} {self.version}"

class CVEAcknowledgment(models.Model):
    """Acknowledgments or mentions"""
    cve = models.ForeignKey(CVE, on_delete=models.CASCADE, related_name='acknowledgments')
    name = models.CharField(max_length=200)
    organization = models.CharField(max_length=200, blank=True)
    url = models.URLField(blank=True)
    description = models.TextField(blank=True)
    
    class Meta:
        ordering = ['name']
    
    def __str__(self):
        return f"{self.name} - {self.cve.cve_id}"