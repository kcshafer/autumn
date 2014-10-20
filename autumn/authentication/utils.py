from django.http import HttpResponseRedirect

def auth_required(f):
  def wrap(request, *args, **kwargs):
        if 'access_token' in request.session:
             return f(request, *args, **kwargs)
        else:
            return HttpResponseRedirect('/data/query')