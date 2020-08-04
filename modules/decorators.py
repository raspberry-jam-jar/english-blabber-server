from exceptions import PermissionDenied
from graphql_jwt.decorators import user_passes_test


def student_or_staff_member_required(method):
    def wrapper(instance, info, **kwargs):
        if info.context.user.is_staff and not kwargs.get('user_id'):
            raise PermissionDenied()
        elif info.context.user.is_student and kwargs.get('user_id'):
            raise PermissionDenied()
        elif info.context.user.is_student:
            kwargs['user_id'] = info.context.user.id

        return method(instance, info, **kwargs)
    return wrapper


login_required = user_passes_test(lambda u: u.is_authenticated,
                                  exc=PermissionDenied)
