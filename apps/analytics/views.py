from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test
from apps.authentication.views import es_admin

# Views básicas para analytics - se implementarán después
@login_required
@user_passes_test(es_admin)
def reportes_panel(request):
    """Panel básico de reportes - placeholder."""
    return render(request, 'analytics/reportes.html', {})
