from django.shortcuts import render
from rest_framework import viewsets

#this file is used to create views for the Django's APIview
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework import filters
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.permissions import IsAuthenticated

from . import serializers
from . import models
from . import permissions
#status contains a detailed list of HTTP RESPONSE CODES
#To whom it may concern the methods here GET, POST, PUT, PATCH, DELETE basically return what a message of what thier function is in the APIView :)
# Create your views here.
class HelloApiView(APIView):
    """Test the API View"""
    #Tell django the serializer we will use to ...
    serializer_class = serializers.HelloSerializer
    #get is used to get a list from a specific function or an API 
    def get(self , request , format=None):
        """Returns a list of APIView features"""
        an_apiview = [
            'Uses HTTP methods as function (get, post, patch, delete)',
            'It is similar to a traditional Django View',
            'Gives you the most control over your logic',
            'It is mapped manually to URLS'
        ]
        return Response({'message':'Hello @CodeDrillz','an_apiview':an_apiview})
    
    def post(self,request):
        """Create a Hello Message with CodeDrillz"""
        serializer = serializers.HelloSerializer(data=request.data)
        #then validate the data passed into the function above 
        if serializer.is_valid():
            name = serializer.data.get('name')
            message = 'Hello {0}'.format(name)
            return Response({'message':message})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    def put(self, request, pk=None):
        """Handles updating an object"""
        #pK above stands for primary of the object from the database
        return Response({'method':'put'})
    
    def patch(self,request,pk=None):
        """Patch request, only updates fields provided in the request"""
        return Response({'method':'patch'})
    
    def delete(self,request,pk=None):
        """Deletes an Object"""
        return Response({'method':'delete'})

class HelloViewset(viewsets.ViewSet):
    """Test API ViewSet"""
    serializer_class = serializers.HelloSerializer
    #they don't use different http methods for thier function names instead they
    #but they use names for different actions you may perform in thier function names
    #create function creates new http create objects
    def create(self,request):
        """Create a new Hello Message"""
        serializer = serializers.HelloSerializer(data=request.data)
        if serializer.is_valid(): 
            name = serializer.data.get('name')
            message = 'Hello {0}'.format(name)
            return Response({'message':message})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUESTS)
    #retrieve function gets a specific object by it's id use a data-base id to get a specific object
    def retieve(self,request,pk=None):
        """Handles gettig an object by its ID"""
        return Response({'http_method':'GET'})
    #the update function corresponds to the http put method
    #Note: pk is required because you have to know which line you are updating in the data-base
    def update(self,requests,pk=None):
        """Handles updating an object"""
        return Response({'http_method':'PUT'})
    #partial update function corresponds to http patch objects it helps update parts of an object
    def partial_update(self,request,pk=None):
        """Handles update part of an object"""
        return Response({'http_method': 'PATCH'})
    #destroy function destroys or deletes an object from the data-base
    def destroy(self, request, pk=None):
        """Handles removing an object"""
        return Response({'http_method':'DELETE'})
    def list(self,request):
        """Return a Hello Message"""
        a_viewset = [
            'Uses actions (list,create,retrieve,update,partial_update)',
            'Auto maps to URLS using Routers ',
            'Provides more functionality with less code :)'
        ]
        return Response({'message':'Hello! I am Daniel@CodeDrillz','a_viewset': a_viewset})
    
class UserProfileViewSet(viewsets.ModelViewSet):
    """Handles creating, reading and updating profiles"""
    serializer_class = serializers.UserProfileSerializer
    #query set helps the object retrieve an object from the data-base
    queryset = models.UserProfile.objects.all()
    authentication_classes = (TokenAuthentication,)#authenticate for our token
    permission_classes = (permissions.UpdateOwnProfile,)
    filter_backends = (filters.SearchFilter,)#Note the comma is at the end because the variable is a tuple
    search_fields = ('name','email', )
    
class LoginViewSet(viewsets.ViewSet):
    """Checks email and password and returns an auth token"""
    serializer_class = AuthTokenSerializer
    
    def create(self,request):
        """Use the ObtainAuthToken APIView to validate and create a token"""
        return ObtainAuthToken().post(request)

class UserProfileFeedViewSet(viewsets.ModelViewSet):
    """Handles creating, reading and updating profile feed items"""
    authentication_classes = (TokenAuthentication,)
    serializer_class = serializers.ProfileFeedItemSerializer 
    queryset = models.ProfileFeedItem.objects.all()
    permission_classes = (permissions.PostOwnStatus,IsAuthenticated) 
    
    def perform_create(self,serializer): 
        """Sets the user profile to the logged in user."""
        serializer.save(user_profile=self.request.user)