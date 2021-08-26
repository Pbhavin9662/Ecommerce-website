from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import *
from django.contrib.auth import login, authenticate


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Required. Add a valid email address.')

    class Meta:
        model = Account
        fields = ('email', 'username', 'password1', 'password2')


class ProfileForm(forms.ModelForm):
    profile_image = forms.ImageField()

    class Meta:
        model = Profile
        fields = '__all__'
        # exclude = ['account']  
        widgets={
    # 'account' : forms.TextInput(attrs={'class':'form-control'}),
    'mobile_no ' : forms.TextInput(attrs={'class':'form-control'}),
    'alternate_mobile_no' : forms.TextInput(attrs={'class':'form-control'}),
    'country': forms.TextInput(attrs={'class':'form-control'}),
    


    
    }  

class LoginForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

    class Meta:
        model = Account
        fields = ('email', 'password')

    def clean(self):
        if self.is_valid():
            email = self.cleaned_data['email']
            password = self.cleaned_data['password']
            if not authenticate(email=email, password=password):
                raise forms.ValidationError("Invalid login")



class BillingAddressForm(forms.ModelForm):
    username = forms.CharField(max_length=100,widget=forms.TextInput(attrs={'class':'form-control'}))

    class Meta:
        model = BillingAddress
        fields = ('username', 'mobile', 'email', 'country', 'address1', 'address2', 'city', 'state', 'zipcode')

    widgets={
       
    'mobile' : forms.TextInput(attrs={'class':'form-control'}),
    'email' : forms.TextInput(attrs={'class':'form-control'}),
    'country': forms.TextInput(attrs={'class':'form-control'}),
    'address1' : forms.Textarea(attrs={'class':'form-control'}),
    'address2' : forms.Textarea(attrs={'class':'form-control'}),
    'city' : forms.TextInput(attrs={'class':'form-control'}),
    'state' : forms.TextInput(attrs={'class':'form-control'}),
    'zipcode': forms.TextInput(attrs={'class':'form-control'}),
    }

class ShippingForm(forms.ModelForm):
    class Meta:
        model = ShippingAddress
        fields = ('account','address1', 'city', 'state', 'country', 'zipcode')
        widgets={
       
    
    
    'address1' : forms.Textarea(attrs={'class':'form-control'}),
    'city' : forms.TextInput(attrs={'class':'form-control'}),
    'state' : forms.TextInput(attrs={'class':'form-control'}),
    'country': forms.TextInput(attrs={'class':'form-control'}),
    
    'zipcode': forms.TextInput(attrs={'class':'form-control'}),
    }