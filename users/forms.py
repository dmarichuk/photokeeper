from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm

User = get_user_model()


class CreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'avatar']


class EditProfileForm(ModelForm):
    class Meta():
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'avatar']
        exclude = ['password', ]
