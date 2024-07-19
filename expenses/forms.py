from django import forms

from .models import Expense, Category


class ExpenseSearchForm(forms.ModelForm):
    date_from = forms.DateField(widget=forms.DateInput(format="%Y-%m-%d", attrs={"type": "date"}))
    date_to = forms.DateField(widget=forms.DateInput(format="%Y-%m-%d", attrs={"type": "date"}))
    categories = forms.ModelMultipleChoiceField(queryset=Category.objects.all(), widget=forms.CheckboxSelectMultiple)

    sort_by = forms.ChoiceField(
        required=False,
        choices=[
            ("date", "Date"),
            ("category", "Category"),
        ],
        widget=forms.Select(attrs={"class": "form-control"}),
    )
    order = forms.ChoiceField(
        required=False,
        choices=[
            ("asc", "Ascending"),
            ("desc", "Descending"),
        ],
        widget=forms.Select(attrs={"class": "form-control"}),
    )

    class Meta:
        model = Expense
        fields = ("name", "date_from", "date_to", "categories", "sort_by", "order")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["name"].required = False
        self.fields["date_from"].required = False
        self.fields["date_to"].required = False
        self.fields["categories"].required = False
        self.fields["sort_by"].required = False
        self.fields["order"].required = False
