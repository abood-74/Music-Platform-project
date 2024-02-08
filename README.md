# Music-Platform-project

## Task 7 pytest



#### 1- Create a global fixture auth_client that returns a function, if that function is passed a user instance, it'll return aninstance of DRF's APIClient authenticated by that user instance, otherwise, it'll return an instance of APIClient authenticated by an arbitrary user instance. 
##### *conftest.py*
```python
@pytest.fixture
@pytest.mark.django_db
def auth_client(user = None):
    client = APIClient()
    if user:
        client.force_authenticate(user = user)
    else:
        random_user = User.objects.create_user(username = 'random_user', email = '' , password = 'random_password')
        client.force_authenticate(user = random_user)

    return client
```

#### 2- For each endpoint, test the following: 
* If the view has permission classes, test making requests that will obey and disobey the permissions, For example,if a view has IsAuthenticatedOrReadOnly permission class, test that making a write and non authenticated request will return 403 Forbidden status code
* If the view is expecting a certain set of required fields, test that making a request with one or more missing fields will return 400 status code and a proper error message.
 ##### *albums.tests.test_endpoints.py*
```python

def test_get_albums_with_authnticated_user(auth_client):
    response = auth_client.get(reverse('create_album'))
    assert response.status_code == 200

def test_get_albums_without_authnticated_user():
    client = APIClient()
    response = client.get(reverse('create_album'))
    assert response.status_code == 401
    assert response.json() == {'detail': 'Authentication credentials were not provided.'}
    
    
def test_create_album_with_authnticated_user(auth_client):
    artist = Artist.objects.create(stage_name = 'random_artist')
    data = {
    'name': 'random_album',
    'artist': artist.id,
    'cost': '1000.00',
    'release_datetime': '2025-02-13',  
}
    response = auth_client.post(reverse('create_album'), data = data)
    assert response.status_code == 201

def test_create_album_without_authnticated_user():
    client = APIClient()
    artist = Artist.objects.create(stage_name = 'random_artist')
    data = {
    'name': 'random_album',
    'artist': artist.id,
    'cost': '1000.00',
    'release_datetime': '2025-02-13',  
}
    response = client.post(reverse('create_album'), data = data)
    assert response.status_code == 401
    assert response.json() == {'detail': 'Authentication credentials were not provided.'}    
    
    
def test_create_album_without_name(auth_client):
    artist = Artist.objects.create(stage_name = 'random_artist')
    data = {
    'artist': artist.id,
    'cost': '1000.00',
    'release_datetime': '2025-02-13',  
}
    response = auth_client.post(reverse('create_album'), data = data)
    assert response.status_code == 400
    assert response.json() == {'name': ['This field is required.']}
    

def test_create_album_without_artist(auth_client):
    data = {
    'name': 'random_album',
    'cost': '1000.00',
    'release_datetime': '2025-02-13',  
}
    response = auth_client.post(reverse('create_album'), data = data)
    assert response.status_code == 400
    assert response.json() == {'artist': ['This field is required.']}
    
    
def test_create_album_without_release_datetime(auth_client):
    artist = Artist.objects.create(stage_name = 'random_artist')
    data = {
    'name': 'random_album',
    'artist': artist.id,
    'cost': '1000.00',
}
    response = auth_client.post(reverse('create_album'), data = data)
    assert response.status_code == 400
    assert response.json() == {'release_datetime': ['This field is required.']} 
```


#### all other apps has similar tests in app.tests.test_endpoints.py


    


