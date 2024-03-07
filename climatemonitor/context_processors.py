from .models import usersetting

def usersettings_context(request):
    user = request.user
    theme = ""

    if user.is_authenticated:
        theme = user.usersetting_set.filter(setting__name="theme").first()
        
        if theme:
            theme = theme.value.lower()

        if theme not in ['light', 'dark']:
            theme = ""

    
    return {'theme': theme}