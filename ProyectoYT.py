# A simple program to download mp3 from youtube.
#
#
# Made with kivy 2.0.0 and python 3.9.5
#
# First of all, click on top-right button and write download address. Once you do it once, it will stay saved.

import kivy
from kivy.config import Config
from kivy.uix.bubble import Bubble
Config.set('graphics', 'resizable', False) #We make window no resizable.
Config.set('graphics', 'width', '800') #We configure our window to 800x300.
Config.set('graphics', 'height', '400')
Config.set('input', 'mouse', 'mouse,multitouch_on_demand') #Disable multitouch (red dot on mouse right click.)
Config.set('kivy','window_icon','Logo.ico')
kivy.require('2.0.0')
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.textinput import Clipboard, TextInput
from kivy.core import text, clipboard
from kivy.uix.button import Button
from kivy.base import EventLoop
from kivy.uix.screenmanager import Screen, ScreenManager, NoTransition
import pytube
import os
import time

Builder.load_string("""
#:import Clipboard kivy.core.clipboard.Clipboard
<Inicio>:
    canvas.before:      
        Color:
            rgba: (204/255,193/255,193/255,1)
        Rectangle:
            pos: self.pos
            size: self.size
    FloatLayout:
        Label:
            text:"YouTube Downloader"
            pos_hint: {'center_x': 0.5, 'center_y': .90}
            color:"black"
            font_size:35

        Label:
            text:"Introduce la URL del video:"
            pos_hint: {'center_x': 0.2, 'center_y': .68}
            color:"black"
            font_size:25
        
        MenuTextInput:
            id:URL
            use_bubble: True
            multiline:False
            pos_hint: {'center_x': 0.5, 'center_y': .57}
            size_hint: 0.9, 0.1
            font_size:20
            on_text_validate: root.descargar()
            
        Button:
            text:"Descargar"
            size_hint: 0.2, 0.1
            pos_hint: {'center_x': 0.1485, 'center_y': .46}
            on_press: root.descargar()

        Label:
            id:Info
            text:""
            pos_hint: {'center_x': 0.50, 'center_y': .2}
            size_hint: 0.9, 0.05
            font_size: 20
            color:"black"

        Button:
            text:"Pegar enlace"
            size_hint: 0.15,0.08
            pos_hint: {'center_x': 0.875, 'center_y': .68}
            font_size:15
            on_release: URL.text= Clipboard.paste()

        Button:
            text:"···"
            size_hint: 0.075, 0.07
            pos_hint: {'center_x': 0.96, 'center_y': .96}
            font_size:30
            on_press: root.manager.current= 'config'

<MyConfig>
    canvas.before:      
        Color:
            rgba: (204/255,193/255,193/255,1)
        Rectangle:
            pos: self.pos
            size: self.size
    FloatLayout:
        Label:
            text:"Configuración"
            pos_hint: {'center_x': 0.5, 'center_y': .90}
            color:"black"
            font_size:35
                
        Label:
            text:"Introduce la ruta de guardado:"
            pos_hint: {'center_x': 0.23, 'center_y': .68}
            color:"black"
            font_size:25
        
        MenuTextInput:
            id:Destino
            use_bubble: True
            multiline:False
            pos_hint: {'center_x': 0.5, 'center_y': .57}
            size_hint: 0.9, 0.1
            font_size:20
            on_text_validate: 
                root.guardar()
                root.manager.current= 'inicio'

        Button:
            text:"Pegar dirección"
            size_hint: 0.15,0.08
            pos_hint: {'center_x': 0.875, 'center_y': .68}
            font_size:15
            on_release: Destino.text= Clipboard.paste()

        Button:
            text:"Salir sin guardar"
            size_hint: 0.25, 0.15
            pos_hint: {'center_x': 0.13, 'center_y': 0.08}
            font_size: 20
            on_press: 
                Destino.text=""
                root.manager.current= 'inicio'

        Button:
            text:"Guardar"
            size_hint: 0.15, 0.15
            pos_hint: {'center_x': 0.92, 'center_y': 0.08}
            font_size:20
            on_press: 
                root.guardar()
                root.manager.current= 'inicio'

    """)

class MenuTextInput(TextInput):   

    def on_touch_down(self, touch):

        super(MenuTextInput,self).on_touch_down(touch)

        if touch.button == 'right':
            pos = super(MenuTextInput,self).to_local(*self._long_touch_pos, relative=False)

            self._show_cut_copy_paste(
                pos, EventLoop.window, mode='paste')

class Inicio(Screen): #Main screen class with download method.
    def descargar(self):

        # Metemos la URL del video. // Save user URL as an object from pytube class called YouTube.
        MyURL=self.ids.URL.text
        try:
            yt = pytube.YouTube(MyURL)
            
            # Extraemos el audio. // We look for only audio streams for that URL.
            video = yt.streams.filter(only_audio=True).first()
            
            # Introducimos la dirección de destino. // We take destination from 'direccion.txt' archive.
            direccion= open('direccion.txt')
            midireccion= direccion.read()
            destination = midireccion
            
            # Descargamos el archivo // We download music in .mp4 format.
            out_file = video.download(destination)
            
            # Guardamos el archivo // We try to save it changing its format to .mp3.
            try:
                base, ext = os.path.splitext(out_file)
                new_file = base + '.mp3'
                os.rename(out_file, new_file)
            
                # Avisamos de haber terminado. // We display a message telling everything went OK.
                self.ids.Info.text=f"Se ha descargado:\n{yt.title}"

            #Si da error, avisamos al usuario y borramos el archivo duplicado. // If that archive already exists, we display an error and delete the mp4 archive.
            except:
                self.ids.Info.text="Error. Creemos que ese archivo ya existe."
                sobras=f"{destination}/{yt.title}.mp4".replace(",","").replace("|","")
                os.remove(sobras)
            self.ids.URL.text="" #Limpiamos el TextInput // We clean TextInput.
        except:
            pass

class MyConfig(Screen): #Config screen class, used to change destination address.
    def guardar(self):
        destino=self.ids.Destino.text
        if destino=="":
            pass
        else:
            configdestino= open('direccion.txt', 'w')
            configdestino.write(destino)
            configdestino.close()

class YTDownloader(App): #Main class to load app.
    def build(self):
        sm=ScreenManager(transition=NoTransition()) #Añadimos el screen manager. Configuramos para que no haya transición entre pantallas.
        sm.add_widget(Inicio(name='inicio')) #Añadimos las diferentes pantallas a la app.
        sm.add_widget(MyConfig(name='config'))
        return sm

if __name__ == '__main__':
    YTDownloader().run()

