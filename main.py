import os
import threading
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.clock import mainthread
from kivy.utils import platform
import yt_dlp

class TikTokDLApp(App):
    def build(self):
        if platform == 'android':
            from android.permissions import request_permissions, Permission
            request_permissions([
                Permission.INTERNET,
                Permission.WRITE_EXTERNAL_STORAGE,
                Permission.READ_EXTERNAL_STORAGE
            ])

        layout = BoxLayout(orientation='vertical', padding=40, spacing=25)

        self.titulo = Label(
            text="Descargador TikTok (Motor yt-dlp)",
            font_size='20sp',
            size_hint=(1, 0.2)
        )
        layout.add_widget(self.titulo)

        self.url_input = TextInput(
            hint_text="Pega aquí el enlace de TikTok...",
            multiline=False,
            size_hint=(1, 0.2),
            font_size='16sp'
        )
        layout.add_widget(self.url_input)

        self.btn_video = Button(
            text="Descargar Video (MP4)",
            size_hint=(1, 0.2),
            background_color=(0.99, 0.17, 0.33, 1),
            font_size='18sp'
        )
        self.btn_video.bind(on_press=lambda x: self.iniciar_descarga(solo_audio=False))
        layout.add_widget(self.btn_video)

        self.estado = Label(
            text="Esperando enlace...",
            font_size='15sp',
            size_hint=(1, 0.4)
        )
        layout.add_widget(self.estado)

        return layout

    def iniciar_descarga(self, solo_audio=False):
        url = self.url_input.text.strip()
        if not url:
            self.actualizar_estado("[-] Pega un enlace válido primero.")
            return

        self.btn_video.disabled = True
        self.actualizar_estado("[+] Extrayendo con yt-dlp...")
        threading.Thread(target=self.descargar_hilo, args=(url, solo_audio), daemon=True).start()

    def descargar_hilo(self, url, solo_audio):
        try:
            # Ruta de la carpeta Descargas en Android
            carpeta_descargas = "/storage/emulated/0/Download"
            if not os.path.exists(carpeta_descargas):
                carpeta_descargas = os.getcwd()

            ydl_opts = {
                'format': 'best',
                'outtmpl': os.path.join(carpeta_descargas, 'TikTok_%(id)s.%(ext)s'),
                'nocheckcertificate': True,
            }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])

            self.actualizar_estado("[¡Éxito!] Guardado en tu carpeta Descargas.")
        except Exception as e:
            self.actualizar_estado(f"[-] Error: {str(e)[:80]}")
        finally:
            self.habilitar_boton()

    @mainthread
    def actualizar_estado(self, texto):
        self.estado.text = texto

    @mainthread
    def habilitar_boton(self):
        self.btn_video.disabled = False

if __name__ == '__main__':
    TikTokDLApp().run()
