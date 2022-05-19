from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .scripts import process_image

class TestImage(APIView):
    """
    Image testing class.
    """
    def post(self, request, *args, **kwargs):
        """
        Test an image to see if is a damaged bottle.
        """

        images = {
            'front': request.data.get('file_1'),
            'back': request.data.get('file_2'),
            'up': request.data.get('file_3'),
        }

        print(images)
        
        return Response({
            'data': process_image(
                images['front'], 
                images['back'], 
                images['up']
            )
        }, status=status.HTTP_200_OK)