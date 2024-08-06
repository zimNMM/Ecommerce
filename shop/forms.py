from django import forms
from .models import Order, Payment, Contact
from .models import NewsletterSubscription
from captcha.fields import CaptchaField
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