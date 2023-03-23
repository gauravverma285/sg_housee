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
	
# class UserChangePasswordSerializer(serializers.Serializer):
#   password = serializers.CharField(max_length=255, style={'input_type':'password'}, write_only=True)
#   password2 = serializers.CharField(max_length=255, style={'input_type':'password'}, write_only=True)
#   class Meta:
#     fields = ['password', 'password2']

#   def validate(self, attrs):
#     password = attrs.get('password')
#     password2 = attrs.get('password2')
#     user = self.context.get('user')
#     if password != password2:
#       raise serializers.ValidationError("Password and Confirm Password doesn't match")
#     user.set_password(password)
#     user.save()
#     return attrs