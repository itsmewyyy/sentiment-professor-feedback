from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import student_acc, admin_acc
from .serializers import StudentAccSerializer
from .serializers import AdminAccSerializer
from django.contrib.auth.hashers import check_password
from datetime import datetime
from SET.models import student_info, SubmissionSummary
from django.contrib.auth import login, logout
from django.contrib.sessions.models import Session
from django.views.decorators.csrf import csrf_exempt

class RegisterView(APIView):
    def post(self, request):

        student_id = request.data.get('student_id')
        student_email = request.data.get('student_email')
        password = request.data.get('password')
        confirm_password = request.data.get('confirm_password')
        dateofbirth = request.data.get('dateofbirth')
        

        if password != confirm_password:
            return Response({'error': 'Passwords do not match'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            student = student_info.objects.get(student_id=student_id)
        except student_info.DoesNotExist:
            return Response({'error': 'Student ID does not exist'}, status=status.HTTP_400_BAD_REQUEST)


        if dateofbirth:
            try:
                dateofbirth_parsed = datetime.strptime(dateofbirth, '%Y-%m-%d').date()
            except ValueError:
                return Response({'error': 'Invalid date format. Use yyyy-mm-dd.'}, status=status.HTTP_400_BAD_REQUEST)

        else:
            return Response({'error': 'Date of birth is missing.'}, status=status.HTTP_400_BAD_REQUEST)

        
        student_acc_data = {
            'student_acc_number': student_id, 
            'password': password, 
            'date_of_birth': dateofbirth_parsed, 
            'plp_email': student_email}
        serializer = StudentAccSerializer(data=student_acc_data)

        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Student Account registration successful'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class LoginView(APIView):
    def post(self, request):
        student_acc_number = request.data.get('student_acc_number')
        password = request.data.get('password')
        dateofbirth = request.data.get('dateofbirth')

        # Fetch the student account based on student_acc_number
        try:
            student_account = student_acc.objects.get(student_acc_number=student_acc_number)
        except student_acc.DoesNotExist:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)

        # Check if the date of birth matches
        if student_account.date_of_birth.strftime('%Y-%m-%d') != dateofbirth:
            return Response({'error': 'Does not match student date of birth'}, status=status.HTTP_400_BAD_REQUEST)

        # Check if the password is correct
        if check_password(password, student_account.password):
            # Create session
            request.session['student_id'] = student_account.student_acc_number
            request.session['user_type'] = 'student'
            request.session.save() 
            print(request.session.items())
            
            return Response({
                'message': 'Login successful',
                'student_id': student_account.student_acc_number,
                'user_type': 'student',
            }, status=status.HTTP_200_OK)
           
        return Response({'error': 'Invalid password'}, status=status.HTTP_400_BAD_REQUEST)
        
class LogoutView(APIView):
    def post(self, request):
        if 'student_id' in request.session:
            request.session.flush()
            return Response({'message': 'Logout successful'}, status=status.HTTP_200_OK)
        return Response({'error': 'Not logged in'}, status=status.HTTP_400_BAD_REQUEST)

class LoginAdmin(APIView):
    def post(self, request):
        username = request.data.get('adminUsername')
        password = request.data.get('password')
        request.session.save() 
        print(request.session.items())

        try:
            # Fetch the admin account based on the provided username
            admin_account = admin_acc.objects.get(admin_username=username)
        except admin_acc.DoesNotExist:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)

        # Check if the password is correct
        if check_password(password, admin_account.password):
            # Create session for the admin
            request.session['admin_id'] = admin_account.admin_username
            
            if admin_account.is_dean:
                user_type = 'Dean'
            elif admin_account.is_secretary:
                user_type = 'Secretary'
            elif admin_account.is_mis:
                user_type = 'MIS'
            else:
                user_type = 'Admin' 

            return Response({
                'message': 'Login successful',
                'admin_id': admin_account.admin_username,
                'user_type': user_type,
                'dept_id': admin_account.dept_id.department_id if admin_account.dept_id else None,  # Ensure dept_id exists
                'is_dean': admin_account.is_dean,
                'is_secretary': admin_account.is_secretary,
                'is_mis': admin_account.is_mis,
            }, status=status.HTTP_200_OK)

        return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)

class LogoutAdmin(APIView):
    def post(self, request):
        if 'admin_id' in request.session:
            request.session.flush()
            return Response({'message': 'Logout successful'}, status=status.HTTP_200_OK)
        return Response({'error': 'Not logged in'}, status=status.HTTP_400_BAD_REQUEST)

class StudentsCount(APIView):
    def get(self, request):
   
        enrolled_students = student_info.objects.count()
        registered_accounts = student_acc.objects.count()
        submitted_evaluations = SubmissionSummary.objects.first().total_submissions if SubmissionSummary.objects.exists() else 0

        summary = {
            'enrolled_students': enrolled_students,
            'registered_accounts': registered_accounts,
            'submitted_evaluations': submitted_evaluations,
        }
    
        return Response(summary, status=status.HTTP_200_OK)