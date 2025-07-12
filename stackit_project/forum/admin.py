from django.contrib import admin
from .models import Question, Answer, Tag, Notification

admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(Tag)           # ✅ This line makes Tag show up in admin
admin.site.register(Notification)
