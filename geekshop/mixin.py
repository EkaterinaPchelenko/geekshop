from django.contrib.auth.decorators import user_passes_test
from django.utils.decorators import method_decorator
from django.views.generic.base import View


class CustomDispatchMixin(View):
    @method_decorator(user_passes_test(lambda u: u.is_speruser))
    def dispatch(self, request, *args, **kwargs):
        return super(self).dispatch(request, *args, **kwargs)