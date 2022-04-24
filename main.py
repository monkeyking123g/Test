# import tutte file.py

from screen_tu import WindowSecond
from delete import SwipeToDeleteItemMonth, SwipeToDeleteItemTime
from db_conect import conn_db
from screen_home import Windowferst

from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton

from kivy.lang import Builder
from kivy.core.window import Window
from kivymd.app import MDApp
from datetime import datetime, date, timedelta
from kivy.uix.screenmanager import  Screen
from kivy.uix.boxlayout import BoxLayout



class Content(BoxLayout):
   pass

class Windowfrie(Screen):
    pass



class Test(MDApp):
    dialog = None
    dialog_houre = None
    date_now = datetime.now()


    def build(self):
        self.icon = "Logo.png"
        date_month = self.date_now.strftime('%m/%Y')
        self.theme_cls.theme_style = "Light"
        # Create database or connect to on connect
        #conn = sqlite3.connect('time_db.db')
        con = conn_db()
        # Create a Cursor
        c = con.cursor()
        # create  a Table
        c.execute("""CREATE TABLE if not exists time(
            id integer PRIMARY KEY,
            datatime_add TIMESTAMP,
            ore_lavorative FLOAT)

        """)
        c.execute("""CREATE TABLE if not exists totale(
            id integer PRIMARY KEY,
            datatime_add TIMESTAMP,
            total_ore FLOAT)
            """)

        total = c.execute("SELECT strftime('%m/%Y', datatime_add ), SUM(ore_lavorative) from time WHERE strftime('%m/%Y', datatime_add ) = ?;", (date_month,))
        total = c.fetchall()

        # auto add total month
        if self.add_total() == True:
            self.total_month_add(c, self.date_now.date(), total[0][1])

        # commit our change
        con.commit()

        con.close()

        return Builder.load_file('main.kv')

    def on_swipe_complete(self, instance):
        '''Delete widget and time of sql '''
        WindowSecond.trach(self, instance)
        self.root.ids.second.dada.remove_widget(instance)
        self.root.ids.md_list_all.remove_widget(instance)

    def remove_item(self, instance):
        '''Delete widget and month of sql '''
        self.root.ids.md_list.remove_widget(instance)

    def add_month(self):
        """Add total month """
        date_month = self.date_now.strftime('%m/%Y')
        conn = conn_db()
        c = conn.cursor()
        total = c.execute("SELECT strftime('%m/%Y', datatime_add ), SUM(ore_lavorative) from time WHERE strftime('%m/%Y', datatime_add ) = ?;", (date_month,))
        total = c.fetchall()
        totale = total[0][1]

        self.total_month_add(c, date_month, totale)
        c.execute("SELECT * FROM totale;")
        rows = c.fetchall()
        nam = 0
        for i in rows:
            nam = i[0]
        print(nam)
        self.root.ids.md_list.add_widget(
                SwipeToDeleteItemMonth(text=f'{str(nam)}.  {str(date_month)} Totale  {str(totale)} ore', id_total_month=nam)
            )
       
        conn.commit()
        conn.close()

    def on_start(self):
        '''Creates a list of total month.'''
        conn = conn_db()
        c = conn.cursor()
        c.execute("SELECT * FROM totale;")
        nam = 0
        rows = c.fetchall()
        #c = self.date_now.strftime("%B %Y")
        for i in rows:
            nam += 1
            self.root.ids.md_list.add_widget(
                SwipeToDeleteItemMonth(text=f'{str(nam)}.  {str(i[1])} totale  {str(i[2])} ore', id_total_month=i[0])
            )
        c.execute('Select * from time;')
        rows2 = c.fetchall()
        nam2 = 0
        for i in rows2:
            nam2 += 1
            self.root.ids.md_list_all.add_widget(
                    SwipeToDeleteItemTime(text=f'{str(nam2)}.  {str(i[1])} ore  {str(i[2])}', id_tempo=i[0])
            )
        conn.commit()
        conn.close()

    def trach(self, instance):
        '''Delete widget an month total from db'''
        conn = conn_db()
        c = conn.cursor()
        print(instance.id_total_month)
        c.execute("DELETE FROM totale WHERE id = ?", (instance.id_total_month,))

        self.root.ids.md_list.remove_widget(instance)
        conn.commit()
        conn.close()


    def total_month_add(self, d, date_add, total):
        '''insert total in sqlite3
        '''
        insertQuery = """INSERT INTO  totale(datatime_add, total_ore) VALUES (?, ?);"""
        return d.execute(insertQuery, (date_add, total))

    def total_str(self):
        self.tot.title = f'tempo totale : {str(self.total[0][1])}'

    def last_day_of_month(self, any_day):
        # this will never fail
        # get close to the end of the month for any day, and add 4 days 'over'
        next_month = any_day.replace(day=28) + timedelta(days=4)
        # subtract the number of remaining 'overage' days to get last day of current month, or said programattically said, the previous day of the first of next month
        return next_month - timedelta(days=next_month.day)

    def add_total(self):
        for month in range(1, 13):
            if self.date_now.date() == self.last_day_of_month(date(2022, month, 1)):
                if str(self.date_now.strftime("%H:%M:%S")) == '20:30:00':
                    return True

        return False

    def cancel_dialog(self, obj):
        self.dialog.dismiss()

    def cancel_dialog2(self, obj):
        self.dialog_houre.dismiss()

    def add_dialog(self, obj):
        try:
            conn = conn_db()
            c = conn.cursor()
            ora =  float(self.dialog.content_cls.value.text)
            sql_update_query = "Update time set  ore_lavorative = ? where id = ?"
            c.execute(sql_update_query, (ora, self.id_widget))
            print(self.id_widget)
            conn.commit()
            conn.close()
            self.dialog.dismiss()
        except:
            self.dialog.content_cls.value.text = "formato richiesta non corretto !"

    def show_confirmation_dialog(self, g):
        """Open dialog of update hours"""

        if not self.dialog:
            self.dialog = MDDialog(
                title="Agiorna la data:",
                type="custom",
                content_cls=Content(),
                buttons=[
                    MDFlatButton(
                        text="CANCEL", text_color=self.theme_cls.primary_color,on_release=self.cancel_dialog
                    ),
                    MDFlatButton(
                        text="OK", text_color=self.theme_cls.primary_color, on_release=self.add_dialog
                    ),
                ],
            )
        self.id_widget = g.id_tempo
        print(g.id_tempo)
        self.dialog.open()

    def add_hours_for_day(self, obj):
        """ Add hours for day selected"""
        date = self.root.ids.second.tol_bar.title
        if date == "Data !":
            self.dialog_houre.content_cls.value.text = "non hai messo la data !"
        else:
            try:
                ora =  float(self.dialog_houre.content_cls.value.text)
                conn = conn_db()
                c = conn.cursor()

                    # create query to insert the data
                insertQuery = """INSERT INTO time(datatime_add, ore_lavorative) VALUES (?, ?);"""
                c.execute(insertQuery, (date, ora))
                conn.commit()
                conn.close()
                print("Ok")
                self.dialog_houre.dismiss()
            except:
                 self.dialog_houre.content_cls.value.text = "formato richiesta non corretto !"

            
         
    def show_confirmation_dialog2(self):
        ''' Open dialog from  "Agungi ore ". '''
        if not self.dialog_houre:
            self.dialog_houre = MDDialog(
                title="Agungi ore:",
                type="custom",
                content_cls=Content(),
                buttons=[
                    MDFlatButton(
                        text="CANCEL", text_color=self.theme_cls.primary_color,on_release=self.cancel_dialog2
                    ),
                    MDFlatButton(
                        text="OK", text_color=self.theme_cls.primary_color, on_release=self.add_hours_for_day
                    ),
                ],
            )
        self.dialog_houre.open()


Test().run()
