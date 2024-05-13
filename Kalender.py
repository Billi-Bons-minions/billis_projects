import tkinter as tk
from tkinter import messagebox
from tkcalendar import Calendar,DateEntry
import sqlite3

def show(event):
    def delete():
        conn = sqlite3.connect("entrys.db")
        selected_index = liste.curselection()
        selected_event = liste.get(selected_index)
        selected_event = selected_event.replace("Datum: ", "")
        selected_event = selected_event.replace("Ereignis: ", "")
        selected_date, selected_title = selected_event.split(", ")
        conn.execute("DELETE FROM entrys WHERE Datum=? AND Überschrift=?",(selected_date, selected_title))
        conn.commit()
        conn.close()
        load()
        show_event.destroy()
    conn = sqlite3.connect("entrys.db")
    cursor = conn.cursor()
    selected_index = liste.curselection()
    if selected_index:
        selected_event = liste.get(selected_index)
        selected_event = selected_event.replace("Datum: ", "")
        selected_event = selected_event.replace("Ereignis: ","")
        selected_date, selected_title = selected_event.split(", ")
        cursor.execute("SELECT Datum, Überschrift, Beschreibung FROM entrys WHERE Datum=? AND Überschrift=?", (selected_date, selected_title))
        selected_event = cursor.fetchone()
        date, title, description = selected_event
        conn.close()
    show_event=tk.Tk()
    show_event.title("Ereignis")
    show_event.geometry(f"{screen_x//4}x{screen_y//4}")
    show_y=screen_y//4
    show_y=show_y*0.035
    show_event.resizable(False,False)
    show_date=tk.Label(show_event,text=date).pack()
    show_title=tk.Label(show_event,text=title).pack()
    show_description=(tk.Text(show_event,width=(screen_x//4),height=show_y))
    show_description.pack()
    show_description.insert('1.0', description)
    show_description['state'] = 'disabled'
    delete_button=tk.Button(show_event,text="Löschen",command=delete).pack()
    show_event.mainloop()

def load():
    liste.delete(0,tk.END)
    cursor = verb.execute("SELECT Datum,Überschrift FROM entrys")
    for i in cursor:
        liste.insert(tk.END,f"Datum: {i[0]}, Ereignis: {i[1]}")
def add_entry(event):
    def beenden(uberschrift,beschreigung_eingabe):
        selected_date = calender.selection_get()
        Ueberschrift=uberschrift
        if not Ueberschrift.strip():
            messagebox.showerror("Fehler","Keine gültige Überschrift")
            eintrag.destroy()
            return


        Beschreibung = beschreibung_eingabe.get("1.0", "end")
        verb.execute("INSERT INTO entrys (Datum, Überschrift, Beschreibung) VALUES (?,?,?)",(selected_date, Ueberschrift, Beschreibung))
        verb.commit()
        load()
        eintrag.destroy()
    eintrag = tk.Tk()
    eintrag.title("Eintrag")
    eintrag.geometry(f"{screen_x//4}x{screen_y//4}")
    eintrag.resizable(False,False)
    show_y = screen_y // 4
    show_y = show_y * 0.03
    ueberschrift = tk.Label(eintrag,text="Überschrift:")
    ueberschrift.pack()
    überschrift_eingabe = tk.Entry(eintrag)
    überschrift_eingabe.pack(fill="x")
    beschreibung = tk.Label(eintrag,text="Beschreibung:")
    beschreibung.pack()
    beschreibung_eingabe = tk.Text(eintrag,width=(screen_x//4),height=show_y)
    beschreibung_eingabe.pack()
    eingabe = tk.Button(eintrag,text="Speichern",command=lambda:beenden(überschrift_eingabe.get(),beschreibung_eingabe))
    eingabe.pack()
    #eintrag.mainloop()

root = tk.Tk()
root.title("Kalender")
screen_x=root.winfo_screenwidth()
screen_y=root.winfo_screenheight()
listbox = root.winfo_reqheight()//2
listbox=listbox//12
root.geometry(f"{screen_x//2}x{screen_y}+0+0")
calender = Calendar(master=root,selectmode="day")
calender.pack(fill="both",expand=True)
root.bind("<<CalendarSelected>>",add_entry)
liste = tk.Listbox(root,font=12,height=listbox)
liste.pack(fill=tk.BOTH,expand=True)
liste.bind("<<ListboxSelect>>",show)
verb = sqlite3.connect("entrys.db")
verb.execute("CREATE TABLE IF NOT EXISTS entrys (id INTEGER PRIMARY KEY AUTOINCREMENT, Datum TEXT, Überschrift TEXT, Beschreibung TEXT);")
load()
root.mainloop()