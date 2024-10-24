from django.urls import path
from .views import home, create_rule_view, combine_rules_view, evaluate_rule_view, get_rules, edit_rule_view, get_rule_by_id

urlpatterns = [
    path('', home, name='home'),
    path('api/create-rule/', create_rule_view, name='create_rule'),
    path('api/edit-rule/', edit_rule_view, name='edit_rule'),
    path('api/combine-rules/', combine_rules_view, name='combine_rules'),
    path('api/evaluate-rule/', evaluate_rule_view, name='evaluate_rule'),
    path('api/rules/', get_rules, name='get_rules'),
    path('api/rules/<int:rule_id>/', get_rule_by_id, name='get_rule_by_id'),
]
