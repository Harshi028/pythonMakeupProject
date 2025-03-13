from django import forms
from .models import Parlour, Menu

class ParForm(forms.ModelForm):
    class Meta:
        model = Parlour
        fields = ['Par_name','Makeup_cat','rating','img','address']


class MenuForm(forms.ModelForm):
    class Meta:
        model = Menu
        fields = ['item_name', 'description', 'price', 'category']