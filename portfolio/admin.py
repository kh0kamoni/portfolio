from django.contrib import admin
from .models import Profile, ResearchArea, Publication, Experience, Skill, Statistic, ContactMessage
from django.contrib import admin
from .models import (
    Profile, ResearchArea, Publication, Experience, Skill, 
    Statistic, ContactMessage, AcademicInstitution, AcademicDegree,
    Course, AcademicHonor, AcademicTimelineEvent, AcademicHighlight,
    Project, ProjectImage, ProjectCollaborator, MOOCProvider, MOOCCourse, MOOCCategory, MOOCCourseCategory,
    BlogCategory, BlogTag, BlogPost, BlogComment, BlogSeries, BlogReference



)

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['name', 'title', 'email']

@admin.register(ResearchArea)
class ResearchAreaAdmin(admin.ModelAdmin):
    list_display = ['title', 'order']
    list_editable = ['order']

@admin.register(Publication)
class PublicationAdmin(admin.ModelAdmin):
    list_display = ['title', 'year', 'publication_type', 'featured', 'order']
    list_filter = ['publication_type', 'year', 'featured']
    list_editable = ['featured', 'order']
    search_fields = ['title', 'authors']

@admin.register(Experience)
class ExperienceAdmin(admin.ModelAdmin):
    list_display = ['title', 'organization', 'experience_type', 'start_date', 'current']
    list_filter = ['experience_type', 'current']
    list_editable = ['current']

@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'proficiency', 'order']
    list_editable = ['proficiency', 'order']
    list_filter = ['category']

@admin.register(Statistic)
class StatisticAdmin(admin.ModelAdmin):
    list_display = ['label', 'value', 'order']
    list_editable = ['order']

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'subject', 'created_at', 'is_read']
    list_filter = ['is_read', 'created_at']
    readonly_fields = ['name', 'email', 'subject', 'message', 'created_at']




# ... existing admin classes ...

@admin.register(AcademicInstitution)
class AcademicInstitutionAdmin(admin.ModelAdmin):
    list_display = ['name', 'short_name', 'institution_type', 'location']
    list_filter = ['institution_type']
    search_fields = ['name', 'location']

@admin.register(AcademicDegree)
class AcademicDegreeAdmin(admin.ModelAdmin):
    list_display = ['degree_name', 'institution', 'degree_type', 'start_date', 'end_date', 'grade_value']
    list_filter = ['degree_type', 'institution', 'is_current']
    search_fields = ['degree_name', 'field_of_study']
    # Remove filter_horizontal since it's not a many-to-many field
    # If you want to show courses inline, use TabularInline instead

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['course_code', 'course_name', 'degree', 'is_core']
    list_filter = ['is_core', 'degree']
    search_fields = ['course_code', 'course_name']

@admin.register(AcademicHonor)
class AcademicHonorAdmin(admin.ModelAdmin):
    list_display = ['title', 'honor_type', 'institution', 'date_received']
    list_filter = ['honor_type', 'institution']
    search_fields = ['title', 'description']

@admin.register(AcademicTimelineEvent)
class AcademicTimelineEventAdmin(admin.ModelAdmin):
    list_display = ['title', 'event_type', 'institution', 'start_date']
    list_filter = ['event_type', 'institution']
    search_fields = ['title', 'description']

@admin.register(AcademicHighlight)
class AcademicHighlightAdmin(admin.ModelAdmin):
    list_display = ['label', 'value', 'order']
    list_editable = ['order']



class ProjectImageInline(admin.TabularInline):
    model = ProjectImage
    extra = 1
    fields = ['image', 'caption', 'order']

class ProjectCollaboratorInline(admin.TabularInline):
    model = ProjectCollaborator
    extra = 1
    fields = ['name', 'institution', 'role', 'order']

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['title', 'project_date', 'status', 'featured', 'order']
    list_filter = ['status', 'featured']
    list_editable = ['featured', 'order']
    search_fields = ['title', 'description']
    prepopulated_fields = {'slug': ('title',)}
    inlines = [ProjectImageInline, ProjectCollaboratorInline]
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'slug', 'subtitle', 'status', 'featured', 'order')
        }),
        ('Dates', {
            'fields': ('start_date', 'end_date', 'project_date')
        }),
        ('Description', {
            'fields': ('short_description', 'description', 'methods')
        }),
        ('Media & Links', {
            'fields': ('image', 'pdf_file', 'doi', 'github_url', 'presentation_url')
        }),
    )


from .models import Affiliation, TaughtCourse, ProfessionalService

class TaughtCourseInline(admin.TabularInline):
    model = TaughtCourse
    extra = 3
    fields = ['course_code', 'course_name', 'level', 'semester', 'order']

@admin.register(Affiliation)
class AffiliationAdmin(admin.ModelAdmin):
    list_display = ['title', 'organization', 'affiliation_type', 'start_date', 'end_date', 'is_current']
    list_filter = ['affiliation_type', 'is_current', 'organization']
    search_fields = ['title', 'organization', 'description']
    inlines = [TaughtCourseInline]  # Updated to TaughtCourseInline
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'organization', 'department', 'affiliation_type', 'order')
        }),
        ('Duration', {
            'fields': ('start_date', 'end_date', 'is_current', 'display_date')
        }),
        ('Details', {
            'fields': ('description', 'responsibilities')
        }),
        ('Media & Links', {
            'fields': ('logo', 'certificate_file', 'website_url')
        }),
    )

@admin.register(TaughtCourse)  # Updated to TaughtCourse
class TaughtCourseAdmin(admin.ModelAdmin):
    list_display = ['course_code', 'course_name', 'affiliation', 'level', 'semester']
    list_filter = ['level', 'affiliation']
    search_fields = ['course_code', 'course_name']

