from rest_framework import status, generics
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.db.models import Count
from .models import Breed, Dog
from .serializers import BreedSerializer, DogSerializer, AuthSerializer, AnswerSerializer

@api_view(['POST'])
@authentication_classes([])
@permission_classes([AllowAny])
def auth_view(request):
    serializer = AuthSerializer(data=request.data)
    if serializer.is_valid():
        # Aquí implementarías la autenticación con Supabase
        # Por ahora, simulamos un token
        return Response({'token': 'simulated_jwt_token'})
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class BreedListView(generics.ListAPIView):
    queryset = Breed.objects.all()
    serializer_class = BreedSerializer
    pagination_class = None  # Usaremos la paginación por defecto de DRF

class DogListView(generics.ListAPIView):
    queryset = Dog.objects.all().select_related('breed')
    serializer_class = DogSerializer
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Filtros
        name = self.request.query_params.get('name')
        breed = self.request.query_params.get('breed')
        breed__name = self.request.query_params.get('breed__name')
        
        if name:
            queryset = queryset.filter(name__icontains=name)
        if breed:
            queryset = queryset.filter(breed_id=breed)
        if breed__name:
            queryset = queryset.filter(breed__name__icontains=breed__name)
            
        return queryset

@api_view(['POST'])
def answer_view(request):
    serializer = AnswerSerializer(data=request.data)
    if serializer.is_valid():
        # Aquí procesarías las respuestas
        return Response(serializer.validated_data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Vista para calcular estadísticas (útil para el endpoint /answer/)
@api_view(['GET'])
def statistics_view(request):
    total_breeds = Breed.objects.count()
    total_dogs = Dog.objects.count()
    
    # Raza más común
    common_breed = Dog.objects.values('breed__name').annotate(
        count=Count('id')
    ).order_by('-count').first()
    
    # Nombre más común
    common_dog_name = Dog.objects.values('name').annotate(
        count=Count('id')
    ).order_by('-count').first()
    
    return Response({
        'totalBreeds': total_breeds,
        'totalDogs': total_dogs,
        'commonBreed': common_breed['breed__name'] if common_breed else '',
        'commonDogName': common_dog_name['name'] if common_dog_name else ''
    })