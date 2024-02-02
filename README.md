# Music-Platform-project

## Task 6

#### 1- In the users app, extend Django's user model by inheriting from AbstractUser to include an optional bio CharField with a max length of 256 characters
##### *users.models.py*
```python
from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    bio = models.CharField(max_length=256 , blank=True)

    def __str__(self): 
        return self.username
```

#### 2- In the authentication app, support a POST authentication/register/ endpoint that creates users.
 ##### *authentication.views.py*
```python
class RegisterAPI(APIView):
    
    def post(self, request, *args, **kwargs):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
        
            return Response(data={
                "user": UserSerializer(user).data,
                "token": AuthToken.objects.create(user)[1]
            }, status=HTTP_201_CREATED)

        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

```
![Alt](https://github.com/abood-74/Music-Platform-project/blob/Task-6/readme_elements/Screenshot%20from%202024-02-02%2008-16-34.png)

* This endpoint must accept the following fields formatted in JSON username, email, password1, password2 (confirmation of password1 )
  ##### *authentication.serializers.py*
```python
class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True)
    password1 = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'bio', 'email', 'password', 'password1']
        extra_kwargs = {'password': {'write_only': True}}
#.......

```
* Perform proper validation  if password1 doesn't match password2.
##### *authentication.serializers.py*
 ```python
def create(self, validated_data):
        if validated_data['password'] == validated_data['password1']:
            user = User.objects.create_user(
                username=validated_data['username'],
                email=validated_data['email'],
                password=validated_data['password']
            )
            return user
        raise serializers.ValidationError("passwords doesn't match")

```
#### 3- Create a POST authentication/login/ that logs in users using their username and password and returns a KnoxToken and the user's data in a nested object.
##### *authentication.serializers.py*
```python
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Incorrect Credentials")
```
##### *authentication.views.py*
```python
class LoginAPI(APIView):
    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data
            return Response(data={
                "user": UserSerializer(user).data,
                "token": AuthToken.objects.create(user)[1]
            }, status=HTTP_200_OK)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
```
![Alt](https://github.com/abood-74/Music-Platform-project/blob/Task-6/readme_elements/Screenshot%20from%202024-02-02%2008-16-23.png)

#### 4- Create a POST authentication/logout/ endpoint that logs the user out from the app by invalidating the knox token
##### *authentication.urls.py*
```python
from django.urls import path
from knox import views as knox_views
from .views import *

urlpatterns = [
    path('/login/', LoginAPI.as_view(), name='signin'),
     path('/logout/', knox_views.LogoutAllView.as_view(), name='knox_logout'),
    path('/register/', RegisterAPI.as_view(), name='register'),
    
]

```

#### 5- In the users app, create a user detail endpoint /users/<pk> that supports the following requests:
* GET returns the user data matching the given pk , namely, it should return the user's id , username , email ,and bio .
###### *users.views.py*
```python
class UserDetailView(APIView):
    def get_object(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            return None

    def get(self, request, pk, format=None):
        user = self.get_object(pk)
        if user is not None:
            serializer = UserSerializer(user)
            return Response(serializer.data)
        return Response(status=status.HTTP_404_NOT_FOUND)

#.....

```
* PUT This is exactly the same as when creating a user except that an ID of an existing user is provided in the URL, and that the request will overwrite the user's data with that given ID.
  ###### *users.views.py*

```python
class UserDetailView(APIView):
    def get_object(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            return None

    def put(self, request, pk, format=None):
        user = self.get_object(pk)
        if user is not None and request.user == user:
            serializer = UserSerializer(user, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({'error': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)

#.....
```
* PATCH This is exactly the same as when updating a user except none of the fields are required, and that only fields given a value will be updated. (hint: see partial_update in serializers)
  ###### *users.views.py*

```python
class UserDetailView(APIView):
    def get_object(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            return None

    def patch(self, request, pk, format=None):
        user = self.get_object(pk)
        if user is not None and request.user == user:
            serializer = UserSerializer(user, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({'error': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)


#.....
```
![Alt](https://github.com/abood-74/Music-Platform-project/blob/Task-6/readme_elements/Screenshot%20from%202024-02-02%2008-16-48.png)



