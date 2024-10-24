# utils.py
import re
from django.db import transaction
from django.core.exceptions import ValidationError
from .models import Node, Rule

# A simple class to represent a node structure for comparison
class NodeKey:
    def __init__(self, node_type, value, left=None, right=None):
        self.node_type = node_type
        self.value = value
        self.left = left
        self.right = right

    def __hash__(self):
        lft = self.left.id if self.left else None
        rht = self.right.id if self.right else None
        return hash((self.node_type, self.value, lft, rht))

    def __eq__(self, other):
        return (
            self.node_type == other.node_type and
            self.value == other.value and
            self.left == other.left and
            self.right == other.right
        )


# Operator precedence
PRECEDENCE = {
    'AND': 1,
    'OR': 1,
    'XOR': 1,
    'NAND': 2, 
    'NOR': 2, 
    'XNOR': 2,
    '>': 3,
    '>=': 3,
    '<': 3,
    '<=': 3,
    '=': 3,
    '==':3,
    '!=': 3,
    '+': 4,
    '-': 4,
    '*': 5,
    '/': 5,
    '%': 5,
}

def tokenize(rule_string):
    """
    Tokenizes the input rule string.
    """
    # Regex to handle string literals and other tokens
    pattern = r'\"[^\"]*\"|\'[^\']*\'|AND|OR|XOR|NAND|NOR|XNOR|>=|<=|!=|==|=|>|<|\+|\-|\*|/|%|\(|\)|[a-zA-Z0-9_][\w]*'

    # Find all matching tokens
    tokens = re.findall(pattern, rule_string)
    return [token for token in tokens if token]

def infix_to_postfix(tokens):
    """
    Converts infix tokens to postfix notation using the Shunting Yard algorithm.
    
    Args:
        tokens (list): A list of tokens in infix notation.
    
    Returns:
        list: A list of tokens in postfix notation.
    
    Raises:
        ValueError: If there are any syntax errors in the expression.
    """
    output = []
    operator_stack = []

    # Check for empty input
    if not tokens:
        raise ValueError("No tokens provided for conversion.")

    # Ensure matching parentheses
    open_parentheses = 0

    for token in tokens:
        if token not in PRECEDENCE and (token != '(' and token != ')'):  # If the token is an operand
            output.append(token)

        elif token == '(':
            operator_stack.append(token)
            open_parentheses += 1
            
        elif token == ')':
            if open_parentheses == 0:
                raise ValueError("Mismatched parentheses: extra closing parenthesis.")
            while operator_stack and operator_stack[-1] != '(':
                output.append(operator_stack.pop())
            if operator_stack: 
                operator_stack.pop()  # Pop the '(' from the stack
                open_parentheses -= 1

        else:  # If the token is an operator
            while (operator_stack and operator_stack[-1] != '(' and
                   PRECEDENCE[operator_stack[-1]] >= PRECEDENCE[token]):
                output.append(operator_stack.pop())
            operator_stack.append(token)

    # Pop all the operators left in the stack
    while operator_stack:
        top_token = operator_stack.pop()
        if top_token == '(':
            raise ValueError("Mismatched parentheses: extra opening parenthesis.")
        output.append(top_token)

    if open_parentheses > 0:
        raise ValueError("Mismatched parentheses: unmatched opening parenthesis.")

    return output

def is_number(s):
    try:
        float(s)  # Try to convert to float
        return True
    except ValueError:
        return False


