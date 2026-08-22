import json
import os
import tkinter as tk
from tkinter import messagebox,simpledialog
from datetime import datetime
import re
import sys
if getattr(sys,'frozen',False):
   BASE_DIR=os.path.dirname(sys.executable)
else:
     BASE_DIR=os.path.dirname(os.path.abspath(__file__))
SAVE_FILE=os.path.join(BASE_DIR,"To-Do.json")
task_list=[]
root=tk.Tk()
root.geometry("600x600")
root.resizable(False,False)
root.title("Advanced To-Do list")
is_dark_mode=False
entry=tk.Entry(root,font=("Arial",12),width=20)
entry.pack(pady=10,fill="x",padx=5)
def toggle_theme():
    global is_dark_mode
    if is_dark_mode:
        root.config(bg="white")
        entry.config(bg="white",fg="black",insertbackground="black")
        search_entry.config(bg="white",fg="black",insertbackground="black")
        box.config(bg="white",fg="black")
        theme_btn.config(text="Light Mode",bg="#a0a0a0",fg="white")
    else:
        root.config(bg="#1e1e1e")
        entry.config(bg="#1e1e1e",fg="white",insertbackground="white")
        search_entry.config(bg="#a0a0a0",fg="white",insertbackground="white")
        box.config(bg="#a0a0a0",fg="white")
        theme_btn.config(text="Dark Mode",bg="white",fg="black")
    is_dark_mode= not is_dark_mode
    
def save_task():
    if len(task_list)==0:
       messagebox.showinfo("INFO","Saving an empty task list.")
       return
    try:
        with open(SAVE_FILE,"w") as file:
           json.dump(task_list,file,indent=4)
    except Exception as e:
        messagebox.showerror("Error",f"Failed to save file: {e}")
    
def counter_task():
    total_task=len([task for task in task_list if not task.strip().upper().startswith("[DONE]")])
    counter_label.config(text=f"Total Task : {total_task}")
    
def load_task():
    global task_list
    if os.path.exists(SAVE_FILE):
        try:
            with open(SAVE_FILE,"r") as file:
                task_list=json.load(file)
            box.delete(0,tk.END)
            for task in task_list:
                box.insert(tk.END,task)
                current_index=box.size() - 1
                if "[High]" in task:
                    box.itemconfig(current_index,fg="red")
                elif "[Low]" in task:
                    box.itemconfig(current_index,fg="royalblue")
            counter_task()
        except FileNotFoundError:
             task_list=[]
    else:
       task_list=[] 
            
def add_task():
    task=entry.get().strip()
    if task !="":
        priority=priority_combobox.get()
        current_time=datetime.now().strftime("%Y-%m-%d %H:%M")
        formatted_task=f"[{priority}] {task} (Added : {current_time})"
        if priority == "High":
            box.insert(tk.END,formatted_task)
            box.itemconfig(tk.END,fg="red")
        elif priority == "Low":
            box.insert(tk.END,formatted_task)
            box.itemconfig(tk.END,fg="royalblue")
        else:
            box.insert(tk.END,formatted_task)
        task_list.append(formatted_task)
        entry.delete(0,tk.END)
        save_task()
        counter_task()
    else:
        messagebox.showwarning("Warning","Empty task cannot be added!")
        
def del_task():
    try:
        selected_box=box.curselection()[0]
        box.delete(selected_box)
        task_list.pop(selected_box)
        save_task()
        counter_task()
    except IndexError:
        messagebox.showwarning("Warning","Please select a task to delete it!")
        
def clear_all_task():
    global task_list
    if len(task_list) == 0:
       messagebox.showinfo("Empty List","The list box is already empty.")
       return 
    confirm=messagebox.askyesno("Confirm Delete","You are sure you want to delete all tasks?")
    if confirm:
        box.delete(0,tk.END)
        task_list.clear()
        save_task()
        counter_task()
        
def edit_task():
    try:
        selected_box=box.curselection()[0]
        current_task=box.get(selected_box)
        is_done ="[DONE]" in current_task
        match=re.search(r"\[(High|Medium|Low)\]",current_task)
        current_priority=match.group(1) if match else priority_combobox.get()
        clear_task=re.sub(r"^(\[(DONE|High|Medium|Low)\]\s*)+","",current_task)
        clear_task=re.sub(r"\s*\(Added\s*:.*?\)","",clear_task).strip()
        new_task=simpledialog.askstring("Edit task","Update your task",initialvalue=clear_task)
        if new_task and new_task.strip() !="":
            priority=current_priority
            current_time=datetime.now().strftime("%Y-%m-%d %H:%M")
            done_prefix="[DONE]" if is_done else""
            formatted_task=f"{done_prefix}[{priority}] {new_task.strip()} (Added : {current_time})"
            if selected_box < len(task_list):
               task_list[selected_box]=formatted_task
            box.delete(selected_box)
            box.insert(selected_box,formatted_task)
            if priority == "High":
                box.itemconfig(selected_box,fg="red")
            elif priority == "Low":
                box.itemconfig(selected_box,fg="royalblue")
            else:
                box.insert(selected_box)
            save_task()
        elif new_task is not None and new_task.strip() == "":
            messagebox.showwarning("Warning","Empty task cannot be added!")
    except IndexError:
        messagebox.showwarning("Warning","Please select a task to be edit!")
        
