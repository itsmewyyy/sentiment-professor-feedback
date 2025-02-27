from django.urls import path
from . import views
from .views import CategoriesAndQuestionsView, get_current_year_sem, incomplete_evaluations, ProfSubjs, SetAcademicTermView, EvaluationStatusView, AdminDetailView, EnrolledSubjsPost, ProfessorStatusView, YearLevelView, StudentListView, CollegeDetailView, SubjectDetailView, ProfessorDetailView, ProgramDetailView, SectionDetailView, NumericalCategoryDetailView, FeedbackQuestionsView, CollegeListView, SectionStudentsView, StudentStatusView, SubmitRatingsView, EnrolledSubjsView, AdminListView, ProfessorListView, DepartmentListView, ProgramListView, SectionListView, SubjectListView, NumericalCategoryView, NumericalQuestionsView, StudentDetailView, NumericalQuestionDetailView, FeedbackQuestionDetailView

urlpatterns = [
    path('categories-and-questions/', CategoriesAndQuestionsView.as_view(), name='categories-and-questions'),
    path('feedback-questions/', FeedbackQuestionsView.as_view(), name='feedback-questions'),
    path('colleges/', CollegeListView.as_view(), name='college-list'),
    path('section/<str:section_id>/', SectionStudentsView.as_view(), name='section-students'),
    path('submit-ratings/', SubmitRatingsView.as_view(), name='submit-ratings'),
    path('enrolled_subjs/<str:student_id>/', EnrolledSubjsView.as_view(), name='enrolled-subjects'),
    path('admin-list/', AdminListView.as_view(), name='admin-list'),
    path('professor-list/', ProfessorListView.as_view(), name='professor-list'),
    path('department-list/', DepartmentListView.as_view(), name='department-list'),
    path('program-list/', ProgramListView.as_view(), name='program-list'),
    path('years-list/', YearLevelView.as_view(), name='program-list'),
    path('section-list/', SectionListView.as_view(), name='section-list'),
    path('subject-list/', SubjectListView.as_view(), name='subject-list'),
    path('numerical-categories/', NumericalCategoryView.as_view(), name='category-list'),
    path('numerical-questions/', NumericalQuestionsView.as_view(), name='numerical-questions'),
    path('student-status/', StudentStatusView.as_view(), name='student-status'),
    path('professor-status/', ProfessorStatusView.as_view()),
    path('students/', StudentDetailView.as_view(), name='student-create'),
    path('students-list/', StudentListView.as_view()),
    path('students-list/<str:section>/', StudentListView.as_view()),
    path('students/<str:student_id>/', StudentDetailView.as_view(), name='student-detail'),
    path('categorycrud/', NumericalCategoryDetailView.as_view(), name='categorycrud'),
    path('categorycrud/<str:category_id>/', NumericalCategoryDetailView.as_view(), name='categorycrud-detail'),
    path('numerical-questioncrud/', NumericalQuestionDetailView.as_view(), name='numerical-questioncrud'),
    path('numerical-questioncrud/<str:numerical_question_id>/', NumericalQuestionDetailView.as_view(), name='numerical-questioncrud-detail'),
    path('feedback-questioncrud/', FeedbackQuestionDetailView.as_view(), name='feedback-questioncrud'),
    path('feedback-questioncrud/<str:feedback_question_id>/', FeedbackQuestionDetailView.as_view(), name='feedback-questioncrud-detail'),
    path('collegecrud/', CollegeDetailView.as_view()),
    path('collegecrud/<str:department_id>/', CollegeDetailView.as_view()),
    path('programcrud/', ProgramDetailView.as_view()),
    path('programcrud/<str:program_id>/', ProgramDetailView.as_view()),
    path('sectioncrud/', SectionDetailView.as_view()),
    path('sectioncrud/<str:section_id>/', SectionDetailView.as_view()),
    path('professorinfocrud/', ProfessorDetailView.as_view()),
    path('admininfocrud/<str:admin_acc_id>/', AdminDetailView.as_view()),
    path('admininfocrud/', AdminDetailView.as_view()),
    path('professorinfocrud/<str:professor_id>/', ProfessorDetailView.as_view()),
    path('subjectcrud/', SubjectDetailView.as_view()),
    path('subjectcrud/<str:subject_code>/', SubjectDetailView.as_view()),
    path('prof-subjs/', ProfSubjs.as_view()),
    path('enrolled-subjs/', EnrolledSubjsPost.as_view()),
    path('set-academic-term/', SetAcademicTermView.as_view(), name='set_academic_term'),
    path('evaluation-status/', EvaluationStatusView.as_view(), name='evaluation_status'),
    path('current-year-sem/', views.get_current_year_sem, name='current-year-sem'),
    path('student-profile/', views.get_student_profile, name='get_student_profile'),
    path('dean-profile/', views.get_dean_profile, name='get_dean_profile'),
    path('incomplete-evaluations/', views.incomplete_evaluations),
     path('latest-evaluation/', views.latest_evaluation_period, name='latest_evaluation_period'),

]