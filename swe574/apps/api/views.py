from rest_framework.response import Response
from rest_framework.decorators import api_view
from learning_space.models import LearningSpace
from .serializers import LearningSpaceSerializer


@api_view(['GET'])
def get_data(request):
    learning_spaces = LearningSpace.objects.all()
    serializer = LearningSpaceSerializer(learning_spaces, many=True)
    return Response(serializer.data)


