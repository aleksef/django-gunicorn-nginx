from django.conf import settings # import the settings file

def project_name(request):
    # return the value you want as a dictionnary. you may add multiple values in there.
    return {'PROJECT_NAME': settings.PROJECT_NAME}