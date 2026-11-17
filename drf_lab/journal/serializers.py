from rest_framework import serializers

from .models import Article, Category


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name", "description"]


class ArticleSerializer(serializers.ModelSerializer):
    # Show the author's username, and never let the client choose the author.
    author = serializers.ReadOnlyField(source="author.username")
    # Clients send category ids, e.g. "categories": [1, 3]
    categories = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Category.objects.all(), required=False
    )

    class Meta:
        model = Article
        fields = [
            "id",
            "title",
            "body",
            "author",
            "categories",
            "is_published",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["created_at", "updated_at"]

    # Lesson 04: validation for ONE field -> a method called validate_<field_name>
    def validate_title(self, value):
        if len(value.strip()) < 5:
            raise serializers.ValidationError("Title must be at least 5 characters long.")
        return value.strip()

    # Lesson 04: validation that needs SEVERAL fields -> validate()
    def validate(self, data):
        # On an update, a field that was not sent keeps its old value (self.instance).
        body = data.get("body", getattr(self.instance, "body", ""))
        is_published = data.get("is_published", getattr(self.instance, "is_published", False))
        if is_published and len(body) < 20:
            raise serializers.ValidationError(
                {"body": "A published article needs a body of at least 20 characters."}
            )
        return data
