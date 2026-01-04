from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window
from kivy.uix.widget import Widget
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from kivy.graphics import Color, RoundedRectangle, Rectangle
import connection_bd
import cv2
import numpy as np
import os
from kivy.clock import Clock
import threading
import face_recognition
import mysql.connector
from PIL import Image as PILImage
import io
from kivy.core.image import Image as CoreImage

class MainScreen(Screen):
    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', spacing=60, padding=8)
        
        btn_registro = Button(text="Registro", size_hint=(None, None), size=(200, 100),
                              background_color=(1, 1, 1, 0.5), color=(1, 1, 1, 1), font_size='18sp')
        btn_registro.bind(on_press=self.go_to_registro)
        
        btn_consulta = Button(text="Consulta", size_hint=(None, None), size=(200, 100),
                              background_color=(1, 1, 1, 0.5), color=(1, 1, 1, 1), font_size='18sp')
        btn_consulta.bind(on_press=self.go_to_consulta)
        
        btn_registro_visitante = Button(text="Registro de Visitante", size_hint=(None, None), size=(200, 100),
                                        background_color=(1, 1, 1, 0.5), color=(1, 1, 1, 1), font_size='18sp')
        btn_registro_visitante.bind(on_press=self.go_to_registro_visitante)

        h_layout_registro = BoxLayout(orientation='horizontal', padding=[50, 0, 50, -90])
        h_layout_registro.add_widget(Widget())
        h_layout_registro.add_widget(btn_registro)
        h_layout_registro.add_widget(Widget())
        
        h_layout_consulta = BoxLayout(orientation='horizontal', padding=[50, 0, 50, 11])
        h_layout_consulta.add_widget(Widget())
        h_layout_consulta.add_widget(btn_consulta)
        h_layout_consulta.add_widget(Widget())
        
        h_layout_registro_visitante = BoxLayout(orientation='horizontal', padding=[50, 0, 50, 110])
        h_layout_registro_visitante.add_widget(Widget())
        h_layout_registro_visitante.add_widget(btn_registro_visitante)
        h_layout_registro_visitante.add_widget(Widget())
        
        layout.add_widget(h_layout_registro)
        layout.add_widget(h_layout_consulta)
        layout.add_widget(h_layout_registro_visitante)
        
        self.add_widget(layout)
    
    def go_to_registro(self, instance):
        self.manager.current = 'registro'
    
    def go_to_consulta(self, instance):
        self.manager.current = 'consulta'
    
    def go_to_registro_visitante(self, instance):
        self.manager.current = 'registro_visitante'

