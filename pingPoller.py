import subprocess
res = subprocess.call(['ping','-c','3','10.0.1.2'])
print (res)