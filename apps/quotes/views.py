from django.shortcuts import render, redirect
from django.contrib import messages
from apps.shop.models import Quote
from django.contrib.auth.models import User

def quote_form(request):
    if request.method == 'POST':
        title = request.POST.get('title', '').strip()
        description = request.POST.get('description', '').strip()
        project_type = request.POST.get('project_type', 'Red Corporativa')
        contact_info = request.POST.get('contact_info', '').strip()
        urgency = request.POST.get('urgency', 'Media')

        if not title or not description:
            messages.error(request, "Por favor, complete todos los campos obligatorios del formulario de cotización.")
            return render(request, 'quotes/quote_form.html')

        full_description = f"[Tipo: {project_type} | Urgencia: {urgency} | Contacto: {contact_info}]\n\n{description}"
        
        # Asignar usuario o crear uno genérico si es anónimo
        user = request.user if request.user.is_authenticated else None
        if not user:
            user, _ = User.objects.get_or_create(username='cliente_anonimo', defaults={'email': 'info@telemred.cl'})

        Quote.objects.create(
            user=user,
            title=f"[{project_type}] {title}",
            description=full_description
        )

        messages.success(request, f"¡Su solicitud de cotización '{title}' fue enviada con éxito al equipo de ingeniería de TELEMRED! Le contactaremos a la brevedad.")
        return redirect('quote_form')

    # Si hay un asunto preseleccionado desde el catálogo
    subject = request.GET.get('subject', '')
    return render(request, 'quotes/quote_form.html', {'preselected_subject': subject})
