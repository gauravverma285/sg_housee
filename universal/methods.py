import math, random
import string
from django.conf import settings


def otp_func() :
 
	# Declare a digits variable 
	# which stores all digits
	digits = "0123456789"
	OTP = ""
 
   # length of password can be changed
   # by changing value in range
	for i in range(6) :
		OTP += digits[math.floor(random.random() * 10)]
 
	return OTP

def random_data(input_data):
	uid = str(random.randint(1, 9)) +  random.choice(string.ascii_letters).upper() + str(random.randint(1, 9)) + str(input_data) + random.choice(string.ascii_letters) + str(random.randint(1, 9))
	return uid