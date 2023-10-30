from django.shortcuts import render, redirect
from ..models import AIModel, User
from ..forms import AIModelForm
import os
import jwt
import paramiko
import json
from pathlib import Path
from jwt import DecodeError

BASE_DIR = Path(__file__).resolve().parent.parent.parent
SECRETS_DIR = BASE_DIR / '.secrets'
SSH = json.load(open(os.path.join(SECRETS_DIR, 'ssh.json')))
secret = json.load(open(os.path.join(SECRETS_DIR, 'secret.json')))

SECRET_KEY = secret['DJANGO_SECRET_KEY']

def ssh_upload_file(local_file, remote_path, filename):
    ssh_host = SSH['HOST']
    ssh_port = SSH['PORT']
    ssh_user = SSH['USER']
    ssh_password = SSH['PASSWORD']
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(ssh_host, port=ssh_port, username=ssh_user, password=ssh_password)
    
    sftp = client.open_sftp()
    
    # 폴더가 없으면 생성
    try:
        sftp.stat(remote_path)
    except FileNotFoundError:
        sftp.mkdir(remote_path)
    
    sftp.putfo(local_file, remote_path + '/' + filename)
    sftp.close()
    client.close()
    
def write(request):

    access_token = request.COOKIES.get('access')
    refresh_token = request.COOKIES.get('refresh')

    payload = jwt.decode(access_token, SECRET_KEY, algorithms='HS256')
    user = User.objects.get(id=payload['user_id'])
    
    context = {
        "user_id": user.id
    }
    return render(request, 'write.html', context)
    

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
                model_instance = AIModel(user_id=user, model_name=model_name)
                model_instance.save() 

                # UUID를 폴더 이름으로 사용
                remote_path = f'path_on_ssh_server/{model_instance.model_id}'

                # SSH 서버로 파일 전송
                ssh_upload_file(csv_file, remote_path, file_name)

                return redirect('loading')
        else:
            print(form.errors)
    else:
        form = AIModelForm()
    return render(request, 'write.html', {'form': 'form'})

