from rest_framework import generics, serializers
from .models import Contact
import phonenumbers


def normalize_phone(phone: str, default_region: str = 'IN'):
    try:
        parsed = phonenumbers.parse(phone, default_region)
        if not phonenumbers.is_possible_number(parsed) or not phonenumbers.is_valid_number(parsed):
            return None
        return phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.E164)
    except Exception:
        return None


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = ['id', 'name', 'phone', 'email', 'created_at']

    def validate_phone(self, value):
        norm = normalize_phone(value)
        if not norm:
            raise serializers.ValidationError('Invalid phone')
        return norm

    def create(self, validated_data):
        validated_data['owner'] = self.context['request'].user
        return super().create(validated_data)


class ContactCreateView(generics.CreateAPIView):
    serializer_class = ContactSerializer

# Create your views here.
