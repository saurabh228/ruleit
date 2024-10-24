from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Rule, Node
from rest_framework.test import APIClient

class RuleTests(APITestCase):

    @classmethod
    def setUpTestData(cls):

        client = APIClient()

        # Creating a root node
        url = reverse('create_rule')  # Ensure this URL exists in your routes
        data = {
            'rule_name': 'testrule',
            'rule_string': 'a > b'
        }
        url = reverse('create_rule')
        response = client.post(url, data, format='json')
        if response.status_code != status.HTTP_201_CREATED:
            print("Error creating rule")
            print(response.json())
        else:
            response_data = response.json()
            # print(response_data)
            cls.rule_id = response_data['rule_id']
            cls.rule = Rule.objects.get(id=cls.rule_id)


        # Creating a combined rule
        url = reverse('combine_rules')  # Ensure this URL exists in your routes
        data = {
            'combined_rule_name': 'cmb_rl',
            'rule_strings': ["((age > 30 AND department = 'Sales') OR (age < 25 AND department = 'Marketing')) AND (salary > 50000 OR experience > 5)",
                             "((age > 20 AND department = 'Marketing')) AND (salary > 20000 OR experience < 5)"]
        }
        response = client.post(url, data, format='json')
        # print(response.json())
        if response.status_code != status.HTTP_201_CREATED:
            print("Error creating combined rule")
            print(response.json())
        else: 
            response_data = response.json()
            cls.combined_rule_id = response_data['rule_id']

    def test_get_all_rules(self):
        # Testing the API to get all rules
        url = reverse('get_rules')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(len(response.json()), 0)

    def test_get_rule_by_id(self):
        # Get the rule ID dynamically after creation
        rule_id = self.rule_id

        # Fetching rule by ID
        url = reverse('get_rule_by_id', args=[rule_id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data = response.json()
        self.assertEqual(response_data['rule_name'], 'testrule')


    def test_combined_rule_valid_data(self):
        data = {
            'rule_id': self.combined_rule_id,
            'data': {
                'age': 24,
                'department': 'Marketing',
                'salary': 60000,
                'experience': 6
            }
        }
        url = reverse('evaluate_rule')
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        result = response.json().get('result')
        self.assertTrue(result, "Expected True for this data since it satisfies the rule")

    def test_combined_rule_invalid_data(self):
        data = {
            'rule_id': self.combined_rule_id,
            'data': {
                'age': 40,
                'department': 'HR',
                'salary': 15000,
                'experience': 2
            }
        }
        url = reverse('evaluate_rule')
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        result = response.json().get('result')
        self.assertFalse(result, "Expected False for this data since it doesn't satisfy either rule")

    def test_combined_rule_first_rule_valid(self):
        data = {
            'rule_id': self.combined_rule_id,
            'data': {
                'age': 38,
                'department': 'Sales',
                'salary': 55000,
                'experience': 4
            }
        }
        url = reverse('evaluate_rule')
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        result = response.json().get('result')
        self.assertFalse(result, "Expected False since only the first rule is satisfied but not the second")

    def test_combined_rule_second_rule_valid(self):
        data = {
            'rule_id': self.combined_rule_id,
            'data': {
                'age': 28,
                'department': 'Marketing',
                'salary': 22000,
                'experience': 2
            }
        }
        url = reverse('evaluate_rule')
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        result = response.json().get('result')
        self.assertFalse(result, "Expected False since the data only satisfies the second rule")

    def test_combined_rule_incomplete_data(self):
        data = {
            'rule_id': self.combined_rule_id,
            'data': {
                'age': 40,
                'department': 'Sales'
                # Missing salary and experience
            }
        }
        url = reverse('evaluate_rule')
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        result = response.json().get('result')
        print(result)
        self.assertFalse(result, "Expected False for incomplete data, as it can not pass the rule")


