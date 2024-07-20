from django.db.models import F, Sum
from django.views.generic.list import ListView

from .forms import ExpenseSearchForm
from .models import Expense, Category
from .reports import summary_per_category, total_expenses_by_year_month


class ExpenseListView(ListView):
    model = Expense
    paginate_by = 5

    def get_context_data(self, *, object_list=None, **kwargs):
        queryset = object_list if object_list is not None else self.object_list

        form = ExpenseSearchForm(self.request.GET)
        if form.is_valid():
            # Search context
            name = form.cleaned_data.get("name", "").strip()
            date_from = form.cleaned_data.get("date_from")
            date_to = form.cleaned_data.get("date_to")
            selected_categories = form.cleaned_data.get("categories")

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

            # Sort by category or date (ascending and descending)
            sort_by = self.request.GET.get("sort_by")
            order = self.request.GET.get("order", "asc")

            valid_sort_fields = {
                "category": "category",
                "date": "date",
            }

            if sort_by in valid_sort_fields:
                queryset = queryset.order_by(
                    F(valid_sort_fields[sort_by]).asc() if order == "asc" else F(valid_sort_fields[sort_by]).desc()
                )

        return super().get_context_data(
            form=form,
            object_list=queryset,
            summary_per_category=summary_per_category(queryset),
            total_amount_spent=queryset.aggregate(total=Sum("amount"))["total"] or 0,
            total_expenses_by_year_month=total_expenses_by_year_month(queryset),
            **kwargs
        )


class CategoryListView(ListView):
    model = Category
    paginate_by = 5

    def get_context_data(self, *, object_list=None, **kwargs):
        queryset = Expense.objects.all()

        return super().get_context_data(summary_per_category=summary_per_category(queryset))
