from core.models import Profile


def unmask_saved_numbers():
    for profile in Profile.objects.all():
        if profile.telephone:
            profile.telephone = profile.telephone.strip().replace(' ','').replace('(','').replace(')','').replace('-','')
            print(profile.telephone)
            profile.save()
