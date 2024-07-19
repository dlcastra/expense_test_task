from collections import OrderedDict

from django.db.models import Sum, Value
from django.db.models.functions import Coalesce, TruncMonth


def summary_per_category(queryset):
    return OrderedDict(
        sorted(
            queryset.annotate(category_name=Coalesce("category__name", Value("-")))
            .order_by()
            .values("category_name")
            .annotate(s=Sum("amount"))
            .values_list("category_name", "s")
        )
    )


def total_expenses_by_year_month(queryset):
    return OrderedDict(
        sorted(
            queryset.annotate(month=TruncMonth("date"))
            .values("month")
            .annotate(total=Sum("amount"))
            .order_by("month")
            .values_list("month", "total")
        )
    )
