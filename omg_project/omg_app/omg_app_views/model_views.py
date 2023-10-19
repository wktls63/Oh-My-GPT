from django.shortcuts import render, redirect
from ..models import Data, AIModel
from ..forms import AIModelForm, DataForm
import os

def upload_model(request):
    if request.method == 'POST':
        form = DataForm(request.POST, request.FILES)
        if form.is_valid() or 'file_dir' in request.FILES:
            csv_file = request.FILES.get('file_dir', None)
            if csv_file:
                file_name = csv_file.name
                file_path = os.path.join('path_to_save', file_name)
                
                if not os.path.exists('path_to_save'):
                    os.makedirs('path_to_save')
                    
                with open(file_path, 'wb+') as destination:
                    for chunk in csv_file.chunks():
                        destination.write(chunk)

                data_instance = Data(file_dir=file_path)
                data_instance.save()
                
                # 이후 AIModel 처리...

                return redirect('loading')
        else:
            print(form.errors)
    else:
        form = DataForm()
    return render(request, 'write.html', {'form': form})