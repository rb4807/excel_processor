from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from io import BytesIO
import csv
import io
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile

class UserExcelImportViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = "/api/users/user_excel_import/"
        self.valid_csv_data = [
            ["name", "email", "age"],
            ["John Doe", "john@example.com", "30"],
            ["Jane Doe", "jane@example.com", "25"]
        ]
        self.invalid_csv_data = [
            ["wrong_header1", "wrong_header2", "wrong_header3"],
            ["John Doe", "john@example.com", "30"]
        ]

    def generate_csv_file(self, data):
        file = io.StringIO() 
        writer = csv.writer(file)
        writer.writerows(data)  
        file.seek(0)
        return io.BytesIO(file.getvalue().encode("utf-8"))  

    def test_successful_import(self):
        """Test successful CSV import"""
        valid_csv_content = b"name,email,age\nJohn Doe,johndoe@example.com,30\n"  
        file = SimpleUploadedFile("test_users.csv", valid_csv_content, content_type="text/csv")
        response = self.client.post(reverse("user_excel_import"), {"file": file}, format="multipart")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_missing_file(self):
        """Test not providing file"""
        response = self.client.post(self.url, {}, format="multipart")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["error"], "No file provided")
    
    def test_invalid_file_type(self):
        """Test uploading a CSV with invaild file type"""
        invalid_file = BytesIO(b"Invalid content")
        invalid_file.name = "invalid.txt"
        response = self.client.post(self.url, {"file": invalid_file}, format="multipart")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["error"], "Invalid file type. Only CSV files are allowed.")
    
    def test_invalid_headers(self):
        """Test uploading a CSV with incorrect headers"""
        invalid_csv_content = b"wrong_name,wrong_email,wrong_age\nJohn,john@example.com,25\n"
        file = SimpleUploadedFile("test_invalid_headers.csv", invalid_csv_content, content_type="text/csv")
        response = self.client.post(reverse("user_excel_import"), {"file": file}, format="multipart")
        self.assertEqual(response.status_code, 400)
        self.assertIn("Invalid headers", response.data["error"])
