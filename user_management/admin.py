from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import UserProfile, Language, LanguageSkill, TranslationSkill

admin.site.register(UserProfile, UserAdmin)
admin.site.register(Language, admin.ModelAdmin)
admin.site.register(LanguageSkill, admin.ModelAdmin)
admin.site.register(TranslationSkill, admin.ModelAdmin)
