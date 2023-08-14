from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import StringProperty, ColorProperty
from kivy.clock import Clock

from kivymd.app import MDApp
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog

import time
import openai
import threading

from database import Database

db = Database()


class SendMessage(MDBoxLayout):

    def response(self):

        user_chat = db.insert_data(self.ids.user_message.text, 'user')

        self.background_color = (23/255, 195/255, 206/255, 1)
        self.icon = 'account'
        self.color = (1, 1, 1, 1)
        self.identity_color = (23/255, 195/255, 206/255, 1)
        self.identity_bg = [1, 1, 1, 1]
        self.id_text_color = [1, 1, 1, 1]
        self.identity = 'Tristan'

        add_chat = Chats(
            text=user_chat[0], identity=self.identity, background_color=self.background_color, icon=self.icon, context_color=self.color, identity_color=self.identity_color, identity_bg=self.identity_bg, id_text_color=self.id_text_color)
        # return the created task details and create a list item
        MDApp.get_running_app().root.first.ids.listexpenses.add_widget(add_chat)

        self.ids.user_message.text = ''
        # Delay execution by 0.1 seconds
        Clock.schedule_once(lambda dt: self.bot_responsee(), 2)

    def validate_api(self):
        if not MDApp.get_running_app().root.first.ids.api_key_ai.text:
            self.error_dialog(
                message="Sorry, the application failed to establish a connection. Please try again.")
        else:
            openai.api_key = MDApp.get_running_app().root.first.ids.api_key_ai.text
            threading.Thread(target=self.response()).start()

    def error_dialog(self, message):

        close_button = MDFlatButton(
            text='CLOSE',
            text_color=[0, 0, 0, 1],
            on_release=self.close_dialog,
        )
        self.dialog = MDDialog(
            title='[color=#FF0000]Ooops![/color]',
            text=message,
            buttons=[close_button],
            auto_dismiss=False
        )
        self.dialog.open()

    # Close Dialog
    def close_dialog(self, obj):
        self.dialog.dismiss()

    def bot_responsee(self):

        # Bot Response
        time.sleep(2)  # Add a delay of 2 seconds (adjust as needed)

        # Bot Response
        prompt = self.ids.user_message.text
        model = "text-davinci-003"
        response = openai.Completion.create(
            engine=model, prompt=prompt, max_tokens=50)

        generated_text = response.choices[0].text.strip()

        bot_chat = db.insert_data(generated_text, 'bot')

        self.identity = 'Mara AI'
        self.background_color = (245/255, 245/255, 245/255, 1)
        self.icon = 'robot-happy-outline'
        self.color = [0, 0, 0, 1]
        self.identity_color = [1, 1, 1, 1]
        self.identity_bg = (23/255, 195/255, 206/255, 1)
        self.id_text_color = [0, 0, 0, 1]

        add_bot = Chats(
            text=bot_chat[0], identity=self.identity, background_color=self.background_color, icon=self.icon, context_color=self.color, identity_color=self.identity_color, identity_bg=self.identity_bg, id_text_color=self.id_text_color)
        # return the created task details and create a list item
        MDApp.get_running_app().root.first.ids.listexpenses.add_widget(add_bot)


class CustomLabel(MDLabel):
    pass


class Chats(MDCard):
    text = StringProperty()
    identity = StringProperty()
    background_color = ColorProperty()
    icon = StringProperty()
    context_color = ColorProperty()
    identity_color = ColorProperty()
    identity_bg = ColorProperty()
    id_text_color = ColorProperty()


class FirstWindow(Screen):

    Builder.load_file('firstwindow.kv')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Clock.schedule_once(self.create_tasks)

    def create_tasks(self, *args):

        history = db.get_data()
        if len(history) != 0:
            for i in history:
                if i[1] == 'user':
                    self.background_color = (23/255, 195/255, 206/255, 1)
                    self.icon = 'account'
                    self.color = (1, 1, 1, 1)
                    self.identity_color = (23/255, 195/255, 206/255, 1)
                    self.identity_bg = [1, 1, 1, 1]
                    self.id_text_color = [1, 1, 1, 1]
                    self.identity = 'Tristan'

                else:
                    self.identity = 'Mara AI'
                    self.background_color = (245/255, 245/255, 245/255, 1)
                    self.icon = 'robot-happy-outline'
                    self.color = [0, 0, 0, 1]
                    self.identity_color = [1, 1, 1, 1]
                    self.identity_bg = (23/255, 195/255, 206/255, 1)
                    self.id_text_color = [0, 0, 0, 1]
                add_expenses = Chats(
                    text=str(i[0]), identity=self.identity, background_color=self.background_color, icon=self.icon, context_color=self.color, identity_color=self.identity_color, identity_bg=self.identity_bg, id_text_color=self.id_text_color)

                self.ids.listexpenses.add_widget(add_expenses)


class WindowManager(ScreenManager):
    pass


class rawApp(MDApp):

    def build(self):

        return WindowManager()


if __name__ == '__main__':
    rawApp().run()
