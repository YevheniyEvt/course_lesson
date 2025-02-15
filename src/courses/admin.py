import helpers
from django.contrib import admin
from django.utils.html import format_html

from .models import Course, Lesson


class LessonINline(admin.StackedInline):
    model = Lesson
    readonly_fields = ['updated', 'publick_id', 'display_image', 'display_video']
    extra = 0

    def display_image(self, obj):
        url = helpers.get_cloudinary_image_object(obj,
                                                  width=200,
                                                  field_name='thumbnail'
                                                  )
        return format_html(f"<img src={url} />")

    display_image.short_description = "Current Image"

    def display_video(self, obj):
        video_embed_html = helpers.get_cloudinary_video_object(obj,
                                                  width=550,
                                                  field_name='video',
                                                  as_html=True
                                                  )
        return video_embed_html

    display_video.short_description = "Current Video"

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    inlines = [LessonINline]
    list_display = ['title', 'status', 'acces']
    list_filter = ['status', 'acces']
    fields = ['publick_id','title', 'description', 'status', 'image', 'acces', 'display_image']
    readonly_fields = ['display_image', 'publick_id']

    def display_image(self, obj):
        url = helpers.get_cloudinary_image_object(obj,
                                                  width=200,
                                                  field_name='image'
                                                  )
        # cloudinary_id = str(obj.image)
        # cloudinary_html2 = obj.image.image(width = 200)
        # cloudinary_html = CloudinaryImage(cloudinary_id).image(width=100)
        return format_html(f"<img src={url} />")

    display_image.short_description = "Current Image"

    
# admin.site.register(Course)