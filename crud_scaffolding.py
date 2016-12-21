'''
	django_crud_scaffolding script
	scaffold (views actions, templates, model_forms, routes) code for your models by few django shell commands
	scaffold cruds for your models as fast start for your project
	@authers: Askao Ahmed Saad && Mahmoud Samy
	@contact:ahmedsaadkhames@gmail.com - mahmoudsamy18@gmail.com
'''
import inspect, os
from django.apps import apps
from django.conf import settings
import sys


models_list = [] # models list
operations_list = ["List all", "Add", "Edit", "Delete", "View", "All operations"] # operations list
choosed_app = None
choosed_app_name = None
model_name = None
model_fields = []
first_use = False
app_models = None
apps_list = [] # applications list



'''
	add route to urls.py
'''
def add_route_to_urls(route_str):
	# read lines of urls.py file and put them in a list
	urlsfile_list = open(str(os.path.dirname(os.path.realpath(__file__)))+"/"+str(choosed_app_name)+"/urls.py").readlines()
	# define a newList and to append the new file updated string to it
	newList = []
	# loop on lines of urlsfile_list
	for line in urlsfile_list:
		# find the end square barcket of the urls list
		if line == ']':
			# if we get this end square barcket add our route before this line
			newList.append(route_str)
		# append this line to the newList
		newList.append(line)
	# write the newList (the new file updated string) in the urls.py file again 
	outref = open(str(os.path.dirname(os.path.realpath(__file__)))+"/"+str(choosed_app_name)+"/urls.py",'wb')
	outref.writelines(newList)
	outref.close()


'''
	generate the model form class in forms.py module file in wb mode
'''
def scaffold_ModelForm():
	# (wb mode) overwrites the file if the file exists. If the file does not exist, creates a new file for writing
	fo = open(str(os.path.dirname(os.path.realpath(__file__)))+"/"+str(choosed_app_name)+"/forms.py", "wb")
	fo.write("from django.forms import ModelForm\n"+
		"from .models import "+model_name+"\n"+
		"class "+model_name+"Form(ModelForm):\n\n"+
		"\tclass Meta:\n"+
		"\t\tmodel = "+model_name+"\n"+
		"\t\tfields = "+str(model_fields)
	);
	fo.close()


'''
	generate the views.py file with importted classes in wb mode
'''
def scaffold_viewsImports():
	# (wb mode) overwrites the file if the file exists. If the file does not exist, creates a new file for writing
	fo = open(str(os.path.dirname(os.path.realpath(__file__)))+"/"+str(choosed_app_name)+"/views.py", "wb")
	fo.write(
		"\nfrom django.shortcuts import redirect, render\n"+
		"from .models import "+model_name+"\n"+
		"from .forms import "+model_name+"Form\n\n"
		);
	fo.close()


'''
	generate the urls.py file with importted classes in wb mode
'''
def scaffold_urls_beginning():
	# (wb mode) overwrites the file if the file exists. If the file does not exist, creates a new file for writing
	fo = open(str(os.path.dirname(os.path.realpath(__file__)))+"/"+str(choosed_app_name)+"/urls.py", "wb")
	fo.write("from django.conf.urls import url\n"+
		"from . import views\n"+
		"urlpatterns = [\n"+
		"]"
	);
	fo.close()

