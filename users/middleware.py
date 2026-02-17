from django.shortcuts import redirect

class LoginRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        public_paths = ['/login/', '/register/', '/index/'] 
        
        if not request.session.get('matricula') and request.path not in public_paths:
            return redirect('login')

        response = self.get_response(request)
        return response