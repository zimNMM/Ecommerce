from django import forms
from .models import Order, Payment, Contact
from .models import NewsletterSubscription
from captcha.fields import CaptchaField
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from captcha.fields import CaptchaField

class CustomUserCreationForm(UserCreationForm):
    captcha = CaptchaField()

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'class': 'w-full px-4 py-2 rounded-full border-gray-300 focus:border-indigo-500 focus:ring-2 focus:ring-indigo-200',
            'placeholder': 'Enter your username'
        })
        self.fields['password1'].widget.attrs.update({
            'class': 'w-full px-4 py-2 rounded-full border-gray-300 focus:border-indigo-500 focus:ring-2 focus:ring-indigo-200',
            'placeholder': 'Enter your password'
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'w-full px-4 py-2 rounded-full border-gray-300 focus:border-indigo-500 focus:ring-2 focus:ring-indigo-200',
            'placeholder': 'Confirm your password'
        })
        self.fields['captcha'].widget.attrs.update({
            'class': 'w-full px-4 py-2 rounded-full border-gray-300 focus:border-indigo-500 focus:ring-2 focus:ring-indigo-200',
        })

class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'w-full px-4 py-2 rounded-full border-gray-300 focus:border-indigo-500 focus:ring-2 focus:ring-indigo-200',
        'placeholder': 'Enter your username'
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'w-full px-4 py-2 rounded-full border-gray-300 focus:border-indigo-500 focus:ring-2 focus:ring-indigo-200',
        'placeholder': 'Enter your password'
    }))


class NewsletterForm(forms.ModelForm):
    class Meta:
        model = NewsletterSubscription
        fields = ['email']

class ContactForm(forms.ModelForm):
    captcha = CaptchaField()
    class Meta:
        model = Contact
        fields = ['name', 'email', 'message']
        
class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['fullname', 'address']
class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        exclude = ['order', 'method']
        widgets = {
            'card_expiry_date': forms.TextInput(attrs={'placeholder': 'MM/YY'}),
        }