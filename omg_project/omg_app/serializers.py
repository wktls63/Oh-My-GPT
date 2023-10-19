from rest_framework                       import serializers
from .models                              import SubscriptionProduct


class SubscriptionSerializer(serializers.ModelSerializer):
    """
    상품 시리얼라이저
    """
    class Meta:
        model = SubscriptionProduct
        fields = '__all__'