from kivymd.uix.card import MDCardSwipe
from kivy.properties import StringProperty, NumericProperty

class SwipeToDeleteItemMonth(MDCardSwipe):
    '''Card with `swipe-to-delete` Month total.'''
    id_total_month = NumericProperty()
    text = StringProperty()

class SwipeToDeleteItemTime(MDCardSwipe):
    '''Card with `swipe-to-delete` Time of day .'''
    id_tempo = NumericProperty()

    text = StringProperty()