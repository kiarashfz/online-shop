from django.contrib import admin

from core.admin import BaseAdmin
from company.models import Question, SiteSetting


class QuestionAdmin(BaseAdmin):
    ordering = ['created']
    list_display = ['question', 'answer', 'created']
    list_editable = ['answer']
    search_fields = ['question', 'answer']
    # list_filter = ['country']
    list_per_page = 5
    # fieldsets = (
    #     (None, {
    #         'fields': ('name', 'categories')
    #     }),
    #     ('Optionals', {
    #         'fields': ('country', 'description', 'discount'),
    #     }),
    # )
    # filter_vertical = ['categories']
    # autocomplete_fields = ['categories']
    # inlines = [ProductInline]


class SiteSettingAdmin(BaseAdmin):
    list_display = ['site_name']
    # list_editable = ['answer']
    # search_fields = ['question', 'answer']
    # list_filter = ['country']
    # list_per_page = 5


admin.site.register(Question, QuestionAdmin)
admin.site.register(SiteSetting, SiteSettingAdmin)