def create_rule(rule_string, rule_name):
    """
    Create a tree from a rule string in postfix notation and save it to the database.

    Parameters:
    rule_string (str): The rule string to be processed.

    Returns:
    Rule: The created rule instance if successful.

    Raises:
    ValueError: If the rule_string is empty or invalid.
    """

    # Validate the rule string
    if not rule_string:
        raise ValueError("Rule string cannot be empty.")

    # Tokenize and convert the rule string to postfix notation
    try:
        rule_tokens = tokenize(rule_string)
        postfix_tokens = infix_to_postfix(rule_tokens)
        # print("tokens: ",postfix_tokens)
    except Exception as e:
        raise ValueError(f"Error while processing rule string: {str(e)}")

    stack = []
    node_cache = {}

    # Build the tree from postfix tokens
    for token in postfix_tokens:
        if token not in PRECEDENCE:  # Operand

            # Find out if the token is a literal or a variable
            node_type = 'literal' if token.startswith('"') or token.startswith("'") or is_number(token) else 'variable'

            # Create a unique key for the node
            key = NodeKey(node_type=node_type, value=token.strip('"\''))
            # Check if the node already exists
            if key in node_cache:
                stack.append(node_cache[key])
            else:
                node = Node(node_type=node_type, value=token.strip('"\''))
                node.save()
                node_cache[key] = node
                stack.append(node)
        else:  # Operator
            try:
                right_node = stack.pop()
                left_node = stack.pop()
            except IndexError:
                raise ValueError("Invalid rule string: insufficient operands for operators.")

            key = NodeKey(node_type='operator', value=token, left=left_node, right=right_node)

            # Check if the node already exists
            if key in node_cache:
                stack.append(node_cache[key])
            else:
                operator_node = Node(node_type='operator', value=token, left=left_node, right=right_node)
                operator_node.save()
                node_cache[key] = operator_node
                stack.append(operator_node)

    # Ensure that the stack contains the root node
    if len(stack) != 1:
        # print("stack:", stack)
        raise ValueError("Invalid rule string: tree structure could not be formed.")

    # Create the rule in a transaction
    try:
        with transaction.atomic():
            rule = Rule.objects.create(rule_root=stack[0])
            rule.rule_tokens = rule_tokens
            rule.rule_name = rule_name
            rule.save()
    except ValidationError as e:
        raise ValueError(f"Failed to save rule to the database: {str(e)}")

    return rule

def combine_rules(combined_rule_name, rule_strings, operators):
    """
    Combines multiple rule strings into a single AST based on the provided operators.

    :param rule_strings: List of rule strings.

    :param operators: List of operators to combine the rules. If no operators, default to AND.

    :return: Combined AST root or raises ValueError for invalid input.
    """
    
    # Validate input
    if len(operators) != 0 and len(operators) != len(rule_strings) - 1:
        raise ValueError("Number of operators must be zero or one less than the number of rule strings.")


    # Tokenize all rules
    combined_rules = f"({rule_strings[0]})"
    
    for i in range(1,len(rule_strings)):
        combined_rules += f" {operators[i-1]} ({rule_strings[i]})"


    # Create the combined rule AST
    combined_rule_root = create_rule(combined_rules, combined_rule_name)

    return combined_rule_root

def evaluate_rule(ast_root, data):
    """
    Recursively evaluates the AST (abstract syntax tree) rooted at ast_root based on the provided data.
    
    Args:
        ast_root (Node): The root node of the rule AST.
        data (dict): A dictionary containing variable names and their values.
    
    Returns:
        bool or float: The result of evaluating the rule, which could be a boolean or a numeric value.
    
    Raises:
        ValueError: If an operation cannot be performed due to missing data or invalid operations.
    """
    if ast_root is None:
        raise RuntimeError("Invalid tree structure.")

    # Handle node types: literal, variable, operator
    if ast_root.node_type == 'literal':
        # Return the literal as-is, it's a constant value
        return ast_root.value

    elif ast_root.node_type == 'variable':
        # Look up the variable in the data
        return data.get(ast_root.value, None)

    elif ast_root.node_type == 'operator':

        # Convert left and right values to boolean values for logical operations
        def to_bool(val):
            try:
                return bool(val)
            except ValueError:
                raise ValueError(f"Cannot convert '{val}' to a boolean value.")


        # Handle logical operators
        if ast_root.value == 'AND':
            left_value = evaluate_rule(ast_root.left, data)
            if left_value == None: return None

            if not to_bool(left_value): 
                # print(f"operator: {ast_root.value}, returned: False")
                return False
            right_value = evaluate_rule(ast_root.right, data)
            if right_value == None: return None
            # print(f"operator: {ast_root.value}, returned: {to_bool(right_value)}")
            return to_bool(right_value)

        elif ast_root.value == 'OR':
            left_value = evaluate_rule(ast_root.left, data)
            if left_value == None: return None
            if to_bool(left_value): 
                # print(f"operator: {ast_root.value}, returned: {to_bool(left_value)}")
                return True
            right_value = evaluate_rule(ast_root.right, data)
            if right_value == None: return None
            # print(f"operator: {ast_root.value}, returned: {to_bool(right_value)}")
            return to_bool(right_value)
        
        elif ast_root.value == 'XOR':
            left_value = evaluate_rule(ast_root.left, data)
            right_value = evaluate_rule(ast_root.right, data)
            if left_value == None or right_value == None: return None
            return to_bool(left_value) != to_bool(right_value)



        # Evaluate the left and right subtrees for operators
        left_value = evaluate_rule(ast_root.left, data)
        right_value = evaluate_rule(ast_root.right, data)

        # print(f"op: {ast_root.value}, left: {left_value}, right: {right_value}")

        if left_value == None or right_value == None: return None

        # Convert left and right values to float for arithmetic comparisons if needed
        def to_float(val):
            try:
                return float(val)
            except ValueError:
                raise ValueError(f"Cannot convert '{val}' to a numeric value.")

        # Handle operators based on their type
        if ast_root.value == '>':
            return to_float(left_value) > to_float(right_value)
        elif ast_root.value == '<':
            return to_float(left_value) < to_float(right_value)
        elif ast_root.value == '>=':
            return to_float(left_value) >= to_float(right_value)
        elif ast_root.value == '<=':
            return to_float(left_value) <= to_float(right_value)
        elif ast_root.value == '=' or ast_root.value == '==':
            if is_number(left_value) and is_number(right_value):
                return float(left_value) == float(right_value)
            return left_value == right_value
        elif ast_root.value == '!=':
            if is_number(left_value) and is_number(right_value):
                return float(left_value) != float(right_value)
            return left_value != right_value

        # Handle arithmetic operators
        elif ast_root.value == '+':
            return to_float(left_value) + to_float(right_value)
        elif ast_root.value == '-':
            return to_float(left_value) - to_float(right_value)
        elif ast_root.value == '*':
            return to_float(left_value) * to_float(right_value)
        elif ast_root.value == '/':
            if to_float(right_value) == 0:
                raise ValueError("Division by zero is not allowed.")
            return to_float(left_value) / to_float(right_value)
        elif ast_root.value == '%':
            if to_float(right_value) == 0:
                raise ValueError("Modulo by zero is not allowed.")
            return to_float(left_value) % to_float(right_value)


        # Handle unsupported operators
        else:
            raise NotImplementedError(f"Unsupported operator '{ast_root.value}' encountered.")

    # If none of the cases match, raise an error
    raise Exception("unknown error occurred.")

