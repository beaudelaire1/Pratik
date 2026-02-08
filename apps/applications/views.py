from django.views.generic.edit import CreateView
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.contrib import messages
from django.http import JsonResponse
from .models import Application
from .forms import ApplicationForm
from apps.internships.models import Internship

class ApplicationCreateView(LoginRequiredMixin, CreateView):
    model = Application
    form_class = ApplicationForm
    template_name = 'applications/application_form.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.user_type != 'student':
            messages.error(request, "Seuls les étudiants peuvent postuler.")
            return redirect('internship_detail', slug=self.kwargs['slug'])
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        internship = get_object_or_404(Internship, slug=self.kwargs['slug'])
        
        # Check if already applied
        if Application.objects.filter(student=self.request.user, internship=internship).exists():
            messages.warning(self.request, "Vous avez déjà postulé à cette offre.")
            return redirect('internship_detail', slug=internship.slug)

        form.instance.student = self.request.user
        form.instance.internship = internship
        
        # Save application
        response = super().form_valid(form)
        
        # Create notification for company
        from apps.notifications.models import Notification
        from apps.notifications.utils import send_application_received_email
        
        Notification.create_notification(
            recipient=internship.company,
            notification_type=Notification.APPLICATION_RECEIVED,
            title="Nouvelle candidature reçue",
            message=f"{self.request.user.get_full_name() or self.request.user.username} a postulé pour {internship.title}",
            link=f"/dashboard/"
        )
        
        # Send email notification
        send_application_received_email(self.object)
        
        messages.success(self.request, "Votre candidature a été envoyée avec succès!")
        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['internship'] = get_object_or_404(Internship, slug=self.kwargs['slug'])
        return context

    def get_success_url(self):
        return reverse('internship_detail', kwargs={'slug': self.kwargs['slug']})


class ApplicationUpdateStatusView(LoginRequiredMixin, View):
    """
    View to accept or reject an application (Company only)
    """
    def post(self, request, pk):
        application = get_object_or_404(Application, pk=pk)
        
        # Verify that the user is the company that posted the internship
        if application.internship.company != request.user:
            return JsonResponse({'error': 'Non autorisé'}, status=403)
        
        # Get action and message
        action = request.POST.get('action')  # 'accept' or 'reject'
        message = request.POST.get('message', '')
        
        # Mark as viewed
        application.mark_as_viewed(request.user)
        
        # Update status
        if action == 'accept':
            application.accept(message)
            notif_type = 'application_accepted'
            notif_title = "Candidature acceptée !"
            notif_message = f"Votre candidature pour {application.internship.title} a été acceptée"
            success_message = "Candidature acceptée avec succès"
        elif action == 'reject':
            application.reject(message)
            notif_type = 'application_rejected'
            notif_title = "Candidature refusée"
            notif_message = f"Votre candidature pour {application.internship.title} a été refusée"
            success_message = "Candidature refusée"
        else:
            return JsonResponse({'error': 'Action invalide'}, status=400)
        
        # Create notification for student
        from apps.notifications.models import Notification
        from apps.notifications.utils import send_application_response_email
        
        Notification.create_notification(
            recipient=application.student,
            notification_type=notif_type,
            title=notif_title,
            message=notif_message + (f": {message}" if message else ""),
            link=f"/dashboard/"
        )
        
        # Send email notification
        send_application_response_email(application, accepted=(action == 'accept'))
        
        return JsonResponse({
            'success': True,
            'message': success_message,
            'status': application.get_status_display()
        })
