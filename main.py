import json
import argparse
import os
from datetime import datetime 

archivo = "tasks.json"
currentTime=datetime.today()
currentTime=currentTime.strftime("%y-%m-%d %H:%M")

def load_tasks():
     if os.path.exists(archivo):
        with open(archivo,"r") as file:
           tareas= json.load(file)
           return tareas   
     return []

def save_task(tasks):
    with open(archivo,"w") as f:
        json.dump(tasks,f,indent=3)

def add_task(desc):
    tasks=load_tasks()
    task={"id": len(tasks)+1,"descripcion":desc,"status":"todo","add-date":currentTime,"update-date":currentTime}
    tasks.append(task)
    print(desc+" agregado a la lista de tareas")
    save_task(tasks)

def update_task(id,description):
    tasks = load_tasks()
    if id>len(tasks):
        print("tarea no encontrada")
    else:
        for task in tasks:
            if task["id"]==id:
                task["descripcion"]=description
                task["update-date"]=currentTime
    print("tarea actualizada")
    save_task(tasks)
    
def delete_task(id):
    tasks=load_tasks()
    new_tasks=[]
    i=1
    if id>len(tasks):
        print("tarea no encontrada")
    else:
        for task in tasks:
            if task["id"]!=id:
                task["id"]=i
                new_tasks.append(task)
                i+=1
        save_task(new_tasks)
        print("tarea eliminada correctamente")

def list_tasks(status):
    tasks=load_tasks()

    if status==None:
        for task in tasks:
            print("tarea "+str(task["id"])+": \n descripcion: "+task["descripcion"]+"\n estado: "+task["status"]+"\n fecha de creacion: "+task["add-date"]+"\n ultima actualizacion: "+task["update-date"])
    else:
             for task in tasks:
                 if status==task["status"]:
                     print("tarea "+str(task["id"])+": \n descripcion: "+task["descripcion"]+"\n estado: "+task["status"]+"\n fecha de creacion: "+task["add-date"]+"\n ultima actualizacion: "+task["update-date"])

def mark_tasks(command,idTask):
    tasks=load_tasks()
    if idTask>len(tasks):
        print("tarea no encontrada")
    else:
        status=(command.split("-",1))
        for task in tasks:
                if task["id"]==idTask:
                    task["status"]=status[1]
        save_task(tasks)


def main():
    parser = argparse.ArgumentParser(description="Task List CLI")
    subparsers = parser.add_subparsers(dest="command")

    # Comando: add
    add_parser = subparsers.add_parser("add", help="Agregar una tarea")
    add_parser.add_argument("description", help="Descripción de la tarea")

    # Comando: list
    listTasks = subparsers.add_parser("list", help="Listar todas las tareas")
    listTasks.add_argument("status",nargs="?",help="motrar una lista de las tareas")
    # Comando: delete
    delete_parser = subparsers.add_parser("delete", help="Eliminar una tarea")
    delete_parser.add_argument("idDelete", type=int, help="ID de la tarea")

    update_parser = subparsers.add_parser("update", help="actualizar una tarea")
    update_parser.add_argument("taskIdToUpdate", type=int, help="id e la tarea a actualizar")
    update_parser.add_argument("newDescription")

    mark_in_progress_parser=subparsers.add_parser("mark-in-progress",help="marcar como en progreso")
    mark_in_progress_parser.add_argument("taskId",type=int,help="id de tarea")
    mark_done_parser =subparsers.add_parser("mark-done",help="marcar como hecho")
    mark_done_parser.add_argument("taskId",type=int,help="id de tarea")

    args = parser.parse_args()

    if args.command == "add":
        add_task(args.description)
    elif args.command=="update":
        update_task(args.taskIdToUpdate,args.newDescription)
    elif args.command=="delete":
        delete_task(args.idDelete)
    elif args.command=="list":
        list_tasks(args.status)
    elif args.command=="mark-in-progress" or args.command=="mark-done":
        mark_tasks((args.command),args.taskId)

    else:
        parser.print_help()

if __name__ == "__main__":
    main()




