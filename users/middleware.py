from django.shortcuts import redirect

class LoginRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        public_paths = ['/login/', '/register/', '/index/'] 
        usuario_tiene_sesion = request.session.get('matricula')
        if usuario_tiene_sesion:
            if request.path in public_paths or request.path == '/':
                return redirect('home')
        else:
            if request.path == '/':
                return redirect('inicio')
            if request.path not in public_paths:
                return redirect('login')
        response = self.get_response(request)
        return response