from modeltranslation.translator import register, TranslationOptions
from .models import (
    AdsCategory,
    UsefulCategory,
)

@register(AdsCategory)
class AdsCategoryTranslationOptions(TranslationOptions):
    fields = ['name']


@register(UsefulCategory)
class UsefulCategoryTranslationOptions(TranslationOptions):
    fields = ['name']