from django.test import TestCase

# Create your tests here.
import time
from app.models import TH_FORM

THD = TH_FORM.objects.all()
print(type(THD))

#now = time.strftime('%Y %m %d %H %M %S',time.localtime(time.time()))
#print(now)