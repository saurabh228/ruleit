from django.contrib import admin
from .models import Node, Rule

class NodeAdmin(admin.ModelAdmin):
    list_display = ('id', 'node_type', 'value' )
    readonly_fields = ('id',)

class RuleAdmin(admin.ModelAdmin):
    list_display = ('id', 'rule_name', 'rule_tokens')
    readonly_fields = ('id',)

admin.site.register(Node, NodeAdmin)
admin.site.register(Rule, RuleAdmin)