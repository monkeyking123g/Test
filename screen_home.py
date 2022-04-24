from kivy.uix.screenmanager import Screen
from kivymd.uix.picker import MDTimePicker
from datetime import datetime, date
from db_conect import conn_db, total_month_add

class Windowferst(Screen):
    """Scermo home  for time"""
    def print_total(self):
        """Print total ore for month"""
        # data per mese
        date_month = self.datate_now()
        conn = conn_db()
        #create cursor 
        c = conn.cursor()
        # create query to insert the data
          
        total = self.sum_total(c, date_month)
            
        # print total ore 
        self.tot.title = f'tempo totale {str(total)}'
        conn.commit()
        conn.close()

    # return time
    def get_time(self, instance, time):
        '''add time dalle'''
        self.dalle.text = str(time)
        self.dalle_time = time
    
    # cancell
    def on_cancel(self,instance, time):
        self.dalle.text = "Cancel" 

    def show_time_picker(self, f1, f2):
        time_dialog = MDTimePicker()
        time_dialog.bind(on_cancel=f1,time=f2)
        time_dialog.open()
    
    def show_time_picker_dalle(self):
        self.show_time_picker(self.on_cancel, self.get_time)
        
    
    def get_time_alle(self, instance, time):
        '''add time alle'''
        self.alle.text = str(time)
        self.alle_time = time
    
    # cancell
    def on_cancel_alle(self,instance, time):

        self.alle.text = "Cancel" 

    def show_time_picker_alle(self):
        self.show_time_picker(self.on_cancel_alle, self.get_time_alle)
    
    def calculate(self):
        try: 
            dalle = self.dalle_time
            alle = self.alle_time
            datetime_add = datetime.now()
            self.result.text = "confirm"
            # data per mese
            date_month = self.datate_now()
            
            result = datetime.combine(date.today(), alle) - datetime.combine(date.today(), dalle)
            #result = datetime.strptime(str(alle),"%H:%M:%S") - datetime.strptime(str(dalle),"%H:%M:%S")
            #result = timedelta(minutes=alle) - timedelta(minutes=dalle)

            # trasforiamo da secondi in ore 
            total = result.total_seconds() / 60**2

            # connect sql
            conn = conn_db() 

            #create cursor 
            c = conn.cursor()
            # create query to insert the data
            insertQuery = """INSERT INTO time(datatime_add, ore_lavorative) VALUES (?, ?);"""
            c.execute(insertQuery, (datetime_add.date(), total))
            totals = self.sum_total(c, date_month)
        
            # aggiorna  tutto 
            self.tot.title = f'tempo totale {str(totals)}'
            self.dalle.text = "Dalle ore"
            self.alle.text  = "Alle ore"

            # close Database
            conn.commit()

            conn.close()
            # anulla time
            self.dalle_time =  None 
            self.alle_time = None
        except:
            self.result.text = "Non hai messo ora"

    def sum_total(self,d, data_now):
        """return total from month"""
        d.execute("SELECT strftime('%m/%Y', datatime_add ), SUM(ore_lavorative) from time WHERE strftime('%m/%Y', datatime_add ) = ?;", (data_now,))
        rows = d.fetchall()
        return rows[0][1]


    def add_month(self):
        """Add total month """
        date_month = self.datate_now()
        conn = conn_db() 
        c = conn.cursor()
        total = self.sum_total(c, date_month)

        total_sum_month = total_month_add()  
   
        total_sum_month(c, date_month, total)

        conn.commit()
        conn.close()

    def datate_now(self): 
        datetime_add = datetime.now() # date now 
        date_month = datetime_add.strftime('%m/%Y') # year and month
        return date_month