class RegistroScreen(Screen):
    def __init__(self, **kwargs):
        super(RegistroScreen, self).__init__(**kwargs)
        self.captured_image_path = None
        self.imagen_bytes = None
        layout = FloatLayout()
        
        with layout.canvas.before:
            Color(0.4, 0.6, 0.8, 0.2)
            self.rect = RoundedRectangle(pos=(200, 90), size=(397, 420), radius=[(30, 30)])
        
        label1 = Label(text="Nombre:", size_hint=(None, None), size=(200, 40),
                       color=(1, 1, 1, 1), font_size='18sp', pos=(180, 455))
        self.text_input1 = TextInput(size_hint=(None, None), size=(300, 34), font_size='18sp', pos=(250, 425))
        
        label2 = Label(text="Apellido:", size_hint=(None, None), size=(200, 40),
                       color=(1, 1, 1, 1), font_size='18sp', pos=(180, 355))
        self.text_input2 = TextInput(size_hint=(None, None), size=(300, 34), font_size='18sp', pos=(250, 325))
        
        label3 = Label(text="Cedula:", size_hint=(None, None), size=(200, 40),
                       color=(1, 1, 1, 1), font_size='18sp', pos=(180, 255))
        self.text_input3 = TextInput(size_hint=(None, None), size=(300, 34), font_size='18sp', pos=(250, 225))
        
        btn_opcion1 = Button(text="Escaneo", size_hint=(None, None), size=(150, 60),
                             background_color=(0.2, 0.6, 1, 1), color=(1, 1, 1, 1), font_size='18sp', pos=(248, 115))
        btn_opcion1.bind(on_press=self.start_registro_facial)
        
        btn_opcion2 = Button(text="Enviar registro", size_hint=(None, None), size=(150, 60),
                             background_color=(0.2, 0.6, 1, 1), color=(1, 1, 1, 1), font_size='18sp', pos=(400, 115))
        btn_opcion2.bind(on_press=self.enviar_registro)

        btn_volver = Button(text="Volver", size_hint=(None, None), size=(100, 40),
                            background_color=(0.2, 0.6, 1, 1), color=(1, 1, 1, 1), font_size='14sp', pos=(10, 10))
        btn_volver.bind(on_press=self.go_back)
        
        layout.add_widget(label1)
        layout.add_widget(self.text_input1)
        layout.add_widget(label2)
        layout.add_widget(self.text_input2)
        layout.add_widget(label3)
        layout.add_widget(self.text_input3)
        layout.add_widget(btn_opcion1)
        layout.add_widget(btn_opcion2)
        layout.add_widget(btn_volver)
        
        self.add_widget(layout)
        
    def start_registro_facial(self, instance):
        if not self.text_input3.text.strip():
            print("Primero ingresa la cédula")
            return
        threading.Thread(target=self.registro_facial, daemon=True).start()

    def registro_facial(self):
        cap = cv2.VideoCapture(0)
        captured_image = None
        
        while True:
            ret, frame = cap.read()
            if ret:
                cv2.imshow('Registro Facial', frame)
                key = cv2.waitKey(1)
                if key == 27:
                    captured_image = frame
                    break
        
        cap.release()
        cv2.destroyAllWindows()
        
        if captured_image is not None:
            _, buffer = cv2.imencode('.jpg', captured_image)
            self.imagen_bytes = buffer.tobytes()
            cedula = self.text_input3.text.strip()
            filename = f"rostros/{cedula}.jpg"
            
            if not os.path.exists("rostros"):
                os.makedirs("rostros")
            
            cv2.imwrite(filename, captured_image)
            self.captured_image_path = filename

    def enviar_registro(self, instance):
        nombre = self.text_input1.text.strip()
        apellido = self.text_input2.text.strip()
        cedula = self.text_input3.text.strip()

        if not all([nombre, apellido, cedula]):
            print("Todos los campos son obligatorios")
            return
    
        if not self.imagen_bytes or not self.captured_image_path:
            print("Debe capturar una imagen primero")
            return
        
        try:
            face_image = face_recognition.load_image_file(self.captured_image_path)
            face_encodings = face_recognition.face_encodings(face_image)
            
            if not face_encodings:
                print("No se detectó un rostro en la imagen")
                return
            
            face_encoding = face_encodings[0].tobytes()
        except Exception as e:
            print(f"Error al procesar la imagen: {e}")
            return

        if connection_bd.insertar_datos(nombre, apellido, cedula, self.imagen_bytes, face_encoding):
            print("Registro exitoso!")
            self.text_input1.text = ""
            self.text_input2.text = ""
            self.text_input3.text = ""
            self.imagen_bytes = None
        else:
            print("Error al guardar el registro")
    
    def go_back(self, instance):
        self.manager.current = 'main'

