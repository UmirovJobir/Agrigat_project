from django.contrib import admin


class AdsCategoryFilter(admin.SimpleListFilter):
    title = 'Asosiy toifalar'
    parameter_name = 'category'

    def lookups(self, request, model_admin):
        return [(i.name, i.name) for i in model_admin.model.objects.filter(parent__isnull=True)]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(parent__name=self.value())