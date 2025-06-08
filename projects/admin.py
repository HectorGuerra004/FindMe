from django.contrib import admin

from .models import User, Profile, Portfolio, Education, Experience, Skill, Like, Petition

admin.site.register(User)
admin.site.register(Profile)
admin.site.register(Portfolio)
admin.site.register(Education)
admin.site.register(Experience)
admin.site.register(Skill)
admin.site.register(Like)
admin.site.register(Petition)