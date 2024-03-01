from rest_framework.decorators import api_view,permission_classes,authentication_classes
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from rest_framework import status
from core.models import NewsAndEvents,Session
from .serializers import NewsAndEventsSerializer,SessionSerializer
from rest_framework.permissions import IsAdminUser,IsAuthenticated
from rest_framework.authentication import BasicAuthentication


# ######################################################################
# News and event serialization
########################################################################
@api_view(['GET'])
@permission_classes([IsAdminUser])  
@authentication_classes([BasicAuthentication])
def list_news_and_events(request):
    news_and_events = NewsAndEvents.objects.all().order_by('-upload_time')
    serializer = NewsAndEventsSerializer(news_and_events, many=True)
    return Response(serializer.data, status=HTTP_200_OK)



@api_view(['GET'])
@permission_classes([IsAdminUser])  
@authentication_classes([BasicAuthentication])
def get_news_or_event_by_id(request, pk):
    try:
        news_or_event = NewsAndEvents.objects.get(pk=pk)
    except NewsAndEvents.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = NewsAndEventsSerializer(news_or_event)
    return Response(serializer.data, status=HTTP_200_OK)



@api_view(['POST'])
@permission_classes([IsAdminUser])  
@authentication_classes([BasicAuthentication])
def create_news_or_event(request):
    if not request.user.is_authenticated:
        return Response(status=status.HTTP_401_UNAUTHORIZED)

    serializer = NewsAndEventsSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@permission_classes([IsAdminUser])  
@authentication_classes([BasicAuthentication]) 
def delete_news_or_event(request, pk):
    if not request.user.is_authenticated:
        return Response(status=status.HTTP_401_UNAUTHORIZED)

    try:
        news_or_event = NewsAndEvents.objects.get(pk=pk)
    except NewsAndEvents.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    news_or_event.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


#####################################################################
# Session serialization
#####################################################################
# Create a new session
@api_view(['POST'])
@permission_classes([IsAuthenticated])  
def create_session(request):
    if not request.user.is_authenticated:
        return Response(status=status.HTTP_401_UNAUTHORIZED)

    serializer = SessionSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Retrieve all sessions
@api_view(['GET'])
def list_sessions(request):
    sessions = Session.objects.all()
    serializer = SessionSerializer(sessions, many=True)
    return Response(serializer.data, status=HTTP_200_OK)

# Get a session by name
@api_view(['GET'])
def get_session_by_name(request, name):
    try:
        session = Session.objects.get(session=name)
    except Session.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = SessionSerializer(session)
    return Response(serializer.data, status=HTTP_200_OK)

# Update a session
@api_view(['PUT'])
@permission_classes([IsAuthenticated]) 
def update_session(request, name):
    try:
        session = Session.objects.get(session=name)
    except Session.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = SessionSerializer(session, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Delete a session
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])  
def delete_session(request, name):
    try:
        session = Session.objects.get(session=name)
    except Session.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    session.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)
