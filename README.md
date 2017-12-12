## DbReact

DbReact is simple but effective django app which makes any database defined within the project reactive 
using SSE ( Server Side Events - no need to install anything for sse | its a http concept ).

The library provides any addition ,or deletion of objects in model ( row in rdms table ) ,in a json based protocol
( sends json structure of objects deleted and added ) to the client (Android ,Ios ,Web).

( On more Granular Level ) you can also make group of Model objects as reactive .

####Quick start
-----------

1. Add middleware string in middleware list of your project (in settings.py):
	
	```python
    MIDDLEWARE_CLASSES = [
        ...
        'DbReactCreator.reactMiddle.reactiveMiddleware',
    ]
    ```

2. Import reactive decorator to views where you want to create the event pusher, and then create eventsource::
	
	```python
	from DbReactCreator.reactDecorators import dbreact

	...

	@dbreact("unique_id_for_eventsource_in_string")
	def pusher_function(request):
		request.META['objects_to_be_reactive'] = Model.objects.all() | Model.objects.filter() ( always a list of queryset objects)
		request.META['for_model'] = Model
		return JsonResponse({},status=200)
	```

3. Define a url for the view , then pass this url to the EventSource (SSE EventSource)  .

4. As soon as client registers the url ,it starts getting json objects of the elements not present on its end.

* Format of data received by client :
	{ add: [ json_serialized_queryset_object, ... ],
	  delete: [ json_serialized_queryset_object, ... ]
	  }

* [Install with pip](https://pypi.python.org/pypi/django-dbreact)