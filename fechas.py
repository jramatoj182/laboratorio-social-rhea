from datetime import date
from datetime import datetime

#Día actual
today = date.today()

#Fecha actual
now = datetime.now()

print(today)
print(now)
format = now.strftime('jhonta%d%m%Y%H%M%S%f')
print(format)