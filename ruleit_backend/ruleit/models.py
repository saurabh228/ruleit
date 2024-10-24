# models.py
from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.postgres.fields import ArrayField

class Node(models.Model):
    NODE_TYPE_CHOICES = (
        ('operator', 'Operator'),
        ('variable', 'Variable'),
        ('literal', 'Literal'),
    )
    
    node_type = models.CharField(max_length=10, choices=NODE_TYPE_CHOICES)
    left = models.ForeignKey('self', null=True, blank=True, related_name='left_child', on_delete=models.CASCADE)
    right = models.ForeignKey('self', null=True, blank=True, related_name='right_child', on_delete=models.CASCADE)
    value = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f"{self.node_type}: {self.value or 'None'}"

    def clean(self):
        if self.node_type == 'operator' and (not self.left or not self.right):
            raise ValidationError("Operator nodes must have both left and right children.")

class Rule(models.Model):
    rule_name = models.CharField(max_length=225, null=True, blank=True, unique=True)
    rule_root = models.OneToOneField(Node, on_delete=models.CASCADE)
    rule_tokens = ArrayField(
        models.CharField(max_length=255),
        blank=True,
        null=True,
        help_text="Stores the tokenized version of the rule string."
    )
    def __str__(self):
        return self.rule_name or f"Rule id:{self.id}\nRule: {self.rule_tokens}"