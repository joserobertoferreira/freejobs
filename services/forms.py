from django import forms

from services.models import ServiceOrder, ServiceOrderReview


class ServiceOrderForm(forms.ModelForm):
    class Meta:
        model = ServiceOrder
        fields = ['service', 'name', 'email', 'phone', 'address', 'extra_info']
        widgets = {
            'address': forms.TextInput(),
            'service': forms.HiddenInput(),
        }


class ServiceOrderReviewForm(forms.ModelForm):
    class Meta:
        model = ServiceOrderReview
        fields = (
            'rating',
            'comment',
            'order',
        )
        widgets = {
            'rating': forms.HiddenInput(attrs={'id': 'rating-value'}),
            'order': forms.HiddenInput(),
            'comment': forms.Textarea(
                attrs={
                    'id': 'review-text',
                    'placeholder': 'Deixe seus comentários...',
                    'rows': 19,
                }
            ),
        }
