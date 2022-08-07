NATIONALITIES = [
    ('Uganda', 'Uganda'),
    ('South Sudan', 'South Sudan'),
    ('Kenya', 'Kenya'),
    ('Tanzania', 'Tanzania'),
    ('Democratic Republic of Congo', 'Democratic Republic of Congo'),
    ('Rwanda', 'Rwanda'),
    ('Burundi', 'Burundi'),
]

from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import User



class AuthBackend(object):

    def authenticate(self, username=None, password=None):
        print('>>>>>>>>>>>>>')
        user = User.objects.filter(username=username).first()
        if not user:
            user = User.objects.filter(profile__telephone=username).first()

        if user:
            is_valid = check_password(password, user.password)
            if is_valid:
                return user
        return None
