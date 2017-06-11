from rest_framework import serializers
from GE.models import Registers, Persona


class RegistersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Registers
        fields = (
            'id_register',
            'priority_attention',
            'attention_number',
            'attention_type',
            'start_attention',
            'observations',
            'finish_attention',
            'finish_total_attention',
            'sellplace',
            'sucursal',
        )

    def create(self, validated_data):
        """
        Create and return a new `Snippet` instance, given the validated data.
        """
        return Registers.objects.create(**validated_data)


class PersonaSerializers(serializers.ModelSerializer):
    class Meta:
        model = Persona
        fields = (
            'user',
            'pin',
        )