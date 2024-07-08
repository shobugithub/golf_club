from django import forms
from golf.models import Getnewsletter, Contact_us

class News_letter(forms.ModelForm):
    class Meta:
        model = Getnewsletter
        fields = ('email',)


class Become_member(forms.Form):
    full_name = forms.CharField()
    email_address = forms.EmailField()
    comments = forms.CharField()