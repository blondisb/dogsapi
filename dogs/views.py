from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.conf import settings
from supabase import create_client
from .serializers import AuthSerializer, AnswerSerializer

@api_view(['POST'])
@authentication_classes([])
@permission_classes([AllowAny])
def auth_view(request):
    serializer = AuthSerializer(data=request.data)
    if serializer.is_valid():
        email = serializer.validated_data['email']
        password = serializer.validated_data['password']
        
        try:
            supabase = create_client(settings.SUPABASE_URL, settings.SUPABASE_KEY)
            auth_response = supabase.auth.sign_in_with_password({
                "email": email,
                "password": password
            })
            
            if auth_response.user:
                return Response({
                    'token': auth_response.session.access_token
                })
            else:
                return Response(
                    {'error': 'Unable to log in with provided credentials'},
                    status=status.HTTP_400_BAD_REQUEST
                )
                
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def breeds_view(request):
    try:
        supabase = create_client(settings.SUPABASE_URL, settings.SUPABASE_KEY)
        
        # Obtener parámetros de paginación
        limit = int(request.GET.get('limit', 10))
        offset = int(request.GET.get('offset', 0))
        
        # Obtener razas
        response = supabase.table('breeds')\
            .select('*', count='exact')\
            .range(offset, offset + limit - 1)\
            .execute()
        
        count = response.count if hasattr(response, 'count') else len(response.data)
        
        return Response({
            'count': count,
            'next': f"http://127.0.0.1:8000/breeds/?limit={limit}&offset={offset + limit}" if offset + limit < count else None,
            'previous': f"http://127.0.0.1:8000/breeds/?limit={limit}&offset={max(0, offset - limit)}" if offset > 0 else None,
            'results': response.data
        })
        
    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['GET'])
def dogs_view(request):
    try:
        supabase = create_client(settings.SUPABASE_URL, settings.SUPABASE_KEY)
        
        # Obtener parámetros
        page = int(request.GET.get('page', 1))
        limit = 10
        offset = (page - 1) * limit
        
        # Construir query base
        query = supabase.table('dogs')\
            .select('*, breeds(name)', count='exact')\
            .range(offset, offset + limit - 1)
        
        # Aplicar filtros
        name = request.GET.get('name')
        breed = request.GET.get('breed')
        breed_name = request.GET.get('breed__name')
        
        if name:
            query = query.ilike('name', f'%{name}%')
        if breed:
            query = query.eq('breed_id', breed)
        if breed_name:
            query = query.eq('breeds.name', breed_name)
        
        response = query.execute()
        count = response.count if hasattr(response, 'count') else len(response.data)
        
        # Transformar datos para incluir breed como string
        results = []
        for dog in response.data:
            results.append({
                'id': dog['id'],
                'name': dog['name'],
                'breed': dog['breeds']['name'] if dog.get('breeds') else None,
                'breed__name': dog['breeds']['name'] if dog.get('breeds') else None
            })
        
        return Response({
            'count': count,
            'next': f"http://127.0.0.1:8000/dogs/?page={page + 1}" if offset + limit < count else None,
            'previous': f"http://127.0.0.1:8000/dogs/?page={page - 1}" if page > 1 else None,
            'results': results
        })
        
    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['POST'])
def answer_view(request):
    serializer = AnswerSerializer(data=request.data)
    if serializer.is_valid():
        # Simplemente retornamos los datos recibidos
        return Response(serializer.validated_data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)