'''
	generate "list_model_name" action in views.py in ab mode
'''
def scaffold_List():
	# append list action to the views.py file
	fo = open(str(os.path.dirname(os.path.realpath(__file__)))+"/"+str(choosed_app_name)+"/views.py", "ab")
	fo.write(
		"\n\ndef list"+model_name+"(request):\n"+
		"\t"+model_name+"s_list = "+model_name+".objects.all()\n"+
		"\treturn render(request, '"+model_name+"/list"+model_name+".html', {'"+
			model_name+"s_list':"+model_name+"s_list})"
	);
	fo.close()

	# append url route in urls.py
	route_str = "\turl(r'list"+model_name+"/', views.list"+model_name+", name='list"+model_name+"'),\n"
	add_route_to_urls(route_str)

	# check crud template folder is present, if not generate it 
	crud_template_path = str(os.path.dirname(os.path.realpath(__file__)))+"/"+str(choosed_app_name)+"/templates/"+model_name
	if not os.path.exists(crud_template_path):
		os.makedirs(crud_template_path)
	# generate list template in wb mode
	fo = open(str(os.path.dirname(os.path.realpath(__file__)))+"/"+str(choosed_app_name)+"/templates/"+model_name+
		"/list"+model_name+".html", "wb")
	theades = ''
	tfields = ''
	for field in model_fields:
		theades = theades+"\t\t<th>"+field+"</th>\n"
	for field in model_fields:
		tfields = tfields+"\t\t\t\t<td>{{"+model_name+"."+field+"}}</td>\n"
	fo.write("<h3>list "+model_name+"s</h3>\n"+
		"<table>\n"+
		"\t<thead>\n"+
		theades+
        "\t<th colspan='2'></th>\n"+
      	"\t</thead>\n"+
      	"\t<tbody>\n"+
      	"\t\t{% for "+model_name+" in "+model_name+"s_list %}\n"+
        "\t\t\t<tr>\n"+
        tfields+
        "\t\t\t\t<td colspan='2'>\n"+
        "\t\t\t\t\t<a href='{% url \"view"+model_name+"\" "+model_name+".pk %}'>view</a>\n"
        "\t\t\t\t\t<a href='{% url \"edit"+model_name+"\" "+model_name+".pk %}'>edit</a>\n"+
        "\t\t\t\t\t<a href='{% url \"delete"+model_name+"\" "+model_name+".pk %}'>delete</a>\n"+
        "\t\t\t\t</td>\n"+
        "\t\t\t</tr>\n"+
        "\t\t{% endfor %}\n"+
      	"\t</tbody>\n"+
    	"</table>\n"
	);
	fo.close()


'''
	generate "add_model_name" action in views.py in ab mode
'''
def scaffold_Add():
	# append add action to the views.py file
	fo = open(str(os.path.dirname(os.path.realpath(__file__)))+"/"+str(choosed_app_name)+"/views.py", "ab")
	fo.write(
		"\n\ndef add"+model_name+"(request):\n"+
		"\tif request.method == 'POST':\n"+
		"\t\tform = "+model_name+"Form(request.POST)\n"+
		"\t\tif form.is_valid():\n"+
	    "\t\t\tform.save()\n"+
	    "\t\t\treturn redirect('list"+model_name+"')\n"+
		"\telse:\n"+
		"\t\tform = "+model_name+"Form()\n"+
		"\treturn render(request, '"+model_name+"/add"+model_name+".html', {'form': form})"
		);
	fo.close()

	# append url route in urls.py
	route_str = "\turl(r'add"+model_name+"/', views.add"+model_name+", name='add"+model_name+"'),\n"
	add_route_to_urls(route_str)

	# check crud template folder is present, if not generate it 
	crud_template_path = str(os.path.dirname(os.path.realpath(__file__)))+"/"+str(choosed_app_name)+"/templates/"+model_name
	if not os.path.exists(crud_template_path):
		os.makedirs(crud_template_path)
	# generate add template in wb mode
	fo = open(str(os.path.dirname(os.path.realpath(__file__)))+"/"+str(choosed_app_name)+"/templates/"+model_name+
		"/add"+model_name+".html", "wb")
	fo.write("<h3>add "+model_name+"</h3>\n"+
		"<form action='' method='post'>\n"+
		"\t{% csrf_token %}\n"+
		"\t{{form}}\n"+
		"\t<input type='submit' value='submit'/>\n"+
		"\t</form>"
	);
	fo.close()


