
from django.shortcuts import redirect, render
from .models import Option
from .forms import OptionForm



def listOption(request):
	Options_list = Option.objects.all()
	return render(request, 'Option/listOption.html', {'Options_list':Options_list})