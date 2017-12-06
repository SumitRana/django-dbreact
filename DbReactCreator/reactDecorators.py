# Author : Sumit|Sam
# Decorators to make any api a sse
import json

def dbreact(uid=None):
	def innerReact(func):
		def wrapper_func(request):
			
			if (uid is None) or (uid is ""):
				raise KeyError("UID for pusher api missing .")
				return func(request)
			else:
				print "in else"
				try:
					exists = request.COOKIES['push-'+uid]
					exists = "true"
					print "in exists:",exists
				except KeyError:
					print "in except"
					exists = "false"

				is_sse = "true"		

				if exists is "true":
					push_exists = "true"
					try:
						previous_state_ids = list(json.loads(request.COOKIES['state-'+uid]))
						print previous_state_ids
						print request.COOKIES['state-'+uid]
					except KeyError:
						print "in key error"
						previous_state_ids = list()
				elif exists is "false":
					print "in exists : false"
					push_exists = "false"
					previous_state_ids = list()

				# tuple data (uid,is_sse,push_exists,previous_state_ids)

				request.META['pusher_data'] = tuple([uid,is_sse,push_exists,previous_state_ids])
				print "Deco-push :",request.META['pusher_data']

			return func(request)
		return wrapper_func
	return innerReact