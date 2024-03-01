from course.models import *
# from rest_framework.decorators import api_view
from rest_framework.serializers import ModelSerializer,HyperlinkedIdentityField




class all_programs_serializer(ModelSerializer):
    class Meta:
        model=Program
        fields=['id','title','summary']


class all_course_serializer(ModelSerializer):
    class Meta:
        model=Course
        fields=['slug','title','code','credit','summary','program','level','year','semester']


class course_feedbacks_serializer(ModelSerializer):
    class Meta:
        model=Course_feedback
        fields=[]


