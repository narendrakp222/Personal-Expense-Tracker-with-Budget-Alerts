from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Budget, Category, Expense


class UserCategoryChoiceField(forms.ModelChoiceField):
    def to_python(self, value):
        if value in self.empty_values:
            return None

        try:
            return super().to_python(value)
        except forms.ValidationError as exc:
            try:
                return self.queryset.get(name=value)
            except Category.DoesNotExist:
                raise exc


class UserScopedCategoryMixin:
    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        if user is not None:
            self.fields["category"].queryset = Category.objects.filter(user=user)
        else:
            self.fields["category"].queryset = Category.objects.all()


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ["name", "description"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
        }


class BudgetForm(UserScopedCategoryMixin, forms.ModelForm):
    category = UserCategoryChoiceField(
        queryset=Category.objects.none(),
        widget=forms.Select(attrs={"class": "form-select"}),
    )
    month_year = forms.DateField(
        input_formats=["%Y-%m", "%Y-%m-%d"],
        widget=forms.DateInput(attrs={"class": "form-control", "type": "month"}, format="%Y-%m"),
    )

    class Meta:
        model = Budget
        fields = ["category", "monthly_limit", "month_year"]
        widgets = {
            "monthly_limit": forms.NumberInput(attrs={"class": "form-control", "step": "0.01", "min": "0.01"}),
        }

    def clean_monthly_limit(self):
        monthly_limit = self.cleaned_data.get("monthly_limit")
        if monthly_limit is None or monthly_limit <= 0:
            raise forms.ValidationError("Monthly limit must be greater than zero.")
        return monthly_limit

    def clean_month_year(self):
        month_year = self.cleaned_data.get("month_year")
        if month_year:
            return month_year.replace(day=1)
        return month_year


class ExpenseForm(UserScopedCategoryMixin, forms.ModelForm):
    category = UserCategoryChoiceField(
        queryset=Category.objects.none(),
        widget=forms.Select(attrs={"class": "form-select"}),
    )

    class Meta:
        model = Expense
        fields = ["amount", "date", "category", "notes"]
        widgets = {
            "amount": forms.NumberInput(attrs={"class": "form-control", "step": "0.01", "min": "0.01"}),
            "date": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
            "notes": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
        }

    def clean_amount(self):
        amount = self.cleaned_data.get("amount")
        if amount is None or amount <= 0:
            raise forms.ValidationError("Amount must be greater than zero.")
        return amount
