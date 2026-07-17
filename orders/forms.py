from django import forms

from .models import DeliverySlot, Order


class CheckoutForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ["delivery_address", "delivery_slot", "payment_method"]
        widgets = {"delivery_address": forms.Textarea(attrs={"rows": 3})}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["delivery_slot"].queryset = DeliverySlot.objects.filter(is_active=True)
