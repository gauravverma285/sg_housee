from rest_framework import serializers
from rest_framework.authtoken.models import Token
from .models import *



class UserSerializer(serializers.ModelSerializer):
	""" user serializer """

	token_detail = serializers.SerializerMethodField("get_token_detail")
	class Meta:
		model = User 
		fields = ('id', 'username', 'name', 'email', 'mobile', 'token_detail',)
		extra_kwargs = {
			'token_detail': {'read_only': True}
		}
		
	def get_token_detail(self, obj):
		token, created = Token.objects.get_or_create(user=obj)
		return token.key

	def get_user(self, request):
		user = request
		return user
	