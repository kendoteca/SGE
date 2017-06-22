from rest_framework import serializers
from GE.models import Registers, Persona, InitialAttention, AttentionType, Alerta


class RegistersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Registers
        fields = '__all__'

    def create(self, validated_data):
        """
        Create and return a new `Snippet` instance, given the validated data.
        """
        return Registers.objects.create(**validated_data)


class PersonaSerializers(serializers.ModelSerializer):

    name = serializers.PrimaryKeyRelatedField(
        read_only=True, source='user.first_name',
        default=serializers.CurrentUserDefault()
    )

    last_name = serializers.PrimaryKeyRelatedField(
        read_only=True, source='user.last_name',
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = Persona
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
