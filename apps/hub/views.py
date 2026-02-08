from django.views.generic import ListView, DetailView
from django.shortcuts import get_object_or_404
from django.http import FileResponse, Http404
from .models import ResourceCategory, Resource, Training

class HubIndexView(ListView):
    model = ResourceCategory
    template_name = 'services/hub/index.html'
    context_object_name = 'categories'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['featured_resources'] = Resource.objects.filter(
            is_featured=True, is_active=True
        )[:6]
        context['featured_trainings'] = Training.objects.filter(
            is_featured=True, is_active=True
        )[:3]
        return context


class ResourceListView(ListView):
    model = Resource
    template_name = 'hub/resource_list.html'
    context_object_name = 'resources'
    paginate_by = 12
    
    def get_queryset(self):
        queryset = Resource.objects.filter(is_active=True)
        
        # Filter by category
        category_slug = self.kwargs.get('category_slug')
        if category_slug:
            queryset = queryset.filter(category__slug=category_slug)
        
        # Filter by type
        resource_type = self.request.GET.get('type')
        if resource_type:
            queryset = queryset.filter(resource_type=resource_type)
        
        # Search
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(
                title__icontains=search
            ) | queryset.filter(
                description__icontains=search
            )
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = ResourceCategory.objects.all()
        
        category_slug = self.kwargs.get('category_slug')
        if category_slug:
            context['current_category'] = get_object_or_404(
                ResourceCategory, slug=category_slug
            )
        
        return context


class ResourceDetailView(DetailView):
    model = Resource
    template_name = 'hub/resource_detail.html'
    context_object_name = 'resource'
    
    def get_queryset(self):
        return Resource.objects.filter(is_active=True)
    
    def get_object(self):
        obj = super().get_object()
        obj.increment_views()
        return obj


class TrainingListView(ListView):
    model = Training
    template_name = 'services/hub/training.html'
    context_object_name = 'trainings'
    paginate_by = 9
    
    def get_queryset(self):
        queryset = Training.objects.filter(is_active=True)
        
        # Filter by difficulty
        difficulty = self.request.GET.get('difficulty')
        if difficulty:
            queryset = queryset.filter(difficulty=difficulty)
        
        # Search
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(
                title__icontains=search
            ) | queryset.filter(
                description__icontains=search
            )
        
        return queryset


class TrainingDetailView(DetailView):
    model = Training
    template_name = 'hub/training_detail.html'
    context_object_name = 'training'
    
    def get_queryset(self):
        return Training.objects.filter(is_active=True)


def download_resource(request, pk):
    """Download a resource file"""
    resource = get_object_or_404(Resource, pk=pk, is_active=True)
    
    if not resource.file:
        raise Http404("Fichier non disponible")
    
    resource.increment_downloads()
    
    return FileResponse(
        resource.file.open('rb'),
        as_attachment=True,
        filename=resource.file.name.split('/')[-1]
    )


# Library view (alias for resources)
class LibraryView(ResourceListView):
    template_name = 'services/hub/library.html'
    
    def get_queryset(self):
        return Resource.objects.filter(
            is_active=True,
            resource_type__in=['pdf', 'article', 'guide']
        )
