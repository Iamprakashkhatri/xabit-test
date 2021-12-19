from django.contrib import admin
from django.apps import apps
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend

app = apps.get_app_config('user')

for model_name, model in app.models.items():

    class PostAdmin(admin.ModelAdmin):
        list_display = [field.name for field in model._meta.fields if field.name != "password"]

    try:
        admin.site.register(model, PostAdmin)
    except:
        pass

class EmailBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        UserModel = get_user_model()
        try:
            user = UserModel.objects.get(username=username)
        except UserModel.DoesNotExist:
            return None
        else:
            if user.check_password(password):
                return user
        return None