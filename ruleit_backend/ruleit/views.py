# views.py
from django.shortcuts import render
from django.http import JsonResponse
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .utils import create_rule, combine_rules, evaluate_rule
from .models import Node, Rule

@swagger_auto_schema(
    method='post',
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'rule_string': openapi.Schema(
                type=openapi.TYPE_STRING, 
                description='The rule string',
                example="A > 10 AND color = yellow"
            ),
            'rule_name': openapi.Schema(
                type=openapi.TYPE_STRING, 
                description='A unique name to identify the rule',
                example="Rule_01"
            )
        },
    ),
    responses={
        201: openapi.Response('Combined rule created successfully', 
            openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'rule_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='ID of the created rule'),
                    'rule_name': openapi.Schema(type=openapi.TYPE_STRING, description='Name of the created rule'),
                    'root_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='ID of the root node of the rule tree'),
                }
            )
        ),
        400: openapi.Response('Bad Request', 
            openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'error': openapi.Schema(type=openapi.TYPE_STRING, description='Error message')
                }
            )
        ),
        500: openapi.Response('Internal server error', 
            openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'error': openapi.Schema(type=openapi.TYPE_STRING, description='Error message')
                }
            )
        )
    }
)
@api_view(['POST'])
def create_rule_view(request):
    rule_string = request.data.get('rule_string')
    rule_name = request.data.get('rule_name', None)

    # Validate input
    if not rule_string:
        return JsonResponse(
            {'error': 'The rule_string is required.'}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    if not isinstance(rule_string, str):
        return JsonResponse(
            {'error': 'The rule_string must be a string.'}, 
            status=status.HTTP_400_BAD_REQUEST
        )

    try:
        # Create the rule and its AST
        rule_root = create_rule(rule_string)

        # Save the rule with the given name
        if rule_name:
            rule_root.rule_name = rule_name
            rule_root.save()

        # Log the created rule details
        print('Rule created:', {
            'rule_id': rule_root.id,
            'rule_name': rule_root.rule_name,
            'root_id': rule_root.rule_root.id
        })

        return JsonResponse(
            {
                'result': f'New rule created with rule id {rule_root.id}',
                'rule_id': rule_root.id, 
                'rule_name': rule_root.rule_name, 
                'root_id': rule_root.rule_root.id
            }, 
            status=status.HTTP_201_CREATED
        )

    except Exception as e:
        # Catch all exceptions and return a 500 error
        print(str(e))
        return JsonResponse(
            {'error': str(e)}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@swagger_auto_schema(
    method='post',
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'rule_strings': openapi.Schema(
                type=openapi.TYPE_ARRAY,
                items=openapi.Schema(type=openapi.TYPE_STRING),
                description='Array of rule strings to be combined (At least 2 rules required)',
                example=["A > 10", "B < 5", "C = 20"]
            ),
            'operators': openapi.Schema(
                type=openapi.TYPE_ARRAY,
                items=openapi.Schema(type=openapi.TYPE_STRING),
                description="Array of operators to combine the rules (Allowed operators: 'AND', 'OR', 'XOR', 'NAND', 'NOR', 'XNOR'). "
                            "The number of operators must be zero or one less than the number of rule strings."
                            "Defaults to 'AND' if empty.",
                example=["AND", "OR"]
            ),
            'combined_rule_name': openapi.Schema(
                type=openapi.TYPE_STRING, 
                description='A unique name to identify the rule',
                example="MASTER_RULE_1"
            )
        },
        required=['rule_strings'],
    ),
    responses={
        201: openapi.Response('Combined rule created successfully',
            openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'combined_rule_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='ID of the combined rule'),
                    'combined_rule_name': openapi.Schema(type=openapi.TYPE_STRING, description='Name of the combined rule'),
                    'combined_root_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='ID of the root node of the rule tree'),
                }
            )
        ),
        400: openapi.Response('Bad Request', 
            openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'error': openapi.Schema(type=openapi.TYPE_STRING, description='Error message')
                }
            )
        ),
        500: openapi.Response('Internal server error', 
            openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'error': openapi.Schema(type=openapi.TYPE_STRING, description='Error message')
                }
            )
        )
    }
)
@api_view(['POST'])
def combine_rules_view(request):
    rule_strings = request.data.get('rule_strings', [])
    operators = request.data.get('operators', [])
    combined_rule_name = request.data.get('combined_rule_name', None)

    # Validate rule_strings
    if not isinstance(rule_strings, list) or len(rule_strings) < 2:
        return JsonResponse(
            {'error': 'At least two rule strings are required.'},
            status=status.HTTP_400_BAD_REQUEST
        )

    # Validate operators
    allowed_operators = {'AND', 'OR', 'XOR', 'NAND', 'NOR', 'XNOR'}
    if not operators:
        # Use 'AND' as the default operator
        operators = ['AND'] * (len(rule_strings) - 1)
    elif not isinstance(operators, list):
        return JsonResponse(
            {'error': 'Operators should be provided as a list.'},
            status=status.HTTP_400_BAD_REQUEST
        )
    elif len(operators) != len(rule_strings) - 1:
        return JsonResponse(
            {'error': f"Number of operators must be zero or one less than the number of rule strings."},
            status=status.HTTP_400_BAD_REQUEST
        )
    else:
        for operator in operators:
            if operator not in allowed_operators:
                return JsonResponse(
                    {'error': f"Invalid operator '{operator}'. Only {allowed_operators} are allowed."},
                    status=status.HTTP_400_BAD_REQUEST
                )

    # Combine the rules
    try:
        combined_ast = combine_rules(rule_strings, operators)

        if combined_rule_name:
            combined_ast.rule_name = combined_rule_name
            combined_ast.save()


        # Log the created rule details
        print('Rule created:', {
        'combined_rule_id': combined_ast.id,
        'combined_rule_name': combined_ast.rule_name,
        'combined_root_id': combined_ast.rule_root.id
        })
        return JsonResponse(
            {
                'result': f'Combined rule created with rule id {combined_ast.id}',
                'combined_rule_id': combined_ast.id,
                'combined_rule_name': combined_ast.rule_name,
                'combined_root_id': combined_ast.rule_root.id
            },

            status=status.HTTP_201_CREATED
        )
    except ValueError as e:
        return JsonResponse(
            {'error': str(e)},
            status=status.HTTP_400_BAD_REQUEST
        )
    except Exception as e:
        return JsonResponse(
            {'error': f"An unexpected error occurred: {str(e)}"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@swagger_auto_schema(
    method='post',
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'rule_id': openapi.Schema(
                type=openapi.TYPE_INTEGER, 
                description='Rule Id'
            ),
            'rule_name': openapi.Schema(
                type=openapi.TYPE_STRING, 
                description='Unique Rule Name'
            ),
            'data': openapi.Schema(
                type=openapi.TYPE_OBJECT,
                additional_properties=openapi.Schema(type=openapi.TYPE_STRING),
                description='Data for rule evaluation'
            )
        },
    ),
    responses={
        200: openapi.Response('Data evaluated successfully', 
            openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'result': openapi.Schema(type=openapi.TYPE_BOOLEAN, description='If the given data qualify the rule or not.'),
                }
            )
        ),
        404: openapi.Response('Rule Not Found', 
            openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'error': openapi.Schema(type=openapi.TYPE_STRING, description='No rule exists with the given details.')
                }
            )
        ),
        400: openapi.Response('Bad Request', 
            openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'error': openapi.Schema(type=openapi.TYPE_STRING, description='Must provide either rule_id or rule_name.')
                }
            )
        ),
        500: openapi.Response('Internal Server Error', 
            openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'error': openapi.Schema(type=openapi.TYPE_STRING, description='Error while evaluating the rule.')
                }
            )
        ),
    }
)
@api_view(['POST'])
def evaluate_rule_view(request):
    rule_id = request.data.get('rule_id', None)
    rule_name = request.data.get('rule_name', None)
    data = request.data.get('data', {})

    if not rule_id and not rule_name:
        return JsonResponse(
            {'error': 'Must provide either rule_id or rule_name'}, 
            status=status.HTTP_400_BAD_REQUEST
        )

    try:
        # Retrieve the Rule object based on rule_id or rule_name
        if rule_id:
            rule = Rule.objects.get(id=rule_id)
        else:
            rule = Rule.objects.get(rule_name=rule_name)

        # Assuming rule_root is a Node that represents the AST
        ast_root = rule.rule_root
        result = evaluate_rule(ast_root, data)

        return JsonResponse(
            {'result': result},
            status=status.HTTP_200_OK
        )

    except Rule.DoesNotExist:
        return JsonResponse(
            {'error': 'Rule not found'}, 
            status=status.HTTP_404_NOT_FOUND
        )
    except RuntimeError as e:
        return JsonResponse(
            {'error': f'Runtime error occurred: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    except NotImplementedError as e:
        return JsonResponse(
            {'error': f'NotImplementedError: {str(e)}'},
            status=status.HTTP_400_BAD_REQUEST
        )
    except Exception as e:
        return JsonResponse(
            {'error': f'An unexpected error occurred: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


def home(req):
    return render(req, 'index.html')