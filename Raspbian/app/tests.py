from django.test import TestCase

# Create your tests here.
import time

now = time.strftime('%Y%m%d%H%M%S',time.localtime(time.time()))
print(now)