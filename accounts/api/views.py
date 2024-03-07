from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_400_BAD_REQUEST,HTTP_204_NO_CONTENT
from rest_framework.decorators import authentication_classes,permission_classes
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import AllowAny,IsAuthenticated,IsAdminUser
from accounts.models import User,Student
from .serializers import UserSerializer,StudentSerializer

# ########################################
# user views
##########################################
@api_view(['POST'])
def create_user(request):
    # check the models know what to add as the input field....things like the is_lecturer and is_student fields which is a boolean,and other data
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=HTTP_201_CREATED)
    return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)



@api_view(['GET'])
def list_users(request):
    users = User.objects.all()
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data, status=HTTP_200_OK)


@api_view(['GET'])
def get_user_by_id(request, pk):
    try:
        user = User.objects.get(pk=pk)
    except User.DoesNotExist:
        return Response(status=HTTP_400_BAD_REQUEST)

    serializer = UserSerializer(user)
    return Response(serializer.data, status=HTTP_200_OK)



@api_view(['PUT'])
def update_user(request, pk):
    try:
        user = User.objects.get(pk=pk)
    except User.DoesNotExist:
        return Response(status=HTTP_400_BAD_REQUEST)

    serializer = UserSerializer(user, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=HTTP_200_OK)
    return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
def delete_user(request, pk):
    try:
        user = User.objects.get(pk=pk)
    except User.DoesNotExist:
        return Response(status=HTTP_400_BAD_REQUEST)

    user.delete()
    return Response(status=HTTP_204_NO_CONTENT)





########################################
#student_views
########################################
@api_view(['POST'])
def create_student(request):
    serializer = StudentSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=HTTP_201_CREATED)
    return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)



@api_view(['GET'])
def list_students(request):
    students = Student.objects.all()
    serializer = StudentSerializer(students, many=True)
    return Response(serializer.data, status=HTTP_200_OK)

@api_view(['GET'])
def get_student_by_id(request, pk):
    try:
        student = Student.objects.get(pk=pk)
    except Student.DoesNotExist:
        return Response(status=HTTP_400_BAD_REQUEST)

    serializer = StudentSerializer(student)
    return Response(serializer.data, status=HTTP_200_OK)



@api_view(['PUT'])
def update_student(request, pk):
    try:
        user = Student.objects.get(pk=pk)
    except User.DoesNotExist:
        return Response(status=HTTP_400_BAD_REQUEST)

    serializer = StudentSerializer(user, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=HTTP_200_OK)
    return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
def delete_student(request, pk):
    try:
        user = Student.objects.get(pk=pk)
    except User.DoesNotExist:
        return Response(status=HTTP_400_BAD_REQUEST)

    user.delete()
    return Response(status=HTTP_204_NO_CONTENT)