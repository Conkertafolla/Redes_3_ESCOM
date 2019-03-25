import subprocess
import sys
from datetime import datetime

time_log ="PingPoller"+datetime.now().strftime("%m_%d_%Y_%H_%M_%S")
log_file=open(time_log,'w')

with open('ipTest.txt','r') as ips:
    for ip in ips:
        ip=ip.strip()
        res = subprocess.call(['ping','-c','3',ip])
        date_ping=datetime.now()
        print(res)
        if res == 0:
            print("La direccion "+ip+" respondio correctamente a la fecha "+date_ping.strftime("%m/%d/%Y, %H:%M:%S \n"))
            log_file.write("La direccion "+ip+" respondio correctamente a la fecha "+date_ping.strftime("%m/%d/%Y, %H:%M:%S \n"))
        elif res == 2:
            print("La direccion "+ip+" no respondio correctamente a la fecha "+date_ping.strftime("%m/%d/%Y, %H:%M:%S \n"))
            log_file.write("La direccion "+ip+" no respondio correctamente a la fecha "+date_ping.strftime("%m/%d/%Y, %H:%M:%S\n"))
        else:
            print("Ping a la direccion "+ip+" fallo a la fecha "+date_ping.strftime("%m/%d/%Y, %H:%M:%S \n "))
            log_file.write("Ping a la direccion "+ip+" fallo a la fecha "+date_ping.strftime("%m/%d/%Y, %H:%M:%S \n"))
log_file.close()



