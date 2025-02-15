import helpers
import uuid
from django.db import models
from cloudinary.models import CloudinaryField
from django.utils.text import slugify


helpers.cloudinary_init()

class AccesRequirement(models.TextChoices):
    ANYONE = 'any', 'Anyone'
    EMAIL_REQUIREMENT = 'email', "Email requirement"



class PublishStatus(models.TextChoices):
    PUBLISHED = 'pub', 'Published'
    COMING_SOON = 'soon', "Coming soon"
    DRAFT = 'draft', 'Draft'

def handle_upload(instance, filename):
    return f"{filename}"

def generate_publick_id(instance, *args, **kwargs):
    title = instance.title
    unique_id = str(uuid.uuid4()).replace('-', '')
    if not title:
        return unique_id
    slug = slugify(title)
    unique_id_short = unique_id[:5]
    return f"{slug}-{unique_id_short}"


def get_publick_id_prefix(instance, *args, **kwargs):
    if hasattr(instance, 'path'):
        path: str = instance.path
        if path.startswith("/"):
            path = path[1:]
        if path.endswith("/"):
            path = path[:-1]
        return path
    publick_id = instance.publick_id
    model_class = instance.__class__
    model_name = model_class.__name__
    model_name_slug = slugify(model_name)
    if not publick_id:
        return f"{model_name_slug}"
    return f"{model_name_slug}/{publick_id}"


def get_display_name(instance, *args, **kwargs):
    if hasattr(instance, 'get_display_name'):
        return instance.get_display_name()
    elif hasattr(instance, 'title'):
        return instance.title
    model_class = instance.__class__
    model_name = model_class.__name__
    return f'{model_name} Upload'


class Course(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField(blank=True, null=True)
    publick_id = models.CharField(max_length=130, blank=True, null=True, db_index=True) #slug
    # image = models.ImageField(upload_to=handle_upload, blank=True, null=True)
    image = CloudinaryField(
        "image",
        null=True,
        public_id_prefix=get_publick_id_prefix,
        display_name=get_display_name,
        tags=['course', 'thumbnail']
        )
    acces = models.CharField(
        max_length=5,
        choices=AccesRequirement.choices,
        default=AccesRequirement.EMAIL_REQUIREMENT,
        )
    status = models.CharField(
        max_length=10,
        choices=PublishStatus.choices,
        default=PublishStatus.DRAFT,
        )
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.title}(№:{self.id})'
    

    def save(self, *args, **kwargs):
        if self.publick_id == "" or self.publick_id is None:
            self.publick_id = generate_publick_id(self)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return self.path

    @property
    def path(self):
        return f"/courses/{self.publick_id}"

    def get_display_name(self):
        return f"{self.title} - Course"
    

    @property
    def is_published(self):
        return self.status == PublishStatus.PUBLISHED
    
    
    def image_admin_thumbnail(self, as_html=False, width=500):
        return helpers.get_cloudinary_image_object(self,
                                            field_name='image',
                                            as_html=as_html,
                                            width=width)
    
    def get_image_detail(self, as_html=False, width=750):
        return helpers.get_cloudinary_image_object(self,
                                            field_name='image',
                                            as_html=as_html,
                                            width=width)
    

class Lesson(models.Model):
    course  = models.ForeignKey(Course, on_delete=models.CASCADE)
    publick_id = models.CharField(max_length=130, blank=True, null=True, db_index=True) #slug
    title = models.CharField(max_length=50)
    description = models.TextField(blank=True, null=True)
    thumbnail = CloudinaryField(
        "image",
        blank=True,
        null=True,
        public_id_prefix=get_publick_id_prefix,
        display_name=get_display_name,
        tags=['image', 'thumbnail', 'lesson'],
        )
    video = CloudinaryField(
        "video",
        blank=True,
        null=True,
        type='private',
        resource_type='video',
        public_id_prefix=get_publick_id_prefix,
        display_name=get_display_name,
        tags=['video', 'lesson'],
        )
    order = models.IntegerField(default=0)
    can_preview = models.BooleanField(default=False,
                                       help_text='If user does not have access to course, can they see this?')
    status = models.CharField(
        max_length=10,
        choices=PublishStatus.choices,
        default=PublishStatus.PUBLISHED,
        )
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['order', '-updated']


    def save(self, *args, **kwargs):
        if self.publick_id == "" or self.publick_id is None:
            self.publick_id = generate_publick_id(self)
        super().save(*args, **kwargs)

    @property
    def path(self):
        course_path = self.course.path
        if course_path.endswith('/'):
            course_path = course_path[:-1]
        return f"{course_path}/lesson/{self.publick_id}"

    def get_display_name(self):
        return f"{self.title} - {self.course.get_display_name()}"
    
    def get_absolute_url(self):
        return self.path
    
    def is_coming_soon(self):
        return self.status == PublishStatus.COMING_SOON