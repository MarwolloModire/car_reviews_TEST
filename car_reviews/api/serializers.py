from rest_framework import serializers
from .models import Country, Manufacturer, Car, Comment


class CountrySerializer(serializers.ModelSerializer):
    manufacturers = serializers.SerializerMethodField()

    class Meta:
        model = Country
        fields = ['name', 'manufacturers']

    def get_manufacturers(self, obj):
        manufacturers = Manufacturer.objects.filter(country=obj)
        return ManufacturerSerializer(manufacturers, many=True).data


class ManufacturerSerializer(serializers.ModelSerializer):
    country = serializers.PrimaryKeyRelatedField(
        queryset=Country.objects.all())
    cars = serializers.SerializerMethodField()
    comment_count = serializers.SerializerMethodField()

    class Meta:
        model = Manufacturer
        fields = ['name', 'country', 'cars', 'comment_count']

    def get_cars(self, obj):
        cars = Car.objects.filter(manufacturer=obj)
        return CarSerializer(cars, many=True).data

    def get_comment_count(self, obj):
        # Считаем все комментарии к автомобилям, которые произведены данным производителем
        return Comment.objects.filter(car__manufacturer=obj).count()


class CarSerializer(serializers.ModelSerializer):
    manufacturer = serializers.PrimaryKeyRelatedField(queryset=Manufacturer.objects.all())  # noqa #isort: ignore
    comments = serializers.SerializerMethodField()
    comment_count = serializers.SerializerMethodField()

    class Meta:
        model = Car
        fields = ['name', 'manufacturer', 'start_year', 'end_year', 'comments', 'comment_count']  # noqa #isort: ignore

    def get_comments(self, obj):
        comments = Comment.objects.filter(car=obj)
        return CommentSerializer(comments, many=True).data

    def get_comment_count(self, obj):
        # Считаем количество комментариев, связанных с данным автомобилем
        return Comment.objects.filter(car=obj).count()


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['email', 'car', 'created_at', 'content']

    def validate_email(self, value):
        if not value.endswith('@mail.ru'):
            raise serializers.ValidationError(
                "Email должен быть в домене @mail.ru.")
        return value

    def validate_content(self, value):
        if len(value) < 10:
            raise serializers.ValidationError(
                "Комментарий должен содержать не менее 10 символов.")
        return value

    def validate(self, data):
        car = data.get('car')
        if not Car.objects.filter(id=car.id).exists():
            raise serializers.ValidationError(
                "Выбранный автомобиль не существует.")
        return data
