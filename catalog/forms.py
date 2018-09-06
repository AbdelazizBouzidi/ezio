from django import forms
from django.contrib.auth.models import User
from catalog.models import UserProfile

class Search(forms.Form):
    Enter_a_book_name = forms.CharField(max_length=50,initial="",required=False)
    def __init__(self, *args, **kwargs):
        super(Search, self).__init__(*args, **kwargs)
        self.fields['Enter_a_book_name'].widget.attrs.update({'class': 'searchh'})
class SearchSubject(forms.Form):
    Enter_the_subject_name = forms.CharField(max_length=50,initial="",required=False)
    def __init__(self, *args, **kwargs):
        super(SearchSubject, self).__init__(*args, **kwargs)
        self.fields['Enter_the_subject_name'].widget.attrs.update({'class': 'searchh'})
class SearchAuthor(forms.Form):
    Enter_an_author_name = forms.CharField(max_length=50,initial="",required=False)
    def __init__(self, *args, **kwargs):
        super(SearchAuthor, self).__init__(*args, **kwargs)
        self.fields['Enter_an_author_name'].widget.attrs.update({'class': 'searchh'})
from django.contrib.auth.forms import UserCreationForm,UserChangeForm
from django import forms
GENDER_CHOICES = (
        ('Male', 'Male'),
        ('Female', 'Female'),
      )
class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True, help_text='Nikname.')
    last_name = forms.CharField(max_length=30, required=True, help_text='Fsmily name.')
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')
    gender = forms.ChoiceField(choices=GENDER_CHOICES)
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', 'gender',)

    def save(self, commit=True):
        user = super(SignUpForm,self).save(commit = False )
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        user.gender = self.cleaned_data['gender']
class EditProfileForm(UserChangeForm):
    class Meta:
        model= UserProfile
        fields=(
            'gender',
            'avatar',
            'password',
        )
    def __init__(self, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.fields['password'].widget.attrs.update({'class': 'password'})

class UserProfileForm(forms.ModelForm):
    class Meta:
      model = UserProfile
      fields=(
        'avatar',
        'date_of_birth',
        'gender',
       )




