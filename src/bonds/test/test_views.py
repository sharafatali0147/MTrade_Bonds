from django.urls import reverse
from nose.tools import ok_, eq_
from rest_framework.test import APITestCase
from rest_framework import status
from src.users.test.factories import UserFactory
from ..models import Bonds

class TestCreateBonds(APITestCase):
    """
    Tests /Create Bonds detail operations.
    """

    def setUp(self):
        self.url_bond = reverse('bonds_create')
        self.url_bonds_list = reverse('bonds_list')
        self.samle_bond = {"bond_name": "string", "number_of_bonds": 12, "selling_price_mxn": 12}
        self.user = UserFactory()
        tokens = self.user.get_tokens()
        access_token = tokens['access']
        self.url = reverse('user-detail', kwargs={'pk': self.user.pk})
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')

    def test_get_request_returns_a_given_user(self):
        response = self.client.get(self.url)
        eq_(response.status_code, status.HTTP_200_OK)

    def test_bonds_create_with_no_data_fails(self):
        response = self.client.post(self.url_bond, {})
        eq_(response.status_code, status.HTTP_400_BAD_REQUEST)
        
    def test_bonds_create_with_valid_data_succeeds(self):
        response = self.client.post(self.url_bond, self.samle_bond)
        eq_(response.status_code, status.HTTP_201_CREATED)
        eq_(response.data['bond_name'], self.samle_bond.get('bond_name'))
        eq_(response.data['number_of_bonds'], self.samle_bond.get('number_of_bonds'))
        eq_(response.data['selling_price_mxn'], self.samle_bond.get('selling_price_mxn'))
        
    
    def test_bonds_create_with_number_of_bonds_error(self):
        samle_bond = {"bond_name": "string", "number_of_bonds": 0, "selling_price_mxn": 12}
        response = self.client.post(self.url_bond, samle_bond)
        eq_(response.status_code, status.HTTP_400_BAD_REQUEST)
        eq_(response.data['number_of_bonds'], ["Ensure this value is greater than or equal to 1."])
    
    def test_bonds_create_with_number_of_bonds_error_01(self):
        samle_bond = {"bond_name": "string", "number_of_bonds": 10001, "selling_price_mxn": 12}
        response = self.client.post(self.url_bond, samle_bond)
        eq_(response.status_code, status.HTTP_400_BAD_REQUEST)
        eq_(response.data['number_of_bonds'], ["Ensure this value is less than or equal to 10000."])
    
    def test_bonds_create_with_selling_price_mxn_error(self):
        samle_bond = {"bond_name": "string", "number_of_bonds": 1001, "selling_price_mxn": -12}
        response = self.client.post(self.url_bond, samle_bond)
        eq_(response.status_code, status.HTTP_400_BAD_REQUEST)
        eq_(response.data['selling_price_mxn'], ["Ensure this value is greater than or equal to 0.0."])

    def test_bonds_create_with_selling_price_mxn_error_01(self):
        samle_bond = {"bond_name": "string", "number_of_bonds": 1001, "selling_price_mxn": 100000000.0001}
        response = self.client.post(self.url_bond, samle_bond)
        eq_(response.status_code, status.HTTP_400_BAD_REQUEST)
        eq_(response.data['selling_price_mxn'], ["Ensure this value is less than or equal to 100000000.0."])
    
    def test_bonds_create_with_selling_price_mxn(self):
        samle_bond = {"bond_name": "string", "number_of_bonds": 1001, "selling_price_mxn": 1005.125825}
        response = self.client.post(self.url_bond, samle_bond)
        eq_(response.status_code, status.HTTP_201_CREATED)
        eq_(response.data['selling_price_mxn'], 1005.1258)
    

class TestBonds(APITestCase):
    """
    Tests /Bonds detail operations.
    """

    def setUp(self):
        self.url_bonds_list = reverse('bonds_list')
        self.url_bond = reverse('bonds_create')
        self.samle_bond = {"bond_name": "string", "number_of_bonds": 12, "selling_price_mxn": 12}
        self.user = UserFactory()
        tokens = self.user.get_tokens()
        access_token = tokens['access']
        self.url = reverse('user-detail', kwargs={'pk': self.user.pk})
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')

    def test_get_request_returns_a_given_user(self):
        response = self.client.get(self.url)
        eq_(response.status_code, status.HTTP_200_OK)

    def test_get_all_bonds_succeeds(self):
        create_response = self.client.post(self.url_bond, self.samle_bond)
        response = self.client.get(self.url_bonds_list)
        eq_(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.json()['Bonds'], list)
        ok_(response.json()['Bonds'][0]['id'])
        eq_(response.json()['Bonds'][0]['bond_name'], create_response.data['bond_name'])
