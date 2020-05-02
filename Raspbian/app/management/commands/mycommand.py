from django.core.management.base import BaseCommand
from app.hardware import dht11
import RPi.GPIO
import time
from app.models import TH_FORM

class Command(BaseCommand):
    def handle(self, *args, **options):
        while True:
            instance = dht11.DHT11(4)
            result = instance.read()
            if result.is_valid():
                temp = result.temperature
                hum = result.humidity
                RPi.GPIO.cleanup(4)
                now = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
                thd = TH_FORM(timeval=now, temperature=temp, humidity=hum)
                thd.save()
                print("isSaved")
            time.sleep(300)
