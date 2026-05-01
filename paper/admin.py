from django.contrib import admin
from.models import subject, question

#here we are registering our models to the admin site so that we can manage them through the admin interface.
admin.site.register(subject)
admin.site.register(question)       

