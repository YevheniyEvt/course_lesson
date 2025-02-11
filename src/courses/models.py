import helpers
from django.db import models
from cloudinary.models import CloudinaryField

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

class Course(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField(blank=True, null=True)
    # image = models.ImageField(upload_to=handle_upload, blank=True, null=True)
    image = CloudinaryField("image", null=True)
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

    @property
    def is_published(self):
        return self.status == PublishStatus.PUBLISHED