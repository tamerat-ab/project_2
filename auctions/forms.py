from .models import Auction_list
from django import forms


class List_form(forms.ModelForm):
    class Meta:
        model=Auction_list
        fields = "__all__"
        # fields=('item_name','price','description','amount','image', 'date_created')

    
 