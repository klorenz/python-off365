from .user import user_repr

def get_fields(resource):
    if resource == 'user':
        return user_repr.keys()
