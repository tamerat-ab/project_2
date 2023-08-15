from .models import Auction_list
from django import forms


class List_form(forms.ModelForm):

    model=Auction_list
    fields=('item_name','price','description','number','image')