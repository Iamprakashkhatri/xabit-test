from django.shortcuts import render

# Create your views here.


# class UpdateCustomerProfileTest(TestCase):
#     """Test module for UPDATE customer profile API"""

#     def setUp(self):
#         url = reverse('user:register')
#         self.register_response = self.client.post(
#             url, {"first_name":"Anish","last_name":"Shrestha","phone_number": "+9779860837177", "password": "test1234","confirm_password":"test1234"}, format="json"
#         )
#         # breakpoint()
#         self.user = User.objects.get(
#             username=self.register_response.data['user']['username'],
#             first_name='Anish',  
#             phone_number='9860837177'
#             )


#         client.force_login(self.user)
        

#         self.valid_payload={
#             'username':self.register_response.data['user']['username'],
#             'first_name': 'Saroj',
#             'last_name':'Shrestha',
#             'phone_number':'9818120333',
#             "customer": {
#                 "gender": "Female",
#                         }
#         }

#         self.invalid_payload={
#             'first_name': '',
#             'last_name':'',
#         }


#     def test_valid_update_customer_profile_with_pk(self):
#         response = client.put(
#             reverse('customer:customer-profile-detail', kwargs={'pk':self.register_response.data['user']['username']}),
#             data=json.dumps(self.valid_payload),
#             content_type='application/json',
#         )
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(response.data['data']['first_name'], 'Saroj')
#         self.assertEqual(response.data['data']['last_name'],'Shrestha')
#         self.assertEqual(response.data['data']['phone_number'],'+9779818120333')

#     def test_invalid_update_customer_profile_with_pk(self):
#         response = client.put(
#             reverse('customer:customer-profile-detail', kwargs={'pk': self.register_response.data['user']['username']}),
#             data=json.dumps(self.invalid_payload),
#             content_type='application/json',
#         )
#         self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

