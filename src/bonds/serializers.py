from rest_framework import serializers
from .models import Bonds

class BondsSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        bonds = Bonds.objects.create(**validated_data)
        return bonds

    class Meta:
        model = Bonds
        fields = ['id', 'bond_name', 'number_of_bonds', 'selling_price_mxn', 'user_id', 'status', 'buyer_id']

class BondsUSDSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bonds
        fields = ['id', 'bond_name', 'number_of_bonds', 'selling_price_usd', 'user_id', 'status', 'buyer_id']


class create_bond(serializers.ModelSerializer):
    class Meta:
        model = Bonds
        fields = ['bond_name', 'number_of_bonds', 'selling_price_mxn']
