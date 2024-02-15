from rest_framework.generics import ListAPIView,ListCreateAPIView
from .models import Artist
from .serializers import ArtistSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status



class CreateArtistView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        print(request.data)
        data = request.data
        serializer = ArtistSerializer(data = data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)



class ArtistWithAlbumsView(ListAPIView):
    queryset  = Artist.objects.prefetch_related('albums')
    serializer_class = ArtistSerializer
