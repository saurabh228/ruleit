# Rule.it

## Project Overview

Rule.it is a Rule Engine Application, designed to determine user/data eligibility based on user defined rules. It employs an Abstract Syntax Tree (AST) to represent conditional rules, allowing for the dynamic creation, combination, and modification of these rules through a simple user interface, API, and backend.

## Table of Contents

1. [Installation Instructions](#installation-instructions)
2. [Usage Instructions](#usage-instructions)
3. [API Documentation](#api-documentation)
4. [Data Structure](#data-structure)
5. [Common Issues](#common-issues)
6. [Design Choices](#design-choices)

## Installation Instructions

The application is structured into a frontend (React.js) and a backend (Django with PostgreSQL) with corresponding Dockerfiles. To set up the application:

1. **Ensure Docker is Installed:**
   - Download and install Docker from [Docker's official website](https://www.docker.com/get-started).

2. **Clone the Repository:**
   ```bash
   git clone https://github.com/saurabh228/ruleit.git
   cd ruleit
   ```

3. **Run Docker Compose:**
   Navigate to the directory containing the `docker-compose.yml` file and run:
   ```bash
   docker-compose up --build
   ```

This command will build the Docker images and start the services defined in the `docker-compose.yml`. This should be enough to get everything running.


## Usage Instructions

1. **Accessing the Application:**
   - Frontend: Open your browser and navigate to `http://localhost:3000`.
   - Backend: API endpoints can be accessed at `http://localhost:8000`.

2. **API Testing:**
   - Visit `http://localhost:8000/swagger` to explore and test all the API endpoints through the Swagger UI.

## API Documentation

### Endpoints

1. **Create Rule**
   - **URL:** `/api/create-rule/`
   - **Method:** `POST`
   - **Request Body:**
     ```json
     {
       "rule_string": "A > 10 AND color = yellow",
       "rule_name": "Rule_01"
     }
     ```
   - **Responses:**
     - **201:** Rule created successfully
     - **400:** Bad Request
     - **500:** Internal Server Error

2. **Combine Rules**
   - **URL:** `/api/combine-rules/`
   - **Method:** `POST`
   - **Request Body:**
     ```json
     {
       "rule_strings": ["A > 10", "B < 5"],
       "operators": ["AND"],
       "combined_rule_name": "MASTER_RULE_1"
     }
     ```
   - **Responses:**
     - **201:** Combined rule created successfully
     - **400:** Bad Request
     - **500:** Internal Server Error

3. **Evaluate Rule**
   - **URL:** `/api/evaluate-rule/`
   - **Method:** `POST`
   - **Request Body:**
     ```json
     {
       "rule_id": 1,
       "rule_name": "Rule_01",
       "data": {"A": 15, "color": "yellow"}
     }
     ```
   - **Responses:**
     - **200:** Data evaluated successfully
     - **400:** Bad Request
     - **404:** Rule Not Found
     - **500:** Internal Server Error

4. **Get Rules**
   - **URL:** `/api/get-rules/`
   - **Method:** `GET`
   - **Responses:**
     - **200:** List of rules
     - **400:** Bad Request
     - **500:** Internal Server Error

5. **Get Rule by ID**
   - **URL:** `/api/get-rule/<rule_id>/`
   - **Method:** `GET`
   - **Responses:**
     - **200:** Rule details
     - **404:** Rule Not Found
     - **500:** Internal Server Error

6. **Edit Rule**
   - **URL:** `/api/edit-rule/`
   - **Method:** `POST`
   - **Request Body:**
     ```json
     {
       "rule_string": "A > 20 AND color = red",
       "rule_id": "2"
     }
     ```
   - **Responses:**
     - **201:** Rule Edited successfully
     - **400:** Bad Request
     - **500:** Internal Server Error


## Data Structure

### Models Overview

This application employs two primary models: `Node` and `Rule`. The `Node` model represents individual components of a rule's abstract syntax tree (AST), while the `Rule` model encapsulates the rule's metadata and its root node.

### Node Model

The `Node` model defines the structure of the nodes in the AST, which can be of three types: operator, variable, or literal. It allows for recursive relationships, enabling complex rule definitions.

#### Fields:
- **node_type** (`CharField`): Specifies the type of node (choices: operator, variable, literal).
- **left** (`ForeignKey`): A self-referential link to the left child node representing the operand/operator to the left.
- **right** (`ForeignKey`): A link to the right child node. the right operand/operator.
- **value** (`CharField`): The value associated with the node (e.g., the operator, variable name or value).

#### Validation:
- The `clean` method ensures that operator nodes have both left and right children, raising a `ValidationError` if this condition is not met.

### Rule Model

The `Rule` model encapsulates the details of a specific rule, linking it to its root node in the AST.

#### Fields:
- **rule_name** (`CharField`): The name of the rule, which must be unique.
- **rule_root** (`OneToOneField`): A relationship linking to the root `Node` of the rule's AST.
- **rule_tokens** (`ArrayField`): An array of strings representing the tokenized version of the rule string, aiming for easier manipulation.


This structure allows for the dynamic and flexible representation of rules, enabling the application to evaluate and manipulate them effectively.

## Common Issues

1. **Port Conflicts:**
   - Ensure that the ports defined in the `docker-compose.yml` file are free on your machine. If not, change the port mappings.

2. **Database Connection Issues:**
   - Check the database configurations in the `docker-compose.yml` to ensure the credentials match what your application expects.

3. **Dependency Errors:**
   - Ensure all required libraries and dependencies are installed. This is usually handled by Docker, but verify if running in a local environment.

## Design Choices

### Framework and Architecture
- **Django (Backend)**: Chosen for its scalability, and ease of use. Django’s built-in ORM simplifies database management, additionally, it provides a high level of abstraction reducing the complexity of backend development.
  
- **Django REST Framework**: Used in conjunction with Django to provide a powerful and flexible toolkit for building RESTful APIs. It simplifies serialization, authentication, and viewsets, and supports the rapid development and testing of APIs.

- **React (Frontend)**: React was selected for its component-based architecture, which allows for building dynamic and responsive user interfaces easily. It enables the modular development of UI elements, enhancing reusability and maintainability of the frontend codebase.

### API Documentation
- **Swagger**: Integrated with DRF for automatic generation of interactive API documentation. It simplifies the process of testing API endpoints, and ensures that the API is well-documented, making it easier to maintain and scale.
  
### Database Management
- **PostgreSQL**: Selected for its robustness and ability to handle complex data types. Its support for the `ArrayField` is particularly useful for storing tokenized rule strings.

### Data Structure Design
- **Abstract Syntax Tree (AST)**: Implementing AST allows for a clear, hierarchical representation of conditional rules. This design enables easy manipulation, evaluation, and combination of rules based on user-defined conditions.

### Tokenization & Postfix conversion
- **Rule Tokenization**: Tokenizing rules into array of individual tokens. To ensure the efficient parsing and processing of rule strings.
- **Postfix Conversion of Rule**: Building AST from a postfix notation is a lot easier than infix representation. Mailnly because of its lack of parenthesis and implicit handling of operator precedences.

### Error Handling
- **Try & Except**: Exception handling is done throught the project to maintain the stability of the program by gracefully managing runtime errors reducing the possibility of application crash.

### Scalability and Extensibility
- **Modular Design**: The separation of frontend (React) and backend (Django) ensures that both can be scaled independently. This architecture also supports the easy addition of new features, whether they are frontend components or backend rule-processing logic.
  
- **Future-Proof Data Structure**: The AST-based rule engine is designed to be extendable. It can accommodate new node types, additional operators, or changes to the rule evaluation logic without requiring a complete overhaul.

### Containerization
- **Docker**: Docker is used to containerize the application, providing consistent environments for both development and production. This ensures that dependencies are properly managed and the application can run seamlessly across various systems.

## Feel free to try the project and suggest any improvements.
