from celery import shared_task
from django.utils import timezone
from .models import feedbacks, feedback_questions
from reportsAnalysis.models import processed_feedbacks, filtered_feedbacks
from django.db.models import Avg, Sum, Count
from .models import (
    numerical_ratings,
    feedbacks,
)
from reportsAnalysis.models import ( college_numerical_total, college_numerical_summary, college_feedback_total, college_feedback_summary, professor_numerical_total,
    professor_numerical_summary_category,
    professor_feedback_total,
    professor_feedback_summary, professor_numerical_summary_questions)
from joblib import load
from datetime import timedelta
from django.db import transaction

import os
import re
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from django.conf import settings

import logging
logger = logging.getLogger(__name__)

# Load the model and vectorizer globally to avoid reloading them in every task
MODEL_PATH = os.path.join(settings.BASE_DIR, 'reportsAnalysis', 'model.pkl')
VECTORIZER_PATH = os.path.join(settings.BASE_DIR, 'reportsAnalysis', 'vectorizer.pkl')

model = load(MODEL_PATH)
vectorizer = load(VECTORIZER_PATH)

# Load stopwords
stop_words = set(stopwords.words('english')) | set(["akin","aking","ako","alin","am","amin","aming","ang","ano","anumang","apat","at","atin","ating","ay", "bakit", ...]) 
lemmatizer = WordNetLemmatizer()

def preprocess_text(text):
    lowercase_text = text.lower()
    cleaned_text = re.sub(r"[^a-zA-Z0-9\s]", "", lowercase_text)
    tokens = word_tokenize(cleaned_text)
    tokens = [token for token in tokens if token not in stop_words]
    tokens = [lemmatizer.lemmatize(token) for token in tokens]
    return ' '.join(tokens)

@shared_task
def process_feedback_task(feedback_data):
    processed_feedback_instances = []
    filtered_feedback_instances = []

    for question_id, feedback in feedback_data['feedbackRatings'].items():
        processed_text = preprocess_text(feedback)

        try:
            feedback_question_instance = feedback_questions.objects.get(feedback_question_id=question_id)
            feedback_instance = feedbacks.objects.get(
                student_subj_id=feedback_data['student_enrolled_subj_id'],
                feedback_question_id=feedback_question_instance
            )

            # Store preprocessed feedback
            processed_feedback_instance = processed_feedbacks(
                feedback_id=feedback_instance,
                processed_text=processed_text,
                processed_date=timezone.now()
            )
            processed_feedback_instances.append(processed_feedback_instance)

            # Perform sentiment analysis on processed feedbacks
            features = vectorizer.transform([processed_text])
            sentiment = model.predict(features)[0]
            sentiment_label = "positive" if sentiment == 1 else "neutral" if sentiment == 0 else "negative"

            filtered_feedback_instance = filtered_feedbacks(
                feedback_id=feedback_instance,
                sentiment_rating=sentiment,
                sentiment_label=sentiment_label,
                analysis_date=timezone.now()
            )
            filtered_feedback_instances.append(filtered_feedback_instance)

        except feedback_questions.DoesNotExist:
            return f"Feedback question with ID {question_id} does not exist"

    # Save results
    processed_feedbacks.objects.bulk_create(processed_feedback_instances)
    filtered_feedbacks.objects.bulk_create(filtered_feedback_instances)

    return "Feedback processed successfully"


@shared_task
def update_summaries_batch():
    last_update_time = timezone.now() - timedelta(minutes=30)
    
    recent_filtered_feedbacks = filtered_feedbacks.objects.filter(analysis_date__gte=last_update_time)
    recent_ratings = numerical_ratings.objects.filter(numerical_rating_date__gte=last_update_time)
    
    # Update micro (professor) level summaries
    update_professor_feedback_summaries(recent_filtered_feedbacks)
    update_professor_numerical_summaries(recent_ratings)

    # Update macro (college) level summaries
    update_college_feedback_summaries(recent_filtered_feedbacks)
    update_college_numerical_summaries(recent_ratings)
    
    for filtered_feedback in recent_filtered_feedbacks:
        filtered_feedback.processed = True
        filtered_feedback.save()
  
    
    return "Summaries updated successfully"


