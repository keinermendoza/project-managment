# Progress Managment
This is a management tool, focused on communicating project progress and receiving feedback.

## Admin

las acciones importantes como crear proyectos, tareas y editar permisos de usuarios son posibles solo atraves del admin.

la edicion se hace atraves de los formularios integrados de django, la configuracion esta en el admin.py de la app progress.

### Tareas

las tareas tienen un periodo de realizacion estimado que debe ser declarado al crearse. Cuando una tarea es marcada como "Working on" la propiedad "get_time_to_finish" es calculada mostrando el tiempo en el que la tarea deberia estar lista, en caso de que el estatus de la tarea sea marcada como completed o como waiting el valor de esta propiedad sera seteado a null.  

### Privacidad de un Proyecto

el modelo de proyecto tiene una propiedad "public" que permite compartir un projecto con todos los usuarios registrados sin importar si estos estan asignados a dicho projecto, si esta propiedad es seteada como False solo los usuarios asignados al proyecto podran interactuar con el

### Notas
Al crear una nota desde el admin no es necesario marcar el usuario, el usuario actual es detectado. si se edita una nota se mantiene el usuario original.

### Views

Agregué una vista personalizada al admin que permite visualizar la informacion del proyecto de forma unificada. ésta esta registrada dentro de la aplicacion progress.

## Stack