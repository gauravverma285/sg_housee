from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated, AllowAny
from datetime import date
from rest_framework import status
from .serializers import *
from .models import User
# from account.renderers import UserRenderer
from universal.mailing import (
	resetPassMail,
)
from universal.methods import (
	otp_func,
)






from .models import *
# from .serializers import *

class SignupApiView(APIView):
	""" API for signup """

	permission_classes = [AllowAny]

	def post(self, request):
		""" post method for signup api """
		res = {}
		try:
			email = request.data.get("email", None)
			password = request.data.get("password", None)
			cpassword = request.data.get("cpassword", None)
			name = request.data.get('name', None)

			if email is None:
				res['status'] = False
				res['message'] = "Email is Required"
				res['data'] = []
				return Response(res, status=status.HTTP_404_NOT_FOUND)

			if User.objects.filter(email=email).exists() or User.objects.filter(username=email).exists():
				res['status'] = False
				res['message'] = "Account already exist with this Email"
				res['data'] = []
				return Response(res, status=status.HTTP_404_NOT_FOUND)

			if name is None:
				res['status'] = False
				res['message'] = "Name is Required"
				res['data'] = []
				return Response(res, status=status.HTTP_404_NOT_FOUND)

			if password is None or password != cpassword:
				res['status'] = False
				res['message'] = "Password not Match!"
				res['data'] = []
				return Response(res, status=status.HTTP_400_BAD_REQUEST)

			data = request.data
			try:
				data._mutable = True
			except:
				pass
			data['username'] = email
			
			
			serializer = UserSerializer(
				data=data, context={'request': request})
			if serializer.is_valid(raise_exception=True):
				serializer.save()
				res_data = serializer.data
				user = User.objects.filter(id=res_data['id']).last()
				user.set_password(password)
				user.save()

				res['status'] = True
				res['message'] = "You've registered successfully"
				res['data'] = res_data
				return Response(res, status=status.HTTP_200_OK)
			else:
				res['status'] = False
				error = next(iter(serializer.errors))
				res['message'] = serializer.errors[str(error)][0]
				res['data'] = res_data
				return Response(res, status=status.HTTP_200_OK)

		except Exception as e:
			res['status'] = False
			res['message'] = str(e)
			res['data'] = []
			return Response(res, status=status.HTTP_400_BAD_REQUEST)
		
class LoginApiView(APIView):
	""" API for login """

	permission_classes = [AllowAny]

	def post(self, request):
		""" post method for login api """
		res = {}
		username = request.data.get("username", None)
		password = request.data.get("password", None)

		if username is None:
			res['status'] = False
			res['message'] = "Email is required"
			res['data'] = []
			return Response(res, status=status.HTTP_400_BAD_REQUEST)

		if password is None:
			res['status'] = False
			res['message'] = "Password is required"
			res['data'] = []
			return Response(res, status=status.HTTP_400_BAD_REQUEST)

		user = authenticate(username=username, password=password)
		if user is None:
			res['status'] = False
			res['message'] = "Invalid Email or Password!"
			res['data'] = []
			return Response(res, status=status.HTTP_400_BAD_REQUEST)
		serializer = UserSerializer(
			user, read_only=True, context={'request': request})
		if serializer:
			res['status'] = True
			res['message'] = "Authenticated successfully"
			res['data'] = serializer.data
			return Response(res, status=status.HTTP_200_OK)

		else:
			res['status'] = False
			res['message'] = "No recored found for entered data"
			res['data'] = []
			return Response(res, status=status.HTTP_400_BAD_REQUEST)
		
class ResetPasswordApiView(APIView):
	""" API for reset password """

	permission_classes = [IsAuthenticated]
	# permission_classes = [AllowAny]

	def post(self, request):
		
		""" post method for reset password API """
		res = {}
		try:
			old_password = request.data.get('old_password', None)
			new_password = request.data.get('new_password', None)
			re_password = request.data.get('re_password', None)
			user = User.objects.filter(id=request.user.id).last()

			if user is None:
				res['status'] = False
				res['message'] = 'No such Authenticated User.'
				res['data'] = []
				return Response(res,  status=status.HTTP_404_NOT_FOUND)

			if old_password is None:
				res['status'] = False
				res['message'] = 'Old password is required'
				res['data'] = []
				return Response(res,  status=status.HTTP_404_NOT_FOUND)

			if not user.check_password(old_password):
				res['status'] = False
				res['message'] = 'Password not Match!'
				res['data'] = []
				return Response(res,  status=status.HTTP_404_NOT_FOUND)

			if new_password is None:
				res['status'] = False
				res['message'] = 'New password is required'
				res['data'] = []
				return Response(res,  status=status.HTTP_404_NOT_FOUND)

			if re_password is None:
				res['status'] = False
				res['message'] = 'Confirm password is required'
				res['data'] = []
				return Response(res,  status=status.HTTP_404_NOT_FOUND)

			if str(new_password) != str(re_password):
				res['status'] = False
				res['message'] = 'New password and confirm password not match.'
				res['data'] = []
				return Response(res,  status=status.HTTP_404_NOT_FOUND)

			else:
				user.set_password(new_password)
				user.save()
				try:
					user.auth_token.delete()
				except:
					pass
				new_user = authenticate(
					username=user.username, password=new_password)
				if new_user:
					serializer = UserSerializer(new_user, read_only=True)
					res['status'] = True
					res['message'] = 'Password reset successfully.'
					res['data'] = serializer.data
					return Response(res, status=status.HTTP_200_OK)

				else:
					res['status'] = False
					res['message'] = 'Password reset but unable to authenticate user, please try again.'
					res['data'] = []
					return Response(res, status=status.HTTP_400_BAD_REQUEST)

		except Exception as e:
			res['status'] = False
			res['message'] = str(e)
			res['data'] = []
			return Response(res, status=status.HTTP_400_BAD_REQUEST)
		
class ForgotPasswordApiView(APIView):
	"""forgot password API view"""

	permission_classes = [AllowAny]

	def post(self, request):
		""" post method for forgot password API """

		res = {}
		try:
			email = request.data.get('email', None)
			if email is None:
				res['status'] = False
				res['message'] = "Email is required."
				res['data'] = []
				return Response(res,  status=status.HTTP_404_NOT_FOUND)

			user = User.objects.filter(username=email).last()
			if user is None:
				res['status'] = False
				res['message'] = "No such user registered with this email."
				res['data'] = []
				return Response(res,  status=status.HTTP_404_NOT_FOUND)

			else:
				user.otp = otp_func()
				user.save()
				name = user.name
				subject = "Here is your OTP to Reset Password"
				recipient_list = [user.email]
				otp = user.otp
				resetPassMail(subject, recipient_list, name, otp)
				res['status'] = True
				res['message'] = "Otp sent Successfully"
				res['data'] = {'id': user.id}
				return Response(res, status=status.HTTP_200_OK)

		except Exception as e:
			res['status'] = False
			res['message'] = str(e)
			res['data'] = []
			return Response(res, status=status.HTTP_400_BAD_REQUEST)
