from django.shortcuts import render, redirect
from ..models import AIModel, User, ChatRoom
from ..forms import AIModelForm
import os
import jwt
import json
import requests
from pathlib import Path
from jwt import DecodeError
from django.core.mail                       import EmailMessage
from rest_framework.response import Response
from rest_framework import viewsets, status
from ..serializers import EmailSerializer
from rest_framework.views                   import APIView

BASE_DIR = Path(__file__).resolve().parent.parent.parent
SECRETS_DIR = BASE_DIR / '.secrets'
secret = json.load(open(os.path.join(SECRETS_DIR, 'secret.json')))

SECRET_KEY = secret['DJANGO_SECRET_KEY']



def upload_model(request):
    if request.method == 'POST':
        form = AIModelForm(request.POST, request.FILES)
        if form.is_valid():
            user_id = request.POST.get('user_id')
            model_name = request.POST.get('model_name')
            user = User.objects.get(id=user_id)

            csv_file = request.FILES.get('file_dir', None)

            if csv_file:
                file_name = csv_file.name
                file_content = csv_file.read()
                model_instance = AIModel(user_id=user, model_name=model_name)
                model_instance.save() 

                url = "http://oreumi.site:1217/finetuning/uploadData"
                data = {
                    'my_model_id': model_instance.model_id,
                    'my_model_name': model_name,
                    'user_email': user.email
                }

                files = {'file': (file_name, file_content)}
                response = requests.post(url, data=data, files=files)

                # 응답 처리
                if response.status_code == 200:
                    return redirect('loading')
                else:
                    # 실패 시 처리 로직 (예: 에러 메시지 표시)
                    return render(request, 'error.html', {'message': 'Upload failed.'})
        else:
            print(form.errors)
    else:
        form = AIModelForm()
    return render(request, 'write.html', {'form': 'form'})



class EmailAPIView(APIView):
    def post(self, request):
        serializer = EmailSerializer(data=request.data)
        if serializer.is_valid():
            email_title = serializer.validated_data['email_title']
            email_msg = serializer.validated_data['email_msg']
            recipient_email = serializer.validated_data['email']

            try:
                email = EmailMessage(email_title, email_msg, to=[recipient_email])
                email.send()
                return Response({'status': 'success', 'message': 'Email sent successfully.'}, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({'status': 'error', 'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

class ModelViewSet(APIView):
    def put(self, request):
        model_id = ChatRoom.objects.get(id=request.data['chat_id']).model_id_id
        model = AIModel.objects.get(model_id=model_id)
        model.model_name = request.data['model_name']
        model.save()
        return Response(status=status.HTTP_200_OK)