### College-level Summaries ###
def update_college_feedback_summaries(recent_filtered_feedbacks):
    with transaction.atomic():
        for filtered_feedback in recent_filtered_feedbacks:
            if filtered_feedback.processed:
                continue  

            raw_feedback = filtered_feedback.feedback_id
            department = raw_feedback.student_subj_id.prof_subj_id.subject_code.assoc_college
            year_sem = raw_feedback.student_subj_id.prof_subj_id.year_sem_id
            
            # Fetch or create college feedback summary for the department and question
            college_feedback, _ = college_feedback_summary.objects.get_or_create(
                college_feedback_summary_id=f"{department}-{year_sem}-{raw_feedback.feedback_question_id}",
                defaults={'total_feedbacks': 0, 'total_positive': 0, 'total_negative': 0, 'total_neutral': 0},
                department=department,
                year_sem_id=year_sem,
                feedback_question_id=raw_feedback.feedback_question_id,
            )

            # Increment feedback counts 
            college_feedback.total_feedbacks += 1
            if filtered_feedback.sentiment_label == 'positive':
                college_feedback.total_positive += 1
            elif filtered_feedback.sentiment_label == 'negative':
                college_feedback.total_negative += 1
            else:
                college_feedback.total_neutral += 1

            college_feedback.save()

        # Calculate total number of feedbacks across all questions for the department
        for department in set(fb.feedback_id.student_subj_id.prof_subj_id.subject_code.assoc_college for fb in recent_filtered_feedbacks):
            year_sem = recent_filtered_feedbacks[0].feedback_id.student_subj_id.prof_subj_id.year_sem_id

            department_feedback_total, _ = college_feedback_total.objects.get_or_create(
                college_total_summary_id=f"{department}-{year_sem}-total",
                defaults={'total_feedbacks': 0, 'total_positive': 0, 'total_negative': 0, 'total_neutral': 0},
                department=department,
                year_sem_id=year_sem,
            )

            total_feedbacks_college = college_feedback_summary.objects.filter(
                department=department,
                year_sem_id=year_sem,
            ).aggregate(
                total_feedbacks=Sum('total_feedbacks'),
                total_positive=Sum('total_positive'),
                total_negative=Sum('total_negative'),
                total_neutral=Sum('total_neutral')
            )

            # Update the overall totals
            department_feedback_total.total_feedbacks = total_feedbacks_college['total_feedbacks'] or 0
            department_feedback_total.total_positive = total_feedbacks_college['total_positive'] or 0
            department_feedback_total.total_negative = total_feedbacks_college['total_negative'] or 0
            department_feedback_total.total_neutral = total_feedbacks_college['total_neutral'] or 0
            department_feedback_total.save()


def update_college_numerical_summaries(recent_ratings):
    for rating in recent_ratings:
        department = rating.student_subj_id.prof_subj_id.subject_code.assoc_college
        year_sem = rating.student_subj_id.prof_subj_id.year_sem_id
        category = rating.numerical_question_id.category

        # Fetch or create college numerical summary for the department and category
        college_numerical_summary_category, _ = college_numerical_summary.objects.get_or_create(
            college_numerical_summary_id=f"{department}-{year_sem}-{category}",
            defaults={'college_average': 0},
            department=department,
            year_sem_id=year_sem,
            category=category,
        )

        total_ratings_category = numerical_ratings.objects.filter(
            student_subj_id__prof_subj_id__subject_code__assoc_college=department,
            student_subj_id__prof_subj_id__year_sem_id=year_sem,
            numerical_question_id__category=category
        ).count()

        total_sum_category = numerical_ratings.objects.filter(
            student_subj_id__prof_subj_id__subject_code__assoc_college=department,
            student_subj_id__prof_subj_id__year_sem_id=year_sem,
            numerical_question_id__category=category
        ).aggregate(total_sum=Sum('numerical_rating'))['total_sum']

        college_numerical_summary_category.college_average = (
            total_sum_category / total_ratings_category
        ) if total_ratings_category > 0 else 0
        college_numerical_summary_category.save()

        # Update total numerical summary for the college
        college_numerical_totals, _ = college_numerical_total.objects.get_or_create(
            college_numerical_total_id=f"{department}-{year_sem}-total_avg",
            defaults={'total_average': 0},
            department=department,
            year_sem_id=year_sem,
        )

        total_ratings_total = numerical_ratings.objects.filter(
            student_subj_id__prof_subj_id__subject_code__assoc_college=department,
            student_subj_id__prof_subj_id__year_sem_id=year_sem
        ).count()

        total_sum_total = numerical_ratings.objects.filter(
            student_subj_id__prof_subj_id__subject_code__assoc_college=department,
            student_subj_id__prof_subj_id__year_sem_id=year_sem
        ).aggregate(total_sum=Sum('numerical_rating'))['total_sum']

        college_numerical_totals.total_average = (
            total_sum_total / total_ratings_total
        ) if total_ratings_total > 0 else 0
        college_numerical_totals.save()


