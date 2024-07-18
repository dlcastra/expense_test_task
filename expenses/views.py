from django.views.generic.list import ListView

from .forms import ExpenseSearchForm
from .models import Expense, Category
from .reports import summary_per_category


class ExpenseListView(ListView):
    model = Expense
    paginate_by = 5

    def get_context_data(self, *, object_list=None, **kwargs):
        queryset = object_list if object_list is not None else self.object_list

        form = ExpenseSearchForm(self.request.GET)
        if form.is_valid():
            name = form.cleaned_data.get("name", "").strip()
            date_from = form.cleaned_data.get("date_from")
            date_to = form.cleaned_data.get("date_to")
            selected_categories = form.cleaned_data.get("categories")
            print(selected_categories)

            # Search by name
            if name:
                queryset = queryset.filter(name__icontains=name)

            # Search by date: from and/or to
            if date_from and date_to:
                queryset = queryset.filter(date__range=[date_from, date_to]).order_by("date")
            elif date_from:
                queryset = queryset.filter(date__gte=date_from).order_by("date")
            elif date_to:
                queryset = queryset.filter(date__lte=date_to).order_by("date")

            # Search by categories: single or multiple categories
            if selected_categories:
                queryset = queryset.filter(category__in=selected_categories)

        return super().get_context_data(
            form=form, object_list=queryset, summary_per_category=summary_per_category(queryset), **kwargs
        )


class CategoryListView(ListView):
    model = Category
    paginate_by = 5
