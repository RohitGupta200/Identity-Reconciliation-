from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import user
from .utils import *
from .serializers import contactSerializer,userSerializer

@api_view(['POST'])
def create(request):
    try:
        data1=request.data
        new_user=user()
        new_user.email = data1['email']
        new_user.phoneNumber = data1['phoneNumber']
        existing_user = getDbUser(new_user)
        if existing_user != None:
            existing_user.save()
            return Response({
            "success" : True,
            "message" : "created successfully",
        })
        new_user.linkPrecedence="primary"
        uid = getPrimaryUserId(new_user)
        print(new_user.id)
        if(uid!=-1):
            new_user.linkPrecedence="secondary"
            new_user.linkedId = uid
        serializer = userSerializer(data=data1)
        if(serializer.is_valid()):
            serializer.save()
            return Response({
                "success" : True,
                "message" : "created successfully",
            })
        else:
            return Response({
                'response':'failure',
            'message':serializer.errors,
            })
    except Exception as e:
        return Response({

            'message':str(e),
        })
    

@api_view(['POST'])
def identify(request):
    try:
        data = request.data
        new_user=user()
        new_user.email = data['email']
        new_user.phoneNumber = data['phoneNumber']
        uid = getPrimaryUserId(new_user)
        if uid==-1:
            return Response({

                'message': 'user not found',
            })
        else:
            updateUsersStatus(new_user,uid)
            primary_contact = getUserById(uid)
            secondary_contacts = getAllAssociatedContacts(uid)
            contact_list = getContact(primary_contact,secondary_contacts)
            serializer = contactSerializer(data=contact_list)
            if serializer.is_valid():
                return Response({
                'response':'success',
                'contact' : serializer.data,
                })
            return Response({
                'response':'failure',
            'message':serializer.errors,
            })

            
    except Exception as e:
        return Response({
            'message':str(e),
        })
 

