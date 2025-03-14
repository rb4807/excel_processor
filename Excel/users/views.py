import openpyxl
from utils.file_handler import is_file_valid
from utils.utils import is_template_vaild
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from .serializers import UserSerializer
from django.core.exceptions import ValidationError

class UploadExcelView(APIView):
    def post(self, request, *args, **kwargs):
        try:
            file = request.FILES.get('file')
            if not file:
                return Response({"error": "No file provided"}, status=status.HTTP_400_BAD_REQUEST)
            
            file_validation = is_file_valid(file, 'document')
            if file_validation:
                wb = openpyxl.load_workbook(file)
                sheet = wb.active
                headers = [cell.value for cell in sheet[1]]
                template_validation = is_template_vaild(headers, 'users')
                if template_validation is True:
                    saved_records = 0
                    rejected_records = 0
                    errors = []

                    for row in sheet.iter_rows(min_row=2, values_only=True):
                        row_data = dict(zip(headers, row))

                        if None in row_data.values():
                            rejected_records += 1
                            errors.append({"row": row, "error": "Row contains missing values."})
                            continue

                        row_data['first_name'] = row_data.pop('name')
                        serializer = UserSerializer(data=row_data)
                        if serializer.is_valid():
                            serializer.save()
                            saved_records += 1
                        else:
                            rejected_records += 1
                            errors.append({"row": row, "errors": serializer.errors})
                    return Response({
                        "saved_records": saved_records, "rejected_records": rejected_records, "errors": errors }, status=status.HTTP_201_CREATED)
                return Response({"error": f"Invalid headers. Expected {template_validation}."}, status=status.HTTP_400_BAD_REQUEST)

            return Response({"error": "Invalid file type. Only .xlsx files are allowed."}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({"error": f"Unexpected server error: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
