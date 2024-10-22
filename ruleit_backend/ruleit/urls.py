from django.urls import path
from .views import home, create_rule_view, combine_rules_view, evaluate_rule_view

urlpatterns = [
    path('', home, name='home'),  # You can define home here if necessary
    path('create_rule/', create_rule_view, name='create_rule'),
    path('combine_rules/', combine_rules_view, name='combine_rules'),
    path('evaluate_rule/', evaluate_rule_view, name='evaluate_rule'),
]