'''
	generate "edit_model_name" action in views.py in ab mode
'''
def scaffold_Edit():
	# append edit action to the views.py file
	fo = open(str(os.path.dirname(os.path.realpath(__file__)))+"/"+str(choosed_app_name)+"/views.py", "ab")
	fo.write(
		"\n\ndef edit"+model_name+"(request,pk):\n"+
		"\t"+model_name+"_instance = "+model_name+".objects.get(pk=pk)\n"+
		"\tif request.method == 'POST':\n"+
		"\t\tform = "+model_name+"Form(request.POST , instance="+model_name+"_instance)\n"+
		"\t\tif form.is_valid():\n"+
	    "\t\t\tform.save()\n"+
	    "\t\t\treturn redirect('list"+model_name+"')\n"+
		"\telse:\n"+
		"\t\tform = "+model_name+"Form(instance="+model_name+"_instance)\n"+
		"\treturn render(request, '"+model_name+"/edit"+model_name+".html', {'form': form, '"+
			model_name+"_instance':"+model_name+"_instance})"
		);
	fo.close()

	# append url route in urls.py
	route_str = "\turl(r'edit"+model_name+"/(?P<pk>\d+)/$', views.edit"+model_name+", name='edit"+model_name+"'),\n"
	add_route_to_urls(route_str)

	# check crud template folder is present, if not generate it 
	crud_template_path = str(os.path.dirname(os.path.realpath(__file__)))+"/"+str(choosed_app_name)+"/templates/"+model_name
	if not os.path.exists(crud_template_path):
		os.makedirs(crud_template_path)
	# generate edit template in wb mode
	fo = open(str(os.path.dirname(os.path.realpath(__file__)))+"/"+str(choosed_app_name)+"/templates/"+model_name+
		"/edit"+model_name+".html", "wb")

	fo.write("<h3>Edit "+model_name+"</h3>\n"+
		"<form action='' method='post'>\n"+
		"\t{% csrf_token %}\n"+
		"\t{{form}}\n"+
		"\t<input type='submit' value='submit'/>\n"+
		"\t</form>"
	);
	fo.close()

'''
	generate "view_model_name" action in views.py in ab mode
'''
def scaffold_View():
	# append view action to the views.py file
	fo = open(str(os.path.dirname(os.path.realpath(__file__)))+"/"+str(choosed_app_name)+"/views.py", "ab")
	fo.write(
		"\n\ndef view"+model_name+"(request,pk):\n"+
		"\t"+model_name+"_instance = "+model_name+".objects.get(pk=pk)\n"+
		"\treturn render(request, '"+model_name+"/view"+model_name+".html', {'"+
			model_name+"_instance':"+model_name+"_instance})"
		);
	fo.close()

	# append url route in urls.py
	route_str = "\turl(r'view"+model_name+"/(?P<pk>\d+)/$', views.view"+model_name+", name='view"+model_name+"'),\n"
	add_route_to_urls(route_str)

	# check crud template folder is present, if not generate it 
	crud_template_path = str(os.path.dirname(os.path.realpath(__file__)))+"/"+str(choosed_app_name)+"/templates/"+model_name
	if not os.path.exists(crud_template_path):
		os.makedirs(crud_template_path)

	# concatenate fields string
	fields_string = ''
	for field in model_fields:
		fields_string = fields_string +""+ field+" : {{"+model_name+"_instance."+field+"}}<br>\n"
	# generate view template in wb mode
	fo = open(str(os.path.dirname(os.path.realpath(__file__)))+"/"+str(choosed_app_name)+"/templates/"+model_name+
		"/view"+model_name+".html", "wb")

	fo.write("<h3>View "+model_name+"</h3>\n"+ fields_string
	);
	fo.close()

'''
	generate "delete_model_name" action in views.py in ab mode
'''
def scaffold_Delete():
	# append delete action to the views.py file
	fo = open(str(os.path.dirname(os.path.realpath(__file__)))+"/"+str(choosed_app_name)+"/views.py", "ab")
	fo.write(
		"\n\ndef delete"+model_name+"(request,pk):\n"+
		"\t"+model_name+"_instance = "+model_name+".objects.get(pk=pk)\n"+
		"\t"+model_name+"_instance.delete()\n"
		"\treturn redirect('list"+model_name+"')\n"
		);
	fo.close()

	# append url route in urls.py
	route_str = "\turl(r'delete"+model_name+"/(?P<pk>\d+)/$', views.delete"+model_name+", name='delete"+model_name+"'),\n"
	add_route_to_urls(route_str)

