from urllib import error

def errormessage(n):
	if int(n) == 10:
		return 100 , 200
	else:
		raise error.URLError('')

for i in range(1,20):
	try:
		a, b = errormessage(i)

	except error.URLError:
		print ('urlerror',10)
		continue
	
	print (a,b)
