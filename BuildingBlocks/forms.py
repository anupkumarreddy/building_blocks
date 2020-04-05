from django.forms import ModelForm, modelformset_factory
from BuildingBlocks.models import WishListItem


ShoppingFormSet = modelformset_factory(WishListItem, fields='__all__')


class WishListItemForm(ModelForm):
     class Meta:
         model = WishListItem
         fields = '__all__'

