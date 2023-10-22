from django.shortcuts import render, redirect
from ..models import AIModel
from ..forms import AIModelForm
import os
import paramiko
import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent
SECRETS_DIR = BASE_DIR / '.secrets'
SSH = json.load(open(os.path.join(SECRETS_DIR, 'ssh.json')))

def ssh_upload_file(local_file, remote_path, filename):
    ssh_host = SSH['HOST']
    ssh_port = SSH['PORT']
    ssh_user = SSH['USER']
    ssh_password = SSH['PASSWORD']
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(ssh_host, port=ssh_port, username=ssh_user, password=ssh_password)
    
    sftp = client.open_sftp()
    sftp.putfo(local_file, remote_path + '/' + filename)
    sftp.close()
    client.close()

def upload_model(request):
    # if request.method == 'POST':
    #     form = DataForm(request.POST, request.FILES)
    #     if form.is_valid() or 'file_dir' in request.FILES:
    #         csv_file = request.FILES.get('file_dir', None)
    #         if csv_file:
    #             file_name = csv_file.name
    #             remote_path = 'path_on_ssh_server'

    #             # SSH 서버로 파일 전송
    #             ssh_upload_file(csv_file, remote_path, file_name)

    #             # 이후 AIModel 처리...

    #             return redirect('loading')
    #     else:
    #         print(form.errors)
    # else:
    #     form = DataForm()
    return render(request, 'write.html', {'form': 'form'})