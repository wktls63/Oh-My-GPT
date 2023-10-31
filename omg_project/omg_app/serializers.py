from rest_framework                       import serializers
from .models                              import SubscriptionProduct, User, Payment


class SubscriptionSerializer(serializers.ModelSerializer):
    """
    상품 시리얼라이저
    """
    class Meta:
        model = SubscriptionProduct
        fields = '__all__'


class PaymentSerializer(serializers.ModelSerializer):

    class Meta: 
        model = Payment
        fields = "__all__"


class UserSerializer(serializers.ModelSerializer):
    """
    유저 시리얼라이저
    """
    
    class Meta:
        model = User
        fields = '__all__'
        
class RegisterSerializer(serializers.ModelSerializer):
    """
    회원가입 시리얼라이저
    """
    class Meta:
        model = User
        fields = '__all__'

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user
    
class EmailSerializer(serializers.Serializer):
    """
    이메일 시리얼라이저
    """
    
    email_title = serializers.CharField()
    email_msg = serializers.CharField()
    email = serializers.EmailField()