# Keep ProfessionalService as is
@admin.register(ProfessionalService)
class ProfessionalServiceAdmin(admin.ModelAdmin):
    list_display = ['title', 'organization', 'service_type', 'start_date', 'is_current']
    list_filter = ['service_type', 'is_current']
    search_fields = ['title', 'organization']


class MOOCCourseCategoryInline(admin.TabularInline):
    model = MOOCCourseCategory
    extra = 1

@admin.register(MOOCProvider)
class MOOCProviderAdmin(admin.ModelAdmin):
    list_display = ['name', 'order']
    list_editable = ['order']
    search_fields = ['name']

@admin.register(MOOCCourse)
class MOOCCourseAdmin(admin.ModelAdmin):
    list_display = ['title', 'provider', 'completion_date', 'difficulty', 'featured']
    list_filter = ['provider', 'difficulty', 'featured', 'completion_date']
    list_editable = ['featured']
    search_fields = ['title', 'description', 'skills']
    inlines = [MOOCCourseCategoryInline]
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'provider', 'instructor', 'difficulty', 'featured', 'order')
        }),
        ('Description', {
            'fields': ('description', 'skills')
        }),
        ('Completion Details', {
            'fields': ('completion_date', 'completion_percentage', 'duration_hours')
        }),
        ('Credentials', {
            'fields': ('credential_id', 'credential_url', 'certificate_file')
        }),
        ('Media', {
            'fields': ('course_image',)
        }),
    )

@admin.register(MOOCCategory)
class MOOCCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'order']
    list_editable = ['order']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name']



class BlogReferenceInline(admin.TabularInline):
    model = BlogReference
    extra = 1
    fields = ['citation_key', 'authors', 'title', 'year', 'doi']

@admin.register(BlogCategory)
class BlogCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'color', 'order']
    list_editable = ['order', 'color']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name']

@admin.register(BlogTag)
class BlogTagAdmin(admin.ModelAdmin):
    list_display = ['name']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name']

@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ['title', 'post_type', 'status', 'published_date', 'featured', 'pinned', 'views']
    list_filter = ['status', 'post_type', 'featured', 'pinned', 'categories']
    list_editable = ['featured', 'pinned']
    search_fields = ['title', 'content', 'excerpt']
    prepopulated_fields = {'slug': ('title',)}
    filter_horizontal = ['categories', 'tags']
    inlines = [BlogReferenceInline]
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'slug', 'post_type', 'author', 'coauthors', 'status')
        }),
        ('Content', {
            'fields': ('excerpt', 'content', 'featured_image', 'banner_image')
        }),
        ('Categorization', {
            'fields': ('categories', 'tags', 'keywords', 'meta_description')
        }),
        ('Academic Metadata', {
            'fields': ('doi', 'arxiv_id', 'citations')
        }),
        ('Dates & Metrics', {
            'fields': ('published_date', 'reading_time_minutes', 'views', 'likes')
        }),
        ('Featured', {
            'fields': ('featured', 'pinned', 'order')
        }),
    )

@admin.register(BlogComment)
class BlogCommentAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'post', 'created_date', 'is_approved']
    list_filter = ['is_approved', 'is_spam', 'created_date']
    search_fields = ['name', 'email', 'content']
    actions = ['approve_comments']
    
    def approve_comments(self, request, queryset):
        queryset.update(is_approved=True)
    approve_comments.short_description = "Approve selected comments"

@admin.register(BlogSeries)
class BlogSeriesAdmin(admin.ModelAdmin):
    list_display = ['title', 'order']
    list_editable = ['order']
    prepopulated_fields = {'slug': ('title',)}
    filter_horizontal = ['posts']


from .models import CVE, CVEAffectedVersion, CVEAcknowledgment

class CVEAffectedVersionInline(admin.TabularInline):
    model = CVEAffectedVersion
    extra = 1
    fields = ['product', 'version', 'version_type']

class CVEAcknowledgmentInline(admin.TabularInline):
    model = CVEAcknowledgment
    extra = 1
    fields = ['name', 'organization', 'url']

@admin.register(CVE)
class CVEAdmin(admin.ModelAdmin):
    list_display = ['cve_id', 'title', 'severity', 'cvss_score', 'published_date', 'status', 'featured']
    list_filter = ['severity', 'status', 'featured', 'published_date']
    list_editable = ['featured']
    search_fields = ['cve_id', 'title', 'description', 'affected_products']
    inlines = [CVEAffectedVersionInline, CVEAcknowledgmentInline]
    fieldsets = (
        ('CVE Information', {
            'fields': ('cve_id', 'title', 'description', 'status', 'featured', 'order')
        }),
        ('Severity Metrics', {
            'fields': ('severity', 'cvss_score', 'cvss_vector')
        }),
        ('Dates', {
            'fields': ('published_date', 'reserved_date', 'discovery_date', 'disclosure_date', 'updated_date')
        }),
        ('Affected Products', {
            'fields': ('affected_products', 'vulnerability_type')
        }),
        ('Links & References', {
            'fields': ('nvd_url', 'mitre_url', 'github_advisory_url', 'references')
        }),
        ('Proof of Concept', {
            'fields': ('has_poc', 'poc_url', 'poc_file')
        }),
        ('Credits', {
            'fields': ('credit_line',)
        }),
    )
    readonly_fields = ['updated_date']

@admin.register(CVEAffectedVersion)
class CVEAffectedVersionAdmin(admin.ModelAdmin):
    list_display = ['cve', 'product', 'version', 'version_type']
    list_filter = ['product']
    search_fields = ['product', 'version']

@admin.register(CVEAcknowledgment)
class CVEAcknowledgmentAdmin(admin.ModelAdmin):
    list_display = ['name', 'organization', 'cve']
    search_fields = ['name', 'organization']