from django.contrib import admin
from django.contrib.admin.widgets import AdminFileWidget

from . import models

# Register your models here.

# Image viewing widget for admin
class AdminBase64ImageView(AdminFileWidget):
	def render(self, name, value, attrs=None):
		return '<img src="{0}">'.format(value)

class PlayerAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.Base64ImageField: {'widget': AdminBase64ImageView }
    }

admin.site.register(models.Player, PlayerAdmin)
admin.site.register(models.Session)