class ConsultaScreen(Screen):
    def __init__(self, **kwargs):
        super(ConsultaScreen, self).__init__(**kwargs)
        self.captured_encoding = None
        layout = FloatLayout()
        
        with layout.canvas.before:
            Color(0.4, 0.6, 0.8, 0.2)
            self.rect = RoundedRectangle(pos=(85, 90), size=(397, 420), radius=[(30, 30)])
        
        self.picture_box = Image(size_hint=(None, None), size=(190, 200), pos=(548, 260))
        self.label_picture = Label(text="", size_hint=(None, None), size=(190, 80),
                                   color=(1, 1, 1, 1), font_size='22sp', pos=(548, 150))
        
        with self.label_picture.canvas.before:
            Color(0.5, 0, 0, 1)
            Rectangle(pos=self.label_picture.pos, size=self.label_picture.size)
        
        label1 = Label(text="Nombre:", size_hint=(None, None), size=(200, 40),
                       color=(1, 1, 1, 1), font_size='18sp', pos=(65, 455))
        self.text_input1 = TextInput(size_hint=(None, None), size=(300, 34), font_size='18sp', pos=(135, 425))
        
        label2 = Label(text="Apellido:", size_hint=(None, None), size=(200, 40),
                       color=(1, 1, 1, 1), font_size='18sp', pos=(65, 355))
        self.text_input2 = TextInput(size_hint=(None, None), size=(300, 34), font_size='18sp', pos=(135, 325))
        
        label3 = Label(text="Cedula:", size_hint=(None, None), size=(200, 40),
                       color=(1, 1, 1, 1), font_size='18sp', pos=(65, 255))
        self.text_input3 = TextInput(size_hint=(None, None), size=(300, 34), font_size='18sp', pos=(135, 225))
        
        btn_opcion1 = Button(text="Escaneo", size_hint=(None, None), size=(150, 60),
                             background_color=(0.2, 0.6, 1, 1), color=(1, 1, 1, 1), font_size='18sp', pos=(133, 115))
        btn_opcion1.bind(on_press=self.start_consulta_facial)
        
        btn_opcion2 = Button(text="Consulta", size_hint=(None, None), size=(150, 60),
                             background_color=(0.2, 0.6, 1, 1), color=(1, 1, 1, 1), font_size='18sp', pos=(285, 115))
        btn_opcion2.bind(on_press=self.realizar_consulta)

        btn_volver = Button(text="Volver", size_hint=(None, None), size=(100, 40),
                            background_color=(0.2, 0.6, 1, 1), color=(1, 1, 1, 1), font_size='14sp', pos=(10, 10))
        btn_volver.bind(on_press=self.go_back)
        
        layout.add_widget(label1)
        layout.add_widget(label2)
        layout.add_widget(label3)
        layout.add_widget(self.text_input1)
        layout.add_widget(self.text_input2)
        layout.add_widget(self.text_input3)
        layout.add_widget(btn_opcion1)
        layout.add_widget(btn_opcion2)
        layout.add_widget(self.picture_box)
        layout.add_widget(self.label_picture)
        layout.add_widget(btn_volver)
        
        self.add_widget(layout)

    def start_consulta_facial(self, instance):
        threading.Thread(target=self.consulta_facial, daemon=True).start()

    def consulta_facial(self):
        cap = cv2.VideoCapture(0)
        captured_image = None
        
        while True:
            ret, frame = cap.read()
            if ret:
                cv2.imshow('Consulta Facial', frame)
                key = cv2.waitKey(1)
                if key == 27:
                    captured_image = frame
                    break
        
        cap.release()
        cv2.destroyAllWindows()
        
        if captured_image is not None:
            rgb_image = cv2.cvtColor(captured_image, cv2.COLOR_BGR2RGB)
            face_locations = face_recognition.face_locations(rgb_image)
            
            if face_locations:
                self.captured_encoding = face_recognition.face_encodings(rgb_image, face_locations)[0]
                Clock.schedule_once(lambda dt: self.mostrar_imagen_capturada(captured_image))

    def mostrar_imagen_capturada(self, frame):
        buffer = cv2.imencode('.jpg', frame)[1].tobytes()
        image_data = io.BytesIO(buffer)
        img = PILImage.open(image_data)
        self.picture_box.texture = self.pil_a_textura(img)

    def pil_a_textura(self, pil_img):
        image_bytes = io.BytesIO()
        pil_img.save(image_bytes, format='png')
        image_bytes.seek(0)
        core_image = CoreImage(image_bytes, ext='png')
        return core_image.texture

    def realizar_consulta(self, instance):
        if self.captured_encoding is None:
            print("Primero captura un rostro")
            return

        conexion = connection_bd.get_connection()
        if not conexion:
            print("Error al conectar a la base de datos")
            return

        try:
            cursor = conexion.cursor()
            cursor.execute("""
                SELECT nombre, apellido, cedula_de_identidad, foto, face_encoding 
                FROM alumnos 
                WHERE face_encoding IS NOT NULL
            """)
            resultados = cursor.fetchall()
            
            for row in resultados:
                nombre, apellido, cedula, foto_blob, encoding_blob = row
                
                try:
                    encoding_almacenado = np.frombuffer(encoding_blob, dtype=np.float64)
                    coincidencia = face_recognition.compare_faces(
                        [encoding_almacenado], 
                        self.captured_encoding,
                        tolerance=0.6
                    )
                    
                    if coincidencia[0]:
                        Clock.schedule_once(lambda dt: self.actualizar_ui(nombre, apellido, cedula, foto_blob))
                        Clock.schedule_once(lambda dt: self.actualizar_estado("Permitido", (0, 0.7, 0, 1)))
                        return
                except Exception as e:
                    print(f"Error procesando {nombre} {apellido}: {e}")
        except Exception as e:
            print(f"Error al realizar la consulta: {e}")


        Clock.schedule_once(lambda dt: self.actualizar_estado("Denegado", (0.7, 0, 0, 1)))

    def actualizar_ui(self, nombre, apellido, cedula, foto_blob):
        self.text_input1.text = nombre
        self.text_input2.text = apellido
        self.text_input3.text = cedula
        
        img_pil = PILImage.open(io.BytesIO(foto_blob))
        self.picture_box.texture = self.pil_a_textura(img_pil)

    def actualizar_estado(self, texto, color):
        self.label_picture.text = texto
        self.label_picture.canvas.before.clear()
        with self.label_picture.canvas.before:
            Color(*color)
            Rectangle(pos=self.label_picture.pos, size=self.label_picture.size)

    def go_back(self, instance):
        self.manager.current = 'main'

