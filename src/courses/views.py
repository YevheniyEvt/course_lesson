from django.shortcuts import render
from django.http import Http404, JsonResponse

from . import services

def cource_list_view(request):
    queryset = services.get_publish_courses()
    # return JsonResponse({'data': [el.path for el in queryset]})
    context = {
        "object_list": queryset
    }
    return render(request, "courses/list.html", context)


def cource_detail_view(request, course_id, *args, **kwargs):
    course_obj = services.get_course_detail(course_id=course_id)
    lessons_queryset = services.get_course_lessons(course_obj)
    context = {
        "object": course_obj,
        "lessons_queryset": lessons_queryset
    }
    # return JsonResponse({'id': course_obj.id, 'lessons': [el.path for el in lessons_queryset]})
    return render(request, "courses/detail.html", context)

def lesson_detail_view(request, course_id, lesson_id, *args, **kwargs):
    lesson_obj = services.get_lesson_detail(lesson_id=lesson_id, course_id=course_id)
    return JsonResponse({'data': lesson_obj.path})
    return render(request, "courses/lesson.html", {})