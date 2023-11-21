from .models import Auction_list
from django import forms
from django.forms import CharField, ModelMultipleChoiceField, ModelChoiceField


class List_form(forms.ModelForm):
    class Meta:
        model=Auction_list
        # fields = "__all__"
        fields=('item_name','price','amount','image','category')

    
