# def test_user_creation(client):
#     url = reverse('user-list')  # пример URL
#     data = {'username': 'newuser', 'password': 'password'}
#     response = client.post(url, data, format='json')
#     assert response.status_code == 201
#     assert response.data['username'] == 'newuser'