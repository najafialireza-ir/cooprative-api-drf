from django.contrib.auth.models import UserManager

class UserManager(UserManager):
    def create_user(self, username, email, user_type, password):
        if not email:
            raise ValueError('You Must Have a Email')
        if not user_type:
            raise ValueError('You Must Have a User Type!')
        
        user = self.model(email=self.normalize_email(email), username=username, user_type=user_type)
        user.set_password(password)
        user.save(using=self.db)
        return user
    
    def create_driver(self, username, email, user_type, password):
        user = self.create_user(username, email, user_type, password)
        user.is_driver = True
        user.save(using=self.db)
        return user
    
    def create_superuser(self, username, email, user_type, password):
        user = self.create_user(username, email, user_type, password)
        user.is_superuser = True
        user.is_staff = True
        user.save()
        return user