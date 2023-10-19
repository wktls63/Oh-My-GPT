from django.shortcuts import render, redirect
from ..models import Data, AIModel
from ..forms import AIModelForm
import os

def upload_model(request):
    if request.method == 'POST':
        form = AIModelForm(request.POST, request.FILES)
        if form.is_valid():
            csv_file = request.FILES['file']

            file_name = csv_file.name
            file_path = os.path.join('path_to_save', file_name)
            with open(file_path, 'wb+') as destination:
                for chunk in csv_file.chunks():
                    destination.write(chunk)

            data_instance = Data(file_dir=file_path)
            data_instance.save()

            ai_model = form.save(commit=False)
            ai_model.user_id = request.user
            ai_model.data_id = data_instance
            ai_model.save()

            return redirect('loading')

    else:
        form = AIModelForm()
    return render(request, 'write.html', {'form': form})