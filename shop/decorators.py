from django.shortcuts import redirect

#decorator for redirecting authenticated user
def redirect_authenticated_user(view_func):
    def wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('index')
        return view_func(request, *args, **kwargs)
    return wrapped_view
#custom decorator for login_required
def login_required_user(view_func):
    def wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        return view_func(request, *args, **kwargs)
    return wrapped_view