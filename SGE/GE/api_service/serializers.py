from rest_framework import serializers
from GE.models import Registers, Persona, InitialAttention, AttentionType, Alerta, Promotion


class RegistersSerializer(serializers.ModelSerializer):
    attention_number = serializers.PrimaryKeyRelatedField(
        read_only=True, source='attention_number.attention_number',
    )
    attention_type = serializers.PrimaryKeyRelatedField(
        read_only=True, source='attention_type.name',
    )

    created = serializers.PrimaryKeyRelatedField(
        read_only=True, source='attention_number.created',
    )

    pin = serializers.PrimaryKeyRelatedField(
        read_only=True, source='pin.last_name',
    )


    class Meta:
        model = Registers
        fields = '__all__'

    def create(self, validated_data):
        """
        Create and return a new `Snippet` instance, given the validated data.
        """
        return Registers.objects.create(**validated_data)


class PersonaSerializers(serializers.ModelSerializer):

    class Meta:
        model = Persona
        fields = '__all__'


class PromotionSerializers(serializers.ModelSerializer):

    class Meta:
        model = Promotion
        fields = '__all__'


class InitialAttentionSerializers(serializers.ModelSerializer):
    class Meta:
        model = InitialAttention
        fields = (
            'attention_number',
            'attention_type',
            'created'
        )


class AlertaSerializers(serializers.ModelSerializer):
    class Meta:
        model = Alerta
        fields = '__all__'


class AttentionTypeSerializers(serializers.ModelSerializer):
    class Meta:
        model = AttentionType
        fields = '__all__'