def edit_rule(rule_string, rule_id):
    """
    Create a tree from a rule string in postfix notation and save it to the database.

    Parameters:
    rule_string (str): The rule string to be processed.

    Returns:
    Rule: The created rule instance if successful.

    Raises:
    ValueError: If the rule_string is empty or invalid.
    """

    # Validate the rule string
    if not rule_string:
        raise ValueError("Rule string cannot be empty.")

    # Tokenize and convert the rule string to postfix notation
    try:
        rule_tokens = tokenize(rule_string)
        postfix_tokens = infix_to_postfix(rule_tokens)
        # print("tokens: ",postfix_tokens)
    except Exception as e:
        raise ValueError(f"Error while processing rule string: {str(e)}")

    stack = []
    node_cache = {}

    # Build the tree from postfix tokens
    for token in postfix_tokens:
        if token not in PRECEDENCE:  # Operand

            # Find out if the token is a literal or a variable
            node_type = 'literal' if token.startswith('"') or token.startswith("'") or is_number(token) else 'variable'

            # Create a unique key for the node
            key = NodeKey(node_type=node_type, value=token.strip('"\''))
            # Check if the node already exists
            if key in node_cache:
                stack.append(node_cache[key])
            else:
                node = Node(node_type=node_type, value=token.strip('"\''))
                node.save()
                node_cache[key] = node
                stack.append(node)
        else:  # Operator
            try:
                right_node = stack.pop()
                left_node = stack.pop()
            except IndexError:
                raise ValueError("Invalid rule string: insufficient operands for operators.")

            key = NodeKey(node_type='operator', value=token, left=left_node, right=right_node)

            # Check if the node already exists
            if key in node_cache:
                stack.append(node_cache[key])
            else:
                operator_node = Node(node_type='operator', value=token, left=left_node, right=right_node)
                operator_node.save()
                node_cache[key] = operator_node
                stack.append(operator_node)

    # Ensure that the stack contains the root node
    if len(stack) != 1:
        # print("stack:", stack)
        raise ValueError("Invalid rule string: tree structure could not be formed.")

    # Create the rule in a transaction
    try:
        with transaction.atomic():
            rule = Rule.objects.get(id=rule_id)
            rule.rule_tokens = rule_tokens
            rule.rule_root = stack[0]
            rule.save()
    except ValidationError as e:
        raise ValueError(f"Failed to save rule to the database: {str(e)}")

    return rule
