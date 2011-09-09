# -*- coding: utf-8 -*-

from functools import wraps


from django.http import Http404, HttpResponseRedirect
from django.utils.decorators import available_attrs




class BaseAuthDecorator(object):
    """
        Base class to permissions decorators.
        Childs must rewrite BaseAuthDecorator.check_perms method
        Example:
            class AnonymousRequiredDecorator(BaseAuthDecorator):
                def check_perms(self, user):
                    return not user.is_authenticated()


            anonymous_required = AnonymousRequiredDecorator()

    """
    error_response_class = Http404

    def check_perms(self, user):
        """
            Method to check access permissions, must be rewriten by child classes
        """
        raise NotImplementedError, "You must rewrite BaseAuthDecorator.check_perms method in child class"

    def error_action(self, *args, **kwargs):
        """
            Method that retrun response or raise exception on check permissions fail
            Default:
                raise self.error_response_class that's Http404
        """
        raise self.error_response_class

    def __call__(self, function):
        def _dec(view_func):
            def _view(request, *args, **kwargs):
                if not self.check_perms(request.user):
                    return self.error_action(request=request)
                return view_func(request, *args, **kwargs)
            return wraps(view_func, assigned=available_attrs(view_func))(_view)
        return _dec(function)


class AnonymousRequiredDecorator(BaseAuthDecorator):
    """
        Only anonymous allowed
    """
    def check_perms(self, user):
        return not user.is_authenticated()

    def error_action(self, request):
        return HttpResponseRedirect(request.META.get("HTTP_REFERER", "/"))


anonymous_required = AnonymousRequiredDecorator()

