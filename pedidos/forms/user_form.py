from django import forms

from django.contrib.auth.models import User


class UserForm(forms.ModelForm):
    class Meta:
        '''Sub classe para definir meta atributos da classe principal.'''

        model = User

        fields = ['username','password']

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        self.fields['username'].required = False