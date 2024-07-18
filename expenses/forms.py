from django import forms

from .models import Expense, Category


class ExpenseSearchForm(forms.ModelForm):
    date_from = forms.DateField(widget=forms.DateInput(format="%Y-%m-%d", attrs={"type": "date"}))
    date_to = forms.DateField(widget=forms.DateInput(format="%Y-%m-%d", attrs={"type": "date"}))
    categories = forms.ModelMultipleChoiceField(queryset=Category.objects.all(), widget=forms.CheckboxSelectMultiple)

    class Meta:
        model = Expense
        fields = ("name", "date_from", "date_to", "categories")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["name"].required = False
        self.fields["date_from"].required = False
        self.fields["date_to"].required = False
        self.fields["categories"].required = False
