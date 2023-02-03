from django.contrib import admin
from .models import User, Category, Product

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'chat_id', 'link')

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'status', 'user')
    list_filter = ('status', 'created')
    list_editable = ('price', 'status')
    raw_id_fields = ('category',)
    actions = ('change_status',)

    @admin.action(description='change status of model')
    def change_status(self, request, queryset):
        rows_count = queryset.update(status=True)
        self.message_user(request, f'{rows_count} status has changed')
        