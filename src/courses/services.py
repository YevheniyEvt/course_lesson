from django.shortcuts import get_object_or_404
from django.http import Http404, JsonResponse

from .models import Course, PublishStatus, Lesson

def get_publish_courses():
    return Course.objects.filter(status=PublishStatus.PUBLISHED)

def get_course_detail(course_id):
    course = get_object_or_404(Course,
                            publick_id=course_id,
                            status = PublishStatus.PUBLISHED)
    return course

    
def get_course_lessons(course_obj):
    lessons = Lesson.objects.none()
    if not isinstance(course_obj, Course):
        return lessons
    lessons = course_obj.lesson_set.filter(status__in=[PublishStatus.PUBLISHED, PublishStatus.COMING_SOON])
    return lessons

def get_lesson_detail(lesson_id, course_id):
    lesson = get_object_or_404(Lesson,
                            publick_id=lesson_id,
                            status__in = [PublishStatus.PUBLISHED, PublishStatus.COMING_SOON],
                            course__status = PublishStatus.PUBLISHED,
                            course__publick_id = course_id
                            )
    return lesson