# *************************************************************


print "-------------------------------------------------------------------------------------------"
print " "
print "Note >>>>any time you want to exit script , press Ctrl-C it kill process , "
print " "
print "-------------------------------------------------------------------------------------------"
print " "





try:
	while True:
		print " >>>> all application in your project : "

		for app in settings.INSTALLED_APPS:
			appNameArr = app.split('.')
			if 'django' in appNameArr:
				pass
			else:
				apps_list.append(app) # add "app name"
				print str(apps_list.index(app) + 1)+  " - " + app # print "model_name" model

		print "_________________________________________________________"
		# ############################################################################
		# 1- choose application to scaffold its models 
		try:
			app_number = int(raw_input(' >>>> PLZ , Enter application number you want to scaffold its models : '))
			print " >>>> application you want to scaffold its models is (%s) >>> "  % apps_list[app_number - 1]
		except IndexError:
			print " >>>> No application with this number"
			continue

		choosed_app = apps.get_app_config(apps_list[app_number - 1]) # choose app

		choosed_app_name = choosed_app.name #get the choosed app name as a string

		print "_________________________________________________________"

		# ############################################################################
		# 2- choose model from your chosed application to scaffold 

		models_list = [] # models list


		# get all models in choosed app
		app_models = choosed_app.models


		# loop on all models in the choosed app
		print " >>>> Models and its fields in your choosed application >>> "

		# loop on "model_name= model name" and "model_class = model fields"
		for model_name, model_class in app_models.iteritems():
		        models_list.append(str(model_class.__name__)) # add "model_names" models name
		        print str(models_list.index(model_class.__name__) + 1)+  " - " + str(model_class.__name__) # print "model_name" model
		        print model_class._meta.get_all_field_names() # print "values" all fields name
		print "_________________________________________________________"

		# choose a particular model from all models
		try:
			model_number = int(raw_input('PLZ , Enter model number you want to scaffold : '))
			model_name = models_list[model_number - 1]
			print " >>>> Model you want to scaffold is >>> " + model_name
			# get fields of th choosed model class
			model_fields = app_models[model_name.lower()]._meta.get_all_field_names()
		except IndexError:
			print " >>>> No model with this number"
			continue


		# ############################################################################

		# 3- choose operations from operations list to run on a choosed model
		print "_________________________________________________________"


		print " >>>> choose operation you want to run on your chosed model (%s) >>> "  % models_list[model_number - 1]
		for op in operations_list:
			print str(operations_list.index(op) + 1)+ " - " + op

		# chose a particular operation from all operations
		try:
			operation_number = int(raw_input('PLZ , Enter operation number you want to excute on ( %s ) : ' % models_list[model_number - 1]))
			print "Operation you want to excute is (%s) >>> " % operations_list[operation_number - 1]

			# ********  excute the operaion *********
			#check if we first use this script to create modelform and imports one not more
			if first_use == False:
				scaffold_ModelForm()
				scaffold_viewsImports()
				scaffold_urls_beginning()
				first_use = True

			if operation_number == 1:
				scaffold_List()
			if operation_number == 2:
				scaffold_Add()
			if operation_number == 3:
				scaffold_Edit()
			if operation_number == 4:
				scaffold_Delete()
			if operation_number == 5:
				scaffold_View()
			if operation_number == 6:
				scaffold_List()
				scaffold_Add()
				scaffold_Edit()
				scaffold_Delete()
				scaffold_View()
			# *****************************************

		except IndexError:
			print "No operation with this number"
			continue
		print "_________________________________________________________"

		# check all operations status

# pressing Ctrl-C raise KeyboardInterrupt "take us outside loop"
except KeyboardInterrupt:
    sys.exit()

