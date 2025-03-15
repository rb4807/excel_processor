import csv
import os
from io import StringIO
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import FileResponse

# Models
from .serializers import UserSerializer
from users.models import UserProfile
# Modules
from Excel import settings
from utils.file_handler import is_file_valid
from utils.utils import is_template_vaild
from utils.rest_crud_handler import get_related_object


class UserExcelImportView(APIView):
    """ Handle uploaded data of user's """
    def post(self, request, *args, **kwargs):
        file = request.FILES.get("file")
        if not file:
            return Response({"error": "No file provided"}, status=status.HTTP_400_BAD_REQUEST)

        # File validation common funtion for allowed extensions
        if not is_file_valid(file, "document"):
            return Response({"error": "Invalid file type. Only CSV files are allowed."}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            csv_data = file.read().decode("utf-8")
            csv_reader = csv.reader(StringIO(csv_data))
            headers = next(csv_reader, None)

            # Uploaded template validation with expected headers
            expected_headers = is_template_vaild(headers, "users")
            if expected_headers is not True:
                return Response({"error": f"Invalid headers. Expected {expected_headers}."}, status=status.HTTP_400_BAD_REQUEST)

            errors = []
            valid_serializers = []
            created_users = []

            for row in csv_reader:
                # Skip empty row
                if not any(row):
                    continue  
                
                if len(row) != len(headers):
                    errors.append({"row": row, "error": "Row has incorrect number of columns."})
                    continue
                
                row_data = dict(zip(headers, row))
                if "" in row_data.values():
                    errors.append({"row": row, "error": "Row contains missing values."})
                    continue
                
                # Field name correction for serilalizers
                row_data["first_name"] = row_data.pop("name", "") 
                serializer = UserSerializer(data=row_data)
                
                if serializer.is_valid():
                    valid_serializers.append(serializer)
                else:
                    errors.append({"row": row, "errors": serializer.errors})
            
            if errors:
                return Response({ "saved_records": 0, "rejected_records": len(errors), "errors": errors, "created_users": []}, status=status.HTTP_400_BAD_REQUEST)
            
            for serializer in valid_serializers:
                user = serializer.save()
                user_profile = get_related_object(user.id, UserProfile, 'user_id')
                created_users.append({
                    "first_name": user.first_name,
                    "email": user.email,
                    "age": user_profile.age if user_profile else ''
                })  
            
            return Response({ "saved_records": len(valid_serializers), "rejected_records": 0, "errors": [], "created_users": created_users }, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error": f"Unexpected server error: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    """ Handle user csv template download """
    def get(self, request, *args, **kwargs):
        # File path on base directory
        file_path = os.path.join(settings.BASE_DIR, 'data', 'excel_template', 'users','users_import_template.csv')
        if os.path.exists(file_path):
            response = FileResponse(open(file_path, 'rb'))
            response['Content-Disposition'] = 'attachment; filename="users_import_template.csv"'
            return response
        else:
            return Response({"error": "Template file not found"}, status=status.HTTP_404_NOT_FOUND)