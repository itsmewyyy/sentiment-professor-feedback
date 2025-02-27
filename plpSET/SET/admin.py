from django.contrib import admin
from SET.models import student_info,SubmissionSummary, year_level, EvaluationPeriod, student_status, academic_year, academic_yearsem, subjects, department, professor_status, professor_info, professor_subjs, student_enrolled_subjs, programs, categories, feedback_questions, feedbacks, numerical_questions, numerical_ratings, section

admin.site.register(student_info)
admin.site.register(programs)
admin.site.register(year_level)
admin.site.register(student_status)
admin.site.register(academic_year)
admin.site.register(academic_yearsem)
admin.site.register(subjects)
admin.site.register(department)
admin.site.register(professor_status)
admin.site.register(professor_info)
admin.site.register(professor_subjs)
admin.site.register(student_enrolled_subjs)
admin.site.register(categories)
admin.site.register(numerical_questions)
admin.site.register(numerical_ratings)
admin.site.register(feedback_questions)
admin.site.register(feedbacks)
admin.site.register(EvaluationPeriod)
admin.site.register(SubmissionSummary)


