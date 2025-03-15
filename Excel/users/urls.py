from django.urls import path
from .views import UserExcelImportView

urlpatterns = [
    path('user_excel_import/', UserExcelImportView.as_view(), name='user_excel_import'),
]
