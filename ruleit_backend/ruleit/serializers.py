# serializers.py
from rest_framework import serializers
from .models import Rule

class RuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rule
        fields = ['id', 'rule_name', 'rule_root', 'rule_tokens']  # Include fields you need
