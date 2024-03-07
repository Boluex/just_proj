from rest_framework.decorators import api_view, permission_classes,authentication_classes
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from rest_framework.authentication import BasicAuthentication
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_401_UNAUTHORIZED,HTTP_404_NOT_FOUND
from rest_framework import status 
from .serializers import all_programs_serializer
from course.models import Program,Course
from .serializers import all_course_serializer

@api_view(['GET'])
@permission_classes([IsAdminUser]) 
@authentication_classes([BasicAuthentication])
def list_all_programs(request):
    if not request.user.is_authenticated:
        return Response(status=HTTP_401_UNAUTHORIZED)

    programs = Program.objects.all().order_by('title')
    serializer = all_programs_serializer(programs, many=True)
    return Response(serializer.data, status=HTTP_200_OK)




@api_view(['GET'])
@permission_classes([IsAdminUser]) 
@authentication_classes([BasicAuthentication])
def get_program_by_id(request, pk):
    if not request.user.is_superuser:
        return Response(status=HTTP_401_UNAUTHORIZED)

    try:
        program = Program.objects.get(pk=pk)
    except Program.DoesNotExist:
        return Response(status=HTTP_404_NOT_FOUND)

    serializer = all_programs_serializer(program)
    return Response(serializer.data, status=HTTP_200_OK)



@api_view(['GET', 'DELETE']) 
@permission_classes([IsAdminUser]) 
@authentication_classes([BasicAuthentication])
def get_or_delete_program(request, pk):
    if not request.user.is_authenticated :
        return Response(status=HTTP_401_UNAUTHORIZED)

    try:
        program = Program.objects.get(pk=pk)
    except Program.DoesNotExist:
        return Response(status=HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = all_programs_serializer(program)
        program.delete()
        return Response(serializer.data, status=HTTP_200_OK)
    elif request.method == 'DELETE':
        program.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)




@api_view(['POST'])
@permission_classes([IsAdminUser]) 
@authentication_classes([BasicAuthentication])
def create_program(request):
    if not request.user.is_authenticated:
        return Response(status=HTTP_401_UNAUTHORIZED)

    serializer = all_programs_serializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)







@api_view(['GET'])
@permission_classes([IsAdminUser]) 
@authentication_classes([BasicAuthentication])
def list_all_the_courses(request):
    if not request.user.is_authenticated:
        return Response(status=HTTP_401_UNAUTHORIZED)

    courses = Course.objects.all().order_by('title') 
    serializer = all_course_serializer(courses, many=True)
    return Response(serializer.data, status=HTTP_200_OK)




@api_view(['GET'])
@permission_classes([IsAdminUser]) 
@authentication_classes([BasicAuthentication])
def get_course_by_id(request, pk):
    if not request.user.is_authenticated:
        return Response(status=HTTP_401_UNAUTHORIZED)

    try:
        course = Course.objects.get(pk=pk)
    except Course.DoesNotExist:
        return Response(status=HTTP_404_NOT_FOUND)

    serializer = all_course_serializer(course)
    return Response(serializer.data, status=HTTP_200_OK)




@api_view(['POST'])
@permission_classes([IsAdminUser]) 
@authentication_classes([BasicAuthentication])
def create_course(request):
    if not request.user.is_authenticated:
        return Response(status=HTTP_401_UNAUTHORIZED)

    serializer = all_course_serializer(data=request.data)
    if serializer.is_valid():
        program_id = serializer.validated_data['program']
        try:
            program = Program.objects.get(pk=program_id)
        except Program.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={'error': 'Invalid program ID'})

        course = serializer.save(program=program) 
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@permission_classes([IsAdminUser]) 
@authentication_classes([BasicAuthentication])
def delete_course(request, pk):
    if not request.user.is_authenticated:
        return Response(status=HTTP_401_UNAUTHORIZED)

    try:
        course = Course.objects.get(pk=pk)
    except Course.DoesNotExist:
        return Response(status=HTTP_404_NOT_FOUND)

    course.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)