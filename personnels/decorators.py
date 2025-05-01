from django.contrib import messages
from django.shortcuts import redirect
from functools import wraps

def fonction_required(*fonctions_autorisees):
    """Décorateur pour restreindre l'accès selon la fonction de l'utilisateur."""
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            # Vérification connexion
            if not request.user.is_authenticated:
                messages.error(request, "Veuillez vous connecter pour accéder à cette page.")
                return redirect('login')  # Redirection vers la page de connexion

            # Superuser toujours autorisé
            if request.user.is_superuser:
                return view_func(request, *args, **kwargs)

            # Vérification fonction de l'utilisateur
            try:
                if request.user.personnel.fonction in fonctions_autorisees:
                    return view_func(request, *args, **kwargs)
            except AttributeError:
                pass  # Si l'utilisateur n'a pas d'attribut "personnel"

            # Permission refusée avec message + redirection
            messages.error(request, "Vous n'avez pas l'autorisation d'accéder à cette interface.")
            return redirect('login')  # Redirection vers une page spécifique

        return _wrapped_view
    return decorator
