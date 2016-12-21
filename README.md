# django_crud_scaffolding
scaffold (views actions, templates, model_forms, routes) code for your models by few django shell commands
<br>scaffold cruds for your models as fast start for your project
<br>@authors: Askao Ahmed Saad && Mahmoud Samy
<br>@contact:ahmedsaadkhames@gmail.com - mahmoudsamy18@gmail.com
<hr>
**requirements**<br>
- django project with apps containing models.
- add the desired apps to settings.INSTALLED_APPS.

<hr>
**Running the application from shell**<br><br>
- run django shell.
```
python manage.py shell
```
<br>
- run django_crud_scaffolding script.
```
import crud_scaffolding
```
<br>
- choose app number from your project installed apps list.
```
-------------------------------------------------------------------------------------------
 
Note >>>>any time you want to exit script , press Ctrl-C it kill process , 
 
-------------------------------------------------------------------------------------------
 
 >>>> all application in your project : 
1 - test_app
_________________________________________________________
 >>>> PLZ , Enter number of app you want to scaffold its models : 
```
<br>
- choose number of model you want to sacffold for it.
```
 >>>> application you want to scaffold its models is (test_app) >>> 
_________________________________________________________
 >>>> Models and its fields in your choosed application >>> 
1 - Option
['useroption', 'created', u'id', 'value', 'name']
2 - UserOption
['created', u'option_id', u'id', 'option', 'name']
_________________________________________________________
PLZ , Enter model number you want to scaffold : 
```
- choose which operation (action) you want to scaffold it's code.
```
_________________________________________________________
 >>>> choose operation you want to run on your chosed model (Option) >>> 
1 - List all
2 - Add
3 - Edit
4 - Delete
5 - View
6 - All operations
PLZ , Enter operation number you want to excute on ( Option ) :
```
<br>
- to exit the script at any time press Ctrl+C.
