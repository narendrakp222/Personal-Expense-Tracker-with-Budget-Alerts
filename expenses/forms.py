# 


from django import forms

from .models import Budget, Category


class BudgetForm(forms.ModelForm):
    class Meta:
        model = Budget
        fields = ["category", "monthly_limit", "month_year"]
        widgets = {
            "category": forms.Select(attrs={"class": "form-control"}),
            "monthly_limit": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "step": "0.01",
                    "min": "0.01",
                    "placeholder": "Enter monthly limit",
                }
            ),
            "month_year": forms.DateInput(
                attrs={"class": "form-control", "type": "date"}
            ),
        }

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        # Show only the logged-in user's categories in the dropdown
        if user is not None:
            self.fields["category"].queryset = Category.objects.filter(user=user)
        else:
            self.fields["category"].queryset = Category.objects.none()

    def clean_monthly_limit(self):
        monthly_limit = self.cleaned_data["monthly_limit"]
        if monthly_limit <= 0:
            raise forms.ValidationError("Monthly limit must be greater than zero.")
        return monthly_limit