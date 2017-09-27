from django.db import models
from _datetime import date

# Create your models here.

import datetime

def getTodayDateTime():
    varTodayDateTime = datetime.datetime.now().strftime('%d/%m/%Y-%H:%M:%S') #strftime("%Y-%m-%d %H:%M:%S")
    return varTodayDateTime

def getTodayDateTimeNowDBFormat():
    varTodayDateTime = datetime.datetime.now()
    return varTodayDateTime

class Utilities(models.Model):
    fechaApertura = None
    today = date.today()
    todayDateTimeNow = getTodayDateTime()
    
    def getTodayDateTimeNow(self):
        return getTodayDateTime()
    
    def getTodayDateTimeNowDBFormat(self):
        return getTodayDateTimeNowDBFormat()
    