class RegistroVisitanteScreen(Screen):
    def __init__(self, **kwargs):
        super(RegistroVisitanteScreen, self).__init__(**kwargs)
        # Usamos FloatLayout para posicionar los elementos manualmente
        layout = FloatLayout()
        
        # Cuadro de fondo con esquinas redondeadas
        with layout.canvas.before:
            Color(0.4, 0.6, 0.8, 0.2)  # Color azul claro con mayor transparencia (RGBA)
            self.rect = RoundedRectangle(pos=(100, 90), size=(397, 420), radius=[(30, 30)])  # Esquinas redondeadas
        
        # Labels y TextInputs con posiciones personalizadas
        label1 = Label(text="Nombre:", size_hint=(None, None), size=(200, 40),
                       color=(1, 1, 1, 1), font_size='18sp', pos=(80, 455))
        self.text_input1 = TextInput(size_hint=(None, None), size=(300, 34), font_size='18sp', pos=(150, 425))
        
        label2 = Label(text="Apellido:", size_hint=(None, None), size=(200, 40),
                       color=(1, 1, 1, 1), font_size='18sp', pos=(80, 355))
        self.text_input2 = TextInput(size_hint=(None, None), size=(300, 34), font_size='18sp', pos=(150, 325))
        
        label3 = Label(text="Cedula:", size_hint=(None, None), size=(200, 40),
                       color=(1, 1, 1, 1), font_size='18sp', pos=(80, 255))
        self.text_input3 = TextInput(size_hint=(None, None), size=(300, 34), font_size='18sp', pos=(150, 225))
        
        # Label y TextInput adicionales
        label4 = Label(text="Motivo de Visita:", size_hint=(None, None), size=(200, 40),
                       color=(1, 1, 1, 1), font_size='18sp', pos=(116, 155))
        self.text_input4 = TextInput(size_hint=(None, None), size=(300, 34), font_size='18sp', pos=(150, 125))
        
        # Botones principales con posiciones personalizadas
        
        btn_opcion2 = Button(text="Enviar registro", size_hint=(None, None), size=(200, 100),
                             background_color=(0.2, 0.6, 1, 1), color=(1, 1, 1, 1), font_size='18sp', pos=(550, 245))
        btn_opcion2.bind(on_press=self.enviar_registro)  # Asociar función al botón
        
        # Botón de volver (más pequeño) en la esquina inferior izquierda
        btn_volver = Button(text="Volver", size_hint=(None, None), size=(100, 40),
                            background_color=(0.2, 0.6, 1, 1),  # Mismo color que los otros botones
                            color=(1, 1, 1, 1), font_size='14sp', pos=(10, 10))
        btn_volver.bind(on_press=self.go_back)
        
        # Agregar todos los widgets al FloatLayout
        layout.add_widget(label1)
        layout.add_widget(self.text_input1)
        layout.add_widget(label2)
        layout.add_widget(self.text_input2)
        layout.add_widget(label3)
        layout.add_widget(self.text_input3)
        layout.add_widget(label4)
        layout.add_widget(self.text_input4)
        layout.add_widget(btn_opcion2)
        layout.add_widget(btn_volver)
        
        self.add_widget(layout)
    
    def go_back(self, instance):
        self.manager.current = 'main'

    def enviar_registro(self, instance):
        # Obtener los datos de los campos de texto
        nombre = self.text_input1.text.strip()
        apellido = self.text_input2.text.strip()
        cedula = self.text_input3.text.strip()
        razon_de_visita = self.text_input4.text.strip()
        
        # Validar que todos los campos estén llenos
        if not all([nombre, apellido, cedula, razon_de_visita]):
            print("Todos los campos son obligatorios")
            return
        
        # Insertar los datos en la base de datos
        if self.insertar_visita(nombre, apellido, cedula, razon_de_visita):
            print("Registro de visitante exitoso!")
            # Limpiar los campos después de guardar
            self.text_input1.text = ""
            self.text_input2.text = ""
            self.text_input3.text = ""
            self.text_input4.text = ""
        else:
            print("Error al guardar el registro")
    
    def insertar_visita(self, nombre, apellido, cedula, razon_de_visita):
        try:
            conexion = connection_bd.get_connection()
            if not conexion:
                print("Error al conectar a la base de datos")
                return False
            
            cursor = conexion.cursor()
            
            # Query para insertar en la tabla visitas
            query = """
                INSERT INTO visitas (nombre, apellido, cedula, razon_de_visita)
                VALUES (%s, %s, %s, %s)
            """
            valores = (nombre, apellido, cedula, razon_de_visita)
            
            cursor.execute(query, valores)
            conexion.commit()
            print("Datos de visitante insertados correctamente")
            return True
            
        except mysql.connector.Error as err:
            print(f"Error de MySQL: {err}")
            return False
            
        finally:
            if 'conexion' in locals() and conexion.is_connected():
                cursor.close()
                conexion.close()

class MiApp(App):
    def build(self):
        Window.size = (800, 600)
        Window.clearcolor = (0.0, 0.0, 0.2, 1)
        
        sm = ScreenManager()
        sm.add_widget(MainScreen(name='main'))
        sm.add_widget(RegistroScreen(name='registro'))
        sm.add_widget(ConsultaScreen(name='consulta'))
        sm.add_widget(RegistroVisitanteScreen(name='registro_visitante'))        
        return sm

if __name__ == "__main__":
    MiApp().run()