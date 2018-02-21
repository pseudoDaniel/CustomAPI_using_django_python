from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import BaseUserManager


# Create your models here.
class UserProfileManager(BaseUserManager):
    """helps django work with our custom user model."""
    #We now define a function that tells django to create a custom user model with the
    #customised user model
    def create_user(self,email,name,password=None):
        """creates a new user profile object"""
        #now we write the logic that create a new user profile in the system
        #check if the email exists
        if not email:
            raise ValueError("Users must have an email address")
        #normalize the email addres by converting them to lower case so that all the email address are
        #standardised in the system
        email = self.normalize_email(email)
        #create a new user profile object
        user = self.model(email = email, name = name)
        #finally we set the user password
        #We do not put password in the user object above because the set_password() method
        #encrypts the password
        user.set_password(password)
        user.save(using = self._db)
        return user
    
    #We now a function that creates an admin
    def create_superuser(self,email,name,password):
        """Creates and save a super user with given details """
        user = self.create_user(email,name,password)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user
    
class UserProfile(AbstractBaseUser, PermissionsMixin):
    """This represents a "user profile" within the system"""
    #We now want to create fields for our django model
    email = models.EmailField( max_length=255, unique = True)
    name = models.CharField(max_length=255)
    #the next function determines whether a user is active
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    #We now create an object manager
    #The object manager is another class that we can use to manage the user UserProfile
    #for example creating an admin-user or a regular user
    objects = UserProfileManager()
    USERNAME_FIELD = 'email'
    #We now set up a list required fields for all user profiles in the system
    REQUIRED_FIELDS = ['name']
    #Next we Create helper functions for our model
    def get_full_name(self):
        """    Used to get a user's Full name        """
        return self.name

    def get_short_name(self):
        """Used to get a user's shortname"""
        return self.name

    def __str__(self):
        """django uses this when it needs to convert the object to a string"""
        return self.email
    
class ProfileFeedItem(models.Model):
    """Profile Status Update"""
    user_profile = models.ForeignKey('UserProfile',on_delete=models.CASCADE)
    #store user staus text
    status_text = models.CharField(max_length=255)
    #store the date and time for status update in a field
    created_on = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        """Return the model as a string"""
        return self.status_text