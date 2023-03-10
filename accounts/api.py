from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated, AllowAny
from datetime import date
from rest_framework import status
from .serializers import *




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