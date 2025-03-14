from rest_framework.exceptions import ValidationError


class RestCRUDHandler:
    def __init__(self, serializer_class=None, model_class=None):
        self.serializer_class = serializer_class
        self.model_class = model_class

    def create_custom(self, data):
        try:
            serializer = self.serializer_class(data=data)
            if serializer.is_valid():
                serializer.save()
                return serializer.data
            else:
                raise ValidationError(serializer.errors)
        except Exception as e:
            print(e)
            return None

    def update_custom(self, instance, data):
        try:
            serializer = self.serializer_class(instance, data=data)
            if serializer.is_valid():
                serializer.save()
                return serializer.data
            else:
                raise ValidationError(serializer.errors)
        except Exception as e:
            print(e)
            return None

    def delete_custom(self, delete_filter):
        try:
            if self.model_class and isinstance(delete_filter, dict) and len(delete_filter):
                self.model_class.objects.filter(**delete_filter).delete()
                return True
            else:
                return False
        except Exception as e:
            print(e)
            return False

    def get_custom(self, get_filter):
        try:
            if self.model_class:
                instance = self.model_class.objects.get(**get_filter)
                serializer = self.serializer_class(instance)
                return serializer.data
            else:
                return None
        except self.model_class.DoesNotExist:
            return None

    def list_custom(self, list_filter=None):
        try:
            if self.model_class:
                if list_filter is not None:
                    queryset = self.model_class.objects.filter(**list_filter).order_by('-id')
                else:
                    queryset = self.model_class.objects.all().order_by('-id')
                serializer = self.serializer_class(queryset, many=True)
                return serializer.data
            else:
                return []
        except self.model_class.DoesNotExist:
            return []

    def get_object(self, pk, field_name=None):
        try:
            if field_name is not None:
                return self.model_class.objects.get(**{field_name: pk})
            else:
                return self.model_class.objects.get(pk=pk)
        except self.model_class.DoesNotExist:
            return None


def get_related_object(related_id, model_class, field_name=None):
    try:
        rest_crud = RestCRUDHandler(model_class=model_class)
        related_obj = rest_crud.get_object(related_id, field_name)
        return related_obj
    except:
        return None
