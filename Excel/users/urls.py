from django.urls import path
from .views import UploadExcelView

urlpatterns = [
    path('download_users_csv_template/', UploadExcelView.as_view(), name='download_users_csv_template'),
    # path('import_users_csv/', UploadCSVView.as_view(), name='import_users_csv'),
]