def mark_task():
    try:
        selected_box=box.curselection()[0]
        current_task=box.get(selected_box)
        if  current_task.startswith("[DONE]"):
            update_task=current_task.replace("[DONE] ","",1)
        else:
            update_task="[DONE] " + current_task
        task_list[selected_box]=update_task
        box.delete(selected_box)
        box.insert(selected_box,update_task)
        if "[High]" in update_task:
           box.itemconfig(selected_box,fg="red")
        elif "[Low]" in update_task:
           box.itemconfig(selected_box,fg="royalblue")
        save_task()
        counter_task()
    except IndexError:
        messagebox.showwarning("Warning","Please select a task to mark it!")
        
def filter_task():
    search=search_entry.get().strip().lower()
    box.delete(0,tk.END)
    for task in task_list:
        clean_task=re.sub(r"^(?:\[.*?\]\s*)+","",task)
        clean_task=clean_task.split("(Added")[0].strip().lower()
        if search == "" or search in clean_task:
          box.insert(tk.END,task)
          current_index=box.size() - 1
          if "[High]" in task:
            box.itemconfig(current_index,fg="red")
          elif "[Low]" in task:
            box.itemconfig(current_index,fg="royalblue")

def show_all_list():
    try:
       box.delete(0,tk.END)
       if len(task_list)==0:
          messagebox.showinfo("Empty list","The listbox is already empty.")
          counter_task()
          return
       for task in task_list:
           box.insert(tk.END,task)
           current_index=box.size() - 1
           if "[High]" in task:
              box.itemconfig(current_index,fg="red")
           elif "[Low]" in task:
              box.itemconfig(current_index,fg="royalblue")
       counter_task() 
    except Exception as e:
        messagebox.showerror("Error",f"An error occurred: {e}")
from tkinter import ttk
priority_combobox=ttk.Combobox(root,values=["High","Medium","Low"],state="readonly")
priority_combobox.set("Medium")
priority_combobox.pack()
entry.bind("<Return>",lambda event :add_task())
frame=tk.Frame(root)
frame.pack(pady=5)
add_btn=tk.Button(root,text="Add Text",command=add_task,font=("Arial",10),bg="navy",fg="gold")
add_btn.pack(pady=5)
search_entry=tk.Entry(frame,font=("Arial",12),width=18)
search_entry.pack(side=tk.LEFT,padx=2)
search_btn=tk.Button(frame,text="Search",command=filter_task,font=("Arial",10),bg="yellow",fg="black")
search_btn.pack(side=tk.LEFT,padx=2)
box=tk.Listbox(root,font=("Arial",12),width=80,height=10)
box.pack(pady=5,fill="x",padx=5)
counter_label=tk.Label(root,text="Total Task : 0",font=("Arial",10),bg="darkblue",fg="white")
counter_label.pack(pady=5)
frame=tk.Frame(root)
frame.pack(pady=5)
del_btn=tk.Button(frame,text="Delete task",command=del_task,font=("Arial",12),bg="green",fg="lightgreen")
del_btn.grid(row=0,column=0,pady=5)
mark_btn=tk.Button(frame,text="Mark Completed",command=mark_task,font=("Arial",10),bg="black",fg="white")
mark_btn.grid(row=0,column=3,padx=10,pady=5)
edit_btn=tk.Button(frame,text="Edit Text",command=edit_task,font=("Arial",10),bg="blue",fg="cyan")
edit_btn.grid(row=0,column=5,padx=10,pady=5)
theme_btn=tk.Button(frame,text="Light Mode",command=toggle_theme,bg="#a0a0a0",fg="white",font=("Arial",10))
theme_btn.grid(row=2,column=0,pady=5)
clear=tk.Button(frame,text="Clear All tasks",command=clear_all_task,font=("Arial",10),bg="red",fg="black")
clear.grid(row=2,column=3,padx=10,pady=5)
show_all=tk.Button(frame,text="Show all tasks",command=show_all_list,font=("Arial",10),bg="gold",fg="black")
show_all.grid(row=2,column=5,pady=5,padx=10)
load_task()
root.mainloop()
