from delete import SwipeToDeleteItemTime
from kivymd.uix.picker import  MDDatePicker
from kivy.uix.screenmanager import Screen
from db_conect import conn_db

class WindowSecond(Screen):
    def on_save(self, instance, value, date_range):

        data = value
        date_input = str(data)
        self.ids.tol_bar.title = date_input
        # connect sql
        conn = conn_db()

         #create cursor
        c = conn.cursor()
        # create query to insert the data
        c.execute("SELECT * from time WHERE datatime_add =?", (date_input,))
        rows = c.fetchall()
        i = 0
        for data_s in rows:
            i += 1
            self.ids.dada.add_widget(
                SwipeToDeleteItemTime(text=f'{str(i)}.  tempo aggiunto {str(data_s[2])}', id_tempo=data_s[0])
                )
        conn.commit()
        conn.close()

    def on_cancel(self, instance, value):
        '''Events called when the "CANCEL" dialog box button is clicked.'''
        self.ids.tol_bar.title = "Data !"
        
        for i in  range(len(self.ids.dada.children)):
            for widget in self.ids.dada.children:
                self.ids.dada.remove_widget(widget)


    def show_date_picker(self):
        date_dialog = MDDatePicker()
        date_dialog.bind(on_save=self.on_save, on_cancel=self.on_cancel)
        date_dialog.open()

    def trach(self, instance):
        '''Delete widget an month time from db'''
        conn = conn_db()
        c = conn.cursor()
        print(instance.id_tempo)

        c.execute("DELETE FROM time WHERE id = ?", (instance.id_tempo,))
        conn.commit()
        conn.close()

    
