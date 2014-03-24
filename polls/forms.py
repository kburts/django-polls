from django import forms
from django.contrib.auth.models import User
from django.forms.models import ModelForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Div, Layout, Submit, Button, HTML, Field
from crispy_forms.bootstrap import PrependedText, FormActions

from django.forms.formsets import formset_factory

from polls.models import Poll, Choice, MakePoll, UserProfile
from django.forms.formsets import formset_factory
from django.forms.models import BaseInlineFormSet, inlineformset_factory

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    #email = forms.EmailField(max_length=100, required=False)
    class Meta:
        model = User
        #fields = ('username', 'email', 'password')
        ## I really don't need your email and you're safer not sharing it with me
        fields = ('username', 'password')
    helper = FormHelper()
    helper.form_method = 'POST'
    helper.add_input(Submit('post', 'post', css_class='btn-primary'))

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('website', 'picture')

class LoginForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'password')

'''
class MakeChoices(forms.ModelForm):
    class Meta:
        model = Choice
        exclude = ['poll', 'votes']
    #poll = Poll.objects.get(id=1)
    choice_text = forms.CharField(max_length=200)
'''

class ChoiceForm(forms.ModelForm):
    class Meta:
	model = Choice
	fields = ['choice_text']


class MakePoll(forms.ModelForm):
    class Meta:
        model = Poll
        exclude = ['user']
    #choice = forms.CharField(max_length=200)
    helper = FormHelper()
    helper.form_method = 'POST'
    helper.layout = Layout(
        Field('question'),
        Field('pub_date', type='hidden'),
        #Field('choice'),
        FormActions(Submit('post', 'Post!', css_class='btn-primary')),
    )

class MakeChoices(forms.Form):
    choice_text = forms.CharField(max_length=200, required=False)


