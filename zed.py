from core.models import Profile, Entity, User
from django.contrib.auth.models import Group


def unmask_saved_numbers():
    for profile in Profile.objects.all():
        if profile.telephone:
            profile.telephone = profile.telephone.strip().replace(' ','').replace('(','').replace(')','').replace('-','')
            print(profile.telephone)
            profile.save()

def init():
    # create superuser
    User.objects.filter(
        username='samuelitwaru').exists() or User.objects.create_superuser(
        'samuelitwaru', 'samuelitwaru@gmail.com', '123')
    # create entity
    Entity.objects.get_or_create (
        id = 1,
        name = 'Mvara Senior Secondary School',
        location='P.O.BOX 23 Arua',
        telephone='0772425437',
        email='mvarasecondaryschool@gmail.com'
    )
    # create dos
    user, created = User.objects.get_or_create(
        username = 'samuelitwaru@yahoo.com',
        email = 'samuelitwaru@yahoo.com',
        first_name = 'Samuel',
        last_name = 'Itwaru',
    )
    user.set_password('123')
    user.save()
    dos_group = Group.objects.get(name='dos')
    dos_group.user_set.add(user)