import csv
import os
from io import StringIO
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import FileResponse

from .serializers import UserSerializer

from Excel import settings
from utils.file_handler import is_file_valid
from utils.utils import is_template_vaild


class UserExcelImportView(APIView):
    def post(self, request, *args, **kwargs):
        file = request.FILES.get("file")
        if not file:
            return Response({"error": "No file provided"}, status=status.HTTP_400_BAD_REQUEST)

        if not is_file_valid(file, "document"):
            return Response({"error": "Invalid file type. Only CSV files are allowed."}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            csv_data = file.read().decode("utf-8")
            csv_reader = csv.reader(StringIO(csv_data))
            headers = next(csv_reader, None)
            
            expected_headers = is_template_vaild(headers, "users")
            if expected_headers is not True:
                return Response({"error": f"Invalid headers. Expected {expected_headers}."}, status=status.HTTP_400_BAD_REQUEST)

            errors = []
            valid_serializers = []
            
            for row in csv_reader:
                if not any(row):
                    continue  
                
                if len(row) != len(headers):
                    errors.append({"row": row, "error": "Row has incorrect number of columns."})
                    continue
                
                row_data = dict(zip(headers, row))
                if "" in row_data.values():
                    errors.append({"row": row, "error": "Row contains missing values."})
                    continue
                
                row_data["first_name"] = row_data.pop("name", "") 
                serializer = UserSerializer(data=row_data)
                
                if serializer.is_valid():
                    valid_serializers.append(serializer)
                else:
                    errors.append({"row": row, "errors": serializer.errors})
            
            if errors:
                return Response({ "saved_records": 0, "rejected_records": len(errors), "errors": errors }, status=status.HTTP_400_BAD_REQUEST)
            
            for serializer in valid_serializers:
                serializer.save()
            
            return Response({ "saved_records": len(valid_serializers), "rejected_records": 0, "errors": [] }, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error": f"Unexpected server error: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def get(self, request, *args, **kwargs):
        file_path = os.path.join(settings.BASE_DIR, 'data', 'excel_template', 'users','users_import_template.csv')
        if os.path.exists(file_path):
            response = FileResponse(open(file_path, 'rb'))
            response['Content-Disposition'] = 'attachment; filename="users_import_template.csv"'
            return response
        else:
            return Response({"error": "Template file not found"}, status=status.HTTP_404_NOT_FOUND)