from rest_framework import serializers
from datetime import datetime
from .models import section, programs, year_level, department, student_info, numerical_ratings, feedbacks, student_enrolled_subjs, numerical_questions, feedback_questions, professor_subjs, professor_info, subjects, categories
from userLogin.models import admin_acc
from django.utils import timezone

class SectionSerializer(serializers.ModelSerializer):

    name = serializers.CharField(source='section')

    class Meta:
        model = section
        fields = ['section_id', 'name', 'program', 'year_level']


class ProgramSerializer(serializers.ModelSerializer):
    sections = SectionSerializer(many=True, read_only=True)

    class Meta: 
        model = programs
        fields = ['program_id', 'program_desc', 'sections', 'dept_id']

class ProgramsSerializer(serializers.ModelSerializer):

    class Meta: 
        model = programs
        fields = ['program_id', 'program_desc', 'dept_id']


class YearLevelSerializer(serializers.ModelSerializer):
    programs = serializers.SerializerMethodField()

    class Meta:
        model = year_level
        fields = ['year_level_id', 'year_level_desc', 'programs']

    def get_programs(self, obj):
        programs_list = programs.objects.filter(sections__year_level=obj).distinct()
        return ProgramSerializer(programs_list, many=True).data


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = department
        fields = ['department_id', 'department_desc']


class CollegeSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='dept_id.department_id')
    description = serializers.CharField(source='dept_id.department_desc')
    years = YearLevelSerializer(many=True, read_only=True)

    class Meta:
        model = programs
        fields = ['name', 'description', 'years']

class StudentSerializer(serializers.ModelSerializer):
    full_name = serializers.ReadOnlyField()

    class Meta:
        model = student_info
        # Include the editable fields
        fields = ['student_id', 'first_name', 'middle_name', 'surname', 'section', 'status', 'full_name']  

class SubmitRatingsSerializer(serializers.Serializer):
    numericalRatings = serializers.DictField(child=serializers.IntegerField())
    feedbackRatings = serializers.DictField(child=serializers.CharField())
    student_enrolled_subj_id = serializers.CharField()  # Add this field to identify the student-subject enrollment

    def create(self, validated_data):
        # Process and save numerical ratings
        for numerical_question_id, rating in validated_data['numericalRatings'].items():
            try:
                # Fetch the instance
                numerical_question_instance = numerical_questions.objects.get(numerical_question_id=numerical_question_id)
                student_enrolled_subj_instance = student_enrolled_subjs.objects.get(
                pk=validated_data['student_enrolled_subj_id']
            )

                # Create NumericalRatings instance
                numerical_ratings.objects.create(
                    numerical_id = f"{student_enrolled_subj_instance}_{numerical_question_instance}",
                    student_subj_id=student_enrolled_subj_instance, 
                    numerical_question_id=numerical_question_instance,  # Use the instance here
                    numerical_rating=rating,
                    numerical_rating_date=timezone.now() 
                )
            except numerical_questions.DoesNotExist:  # Fixed exception reference
                raise serializers.ValidationError(f"Numerical question with ID {numerical_question_id} does not exist.")

        # Process and save feedback ratings
        for question_id, feedback in validated_data['feedbackRatings'].items():
            try:

                #Fetch instance

                feedback_question_instance = feedback_questions.objects.get(feedback_question_id=question_id)
                student_enrolled_subj_instance = student_enrolled_subjs.objects.get(
                pk=validated_data['student_enrolled_subj_id']
            )

                feedbacks.objects.create(
                    feedback_id = f"{student_enrolled_subj_instance}_{feedback_question_instance}",
                    student_subj_id=student_enrolled_subj_instance, 
                    feedback_question_id=feedback_question_instance,
                    feedback_text=feedback,
                    feedback_date=timezone.now() 
                )
            except Exception as e:  
                raise serializers.ValidationError(f"Error creating feedback for question ID {question_id}: {str(e)}")

        # Update is_evaluated to True for the student enrolled in the subject
        try:
            student_enrolled_subj = student_enrolled_subjs.objects.get(
                pk=validated_data['student_enrolled_subj_id']
            )
            student_enrolled_subj.is_evaluated = True
            student_enrolled_subj.save()
        except student_enrolled_subjs.DoesNotExist:  
            raise serializers.ValidationError(f"Student enrolled subject with ID {validated_data['student_enrolled_subj_id']} does not exist.")

        return validated_data
    

# Serializer for Professor Info
class ProfessorInfoSerializer(serializers.ModelSerializer):
    department_desc = serializers.SerializerMethodField()

    full_name = serializers.ReadOnlyField()

    class Meta:
        model = professor_info
        fields = ['professor_id', 'surname', 'first_name','middle_name', 'full_name', 'department', 'department_desc',   'is_dean', 'status'] 

    # Method to get department description
    def get_department_desc(self, obj):
        return obj.department.department_desc if obj.department else None

# Serializer for Subject Info
class SubjectInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = subjects
        fields = ['subject_code', 'subject_desc', 'assoc_college' ]

# Serializer for Student Enrolled Subjects
class EnrolledSubjectsSerializer(serializers.ModelSerializer):
    prof_info = ProfessorInfoSerializer(source='prof_subj_id.professor_id', read_only=True)
    subj_name = SubjectInfoSerializer(source='prof_subj_id.subject_code', read_only=True)

    class Meta:
        model = student_enrolled_subjs
        fields = ['student_enrolled_subj_id', 'prof_info', 'subj_name', 'is_evaluated']

#Serizalier for Admin List
class AdminSerializer(serializers.ModelSerializer):

    class Meta:
        model = admin_acc
        # Include the editable fields
        fields = ['admin_acc_id', 'admin_username', 'is_mis', 'is_dean', 'is_secretary', 'dept_id']  


#Serizalier for Feedback Questions
class FeedbackQuestionsSerializer(serializers.ModelSerializer):

    class Meta:
        model = feedback_questions
        fields = ['feedback_question_id', 'question']  

#Serizalier for Category
class NumericalCategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = categories
        fields = ['category_id', 'category_desc']  

#Serizalier for Numerical Questions
class NumericalQuestionsSerializer(serializers.ModelSerializer):

    class Meta:
        model = numerical_questions
        fields = ['category', 'numerical_question_id', 'question']  
