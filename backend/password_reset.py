from rest_framework.views import APIView
from rest_framework.response import Response
from django.core.mail import send_mail
from django.conf import settings
from django.shortcuts import redirect
from django.http import JsonResponse
from .models import *
from .serializers import *


class ResetPasswordEmail(APIView):
    serializer_class = EmailSerializers
    def post(self,request):
        serializers = self.serializer_class(data=request.data)
        serializers.is_valid(raise_exception=True)
        email = serializers.validated_data['email']
        check_user = User.objects.filter(email=email)
        if check_user.count() > 0:
            get_user = User.objects.get(email=email)
            create_verify = UserVerify.objects.get_or_create(user_id=get_user.id)

            subject = "Mail For Password Reset"
            message = f"Go to given link below: \n\n http://127.0.0.1:8000/check_email?token={create_verify[0].token}"
            recepient = f"{get_user.email}"
            send_mail(subject,message,settings.EMAIL_HOST_USER,[recepient],fail_silently=True)

            return Response({'success':'Email has sent!'})
        return Response({'data':'None'})

def check_email(request):
    if request.method == "GET":
        token = request.GET.get('token')
        try:
            check_token = UserVerify.objects.get(token=token)
            return redirect('http://127.0.0.1:8000/password_reset/?token=' + f"{check_token.token}")
        except:
            return JsonResponse({"error" : "Invalid token"})
    return JsonResponse({"data" : "None"})

class PasswordResetView(APIView):
    serializer_class = PasswordResetSerializers

    def post(self,request):
        serializers = self.serializer_class(data=request.data)
        serializers.is_valid(raise_exception=True)
        token = request.GET.get('token')
        check_token = UserVerify.objects.get(token=token)
        get_user = User.objects.get(id=check_token.user.id)
        get_user.set_password(serializers.validated_data['password'])
        get_user.save()
        check_token.delete()
        return Response({"success":"Password reseted successfully!"})