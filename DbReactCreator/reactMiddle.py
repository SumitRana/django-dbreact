# Author -Sumit|Sam

from django.http import HttpResponseRedirect,HttpResponse
import json


class Serialize:
	def serializeDjangoModel(cls,row_object,traverse_to_top=None):
		try:
			lcs = row_object._meta.local_fields
			local_column_names = []
			jdata = dict()
			for lc in lcs:
				value = getattr(row_object,str(lc.name))
				jdata[str(lc.name)] = cls.serializeDjangoModel(value)
			return jdata
		except Exception:
			return str(row_object)

class reactiveMiddleware(object):

	def process_response(self,request,response):
		
		if request.META.get('pusher_data'):
			# given
			pusher_data = request.META.get('pusher_data')
			print "MIDDLE-rec :",pusher_data
			modal = request.META['for_model']
			try:
				objects_list = request.META['objects_to_be_reactive']
			except:
				objects_list = modal.objects.none()

			# logic
			try:
				previous_ids = tuple(pusher_data[3])
			except KeyError:
				previous_ids = tuple()

			apps = objects_list.filter().exclude(id__in=list(previous_ids))
			new_ids = list(previous_ids)

			all_apps_ids = list(objects_list.filter().values_list('id',flat=True))
			
			l = []
			for app in apps:
				l.append(Serialize().serializeDjangoModel(app))
				new_ids.append(app.id)
				all_apps_ids.remove(app.id)

			difference = list(set(list(previous_ids)).difference(set(all_apps_ids)))

			if len(difference) != 0:
				for diff in difference:
					new_ids.remove(diff)

			dt = {
				"delete": difference,
				"add": l
			}

			# output to response
			data = "data:"+json.dumps(dt)+"\n\n"
			response = HttpResponse(data)
			response.set_cookie('push-'+pusher_data[0],"true")
			response['Content-Type'] = "text/event-stream"
			response['Cache-Control'] = "no-cache"
			response.set_cookie("state-"+str(pusher_data[0]),json.dumps(new_ids))
		else:
			pass
		return response