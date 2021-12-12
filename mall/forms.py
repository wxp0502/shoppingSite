from django import forms
from .models import Commodity


class CommodityForm(forms.ModelForm):
    class Meta:
        model = Commodity
        fields = '__all__'
