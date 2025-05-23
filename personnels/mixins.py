from django.shortcuts import redirect

class SaveByPersonnelMixin:
    success_url = "/"  # Tu peux le redéfinir dans chaque vue

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.save_by = self.request.user.personnel
        instance.save()
        return redirect(self.success_url)