### Professor-level Summaries ###
def update_professor_feedback_summaries(recent_filtered_feedbacks):
    with transaction.atomic():
        for filtered_feedback in recent_filtered_feedbacks:

            if filtered_feedback.processed:
                continue  

            raw_feedback = filtered_feedback.feedback_id
            professor = raw_feedback.student_subj_id.prof_subj_id.professor_id
            year_sem = raw_feedback.student_subj_id.prof_subj_id.year_sem_id
            feedback_question = raw_feedback.feedback_question_id

            # Fetch or create professor feedback summary for each question
            professor_feedback_summary_question, _ = professor_feedback_summary.objects.get_or_create(
                professor_feedback_summary_id=f"{year_sem}-{professor}-{feedback_question}",
                defaults={'total_feedbacks': 0, 'total_positive': 0, 'total_negative': 0, 'total_neutral': 0},
                prof_id=professor,
                year_sem_id=year_sem,
                feedback_question_id=feedback_question,
            )

            # Update feedback counts based on sentiment
            professor_feedback_summary_question.total_feedbacks += 1
            if filtered_feedback.sentiment_label == 'positive':
                professor_feedback_summary_question.total_positive += 1
            elif filtered_feedback.sentiment_label == 'negative':
                professor_feedback_summary_question.total_negative += 1
            else:
                professor_feedback_summary_question.total_neutral += 1

            professor_feedback_summary_question.save()

        # Update total feedback summary for the professor
        for professor in set(fb.feedback_id.student_subj_id.prof_subj_id.professor_id for fb in recent_filtered_feedbacks):
            year_sem = recent_filtered_feedbacks[0].feedback_id.student_subj_id.prof_subj_id.year_sem_id

            professor_feedback_totals, _ = professor_feedback_total.objects.get_or_create(
                professor_feedback_total_id=f"{year_sem}-{professor}-total",
                defaults={'total_feedbacks': 0, 'total_positive': 0, 'total_negative': 0, 'total_neutral': 0},
                prof_id=professor,
                year_sem_id=year_sem,
            )

            
            total_feedbacks = professor_feedback_summary.objects.filter(
                prof_id=professor,
                year_sem_id=year_sem,
            ).aggregate(
                total_feedbacks=Sum('total_feedbacks'),
                total_positive=Sum('total_positive'),
                total_negative=Sum('total_negative'),
                total_neutral=Sum('total_neutral')
            )

            professor_feedback_totals.total_feedbacks = total_feedbacks['total_feedbacks'] or 0
            professor_feedback_totals.total_positive = total_feedbacks['total_positive'] or 0
            professor_feedback_totals.total_negative = total_feedbacks['total_negative'] or 0
            professor_feedback_totals.total_neutral = total_feedbacks['total_neutral'] or 0
            professor_feedback_totals.save()

def update_professor_numerical_summaries(recent_ratings):
    for rating in recent_ratings:
        professor = rating.student_subj_id.prof_subj_id.professor_id
        year_sem = rating.student_subj_id.prof_subj_id.year_sem_id
        category = rating.numerical_question_id.category

        # Fetch or create professor numerical summary for each question
        professor_numerical_summary_question, _ = professor_numerical_summary_questions.objects.get_or_create(
            professor_numerical_summary_question_id=f"{year_sem}-{professor}-{rating.numerical_question_id}",
            defaults={'question_average': 0},
            prof_id=professor,
            year_sem_id=year_sem,
            numerical_question_id=rating.numerical_question_id,
        )

        total_ratings_question = numerical_ratings.objects.filter(
            student_subj_id__prof_subj_id__professor_id=professor,
            student_subj_id__prof_subj_id__year_sem_id=year_sem,
            numerical_question_id=rating.numerical_question_id
        ).count()

        total_ratings_sum = numerical_ratings.objects.filter(
            student_subj_id__prof_subj_id__professor_id=professor,
            student_subj_id__prof_subj_id__year_sem_id=year_sem,
            numerical_question_id=rating.numerical_question_id
        ).aggregate(total_sum=Sum('numerical_rating'))['total_sum']

        professor_numerical_summary_question.question_average = (
            total_ratings_sum / total_ratings_question
        ) if total_ratings_question > 0 else 0
        professor_numerical_summary_question.save()

        # Update total numerical summary by category
        professor_numerical_summary_categories, _ = professor_numerical_summary_category.objects.get_or_create(
            professor_numerical_summary_category_id=f"{year_sem}-{professor}-{category}",
            defaults={'category_average': 0},
            prof_id=professor,
            year_sem_id=year_sem,
            category=category,
        )

        total_ratings_category = numerical_ratings.objects.filter(
            student_subj_id__prof_subj_id__professor_id=professor,
            student_subj_id__prof_subj_id__year_sem_id=year_sem,
            numerical_question_id__category=category
        ).count()

        total_ratings_sum = numerical_ratings.objects.filter(
            student_subj_id__prof_subj_id__professor_id=professor,
            student_subj_id__prof_subj_id__year_sem_id=year_sem,
            numerical_question_id__category=category
        ).aggregate(total_sum=Sum('numerical_rating'))['total_sum']

        professor_numerical_summary_categories.category_average = (
            total_ratings_sum / total_ratings_category
        ) if total_ratings_category > 0 else 0
        professor_numerical_summary_categories.save()

        # Update total numerical summary for the professor
        professor_numerical_totals, _ = professor_numerical_total.objects.get_or_create(
            professor_numerical_total_id=f"{year_sem}-{professor}-total_avg",
            defaults={'total_average': 0},
            prof_id=professor,
            year_sem_id=year_sem,
        )

        total_ratings_total = numerical_ratings.objects.filter(
            student_subj_id__prof_subj_id__professor_id=professor,
            student_subj_id__prof_subj_id__year_sem_id=year_sem
        ).count()

        total_sum = numerical_ratings.objects.filter(
            student_subj_id__prof_subj_id__professor_id=professor,
            student_subj_id__prof_subj_id__year_sem_id=year_sem
        ).aggregate(total_sum=Sum('numerical_rating'))['total_sum']

        professor_numerical_totals.total_average = (
            total_sum / total_ratings_total
        ) if total_ratings_total > 0 else 0
        professor_numerical_totals.save()