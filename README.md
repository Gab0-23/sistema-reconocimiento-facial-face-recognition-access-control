Facial Recognition Access Control System 
This project is a functional prototype developed as part of the Systems Engineering degree program. The objective is to automate access control for an educational institution by verifying student identity through facial recognition and checking their status against a database.

Key Features
User Registration: Captures personal data and photography via webcam in real-time.

Facial Encoding: Uses Deep Learning algorithms (face_recognition) to convert faces into unique biometric vectors (128-d).

Access Validation: Real-time comparison of the detected face against the database of enrolled students.

Graphical Interface: Interactive and touch-friendly UI developed with Kivy.

Visitor Registration: Manual module to register individuals external to the institution.

 Technologies Used
Language: Python 3.

Interface: Kivy (NUI Development Framework).

Computer Vision: OpenCV, face_recognition, NumPy.

Database: MySQL (mysql-connector-python).

 Prerequisites
Python 3.x installed.

Active MySQL server (e.g., XAMPP).

Functional webcam.

 Installation and Usage
1. Clone the repository:

Bash

git clone https://github.com/Gab0-23/YOUR-REPO.git
2. Install dependencies:

Bash

pip install -r requirements.txt
Note: Installing dlib (required for face_recognition) may require CMake and C++ compilers.

3. Import the database:

Create a database named prueba in your MySQL manager.

Import the estructura_bd.sql file included in this repository.

4. Run the application:

Bash

python InterfazRF.py
 Future Improvements (Scalability)
Payment API Integration: Connect the system with the actual administrative database to validate financial solvency in real-time.

Security: Encryption of sensitive data and migration of credentials to environment variables.

Logs: Detailed history of entry and exit times.

Author: Gabriel José González Mujica

-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

Sistema de Control de Acceso por Reconocimiento Facial 

Este proyecto es un prototipo funcional desarrollado como parte de la carrera de Ingeniería de Sistemas. El objetivo es automatizar el control de acceso a una institución educativa verificando la identidad del estudiante mediante reconocimiento facial y consultando su estado en una base de datos.



 Características Principales

Registro de Usuarios: Captura de datos personales y fotografía mediante cámara web en tiempo real.



Codificación Facial: Uso de algoritmos de Deep Learning (face_recognition) para convertir rostros en vectores biométricos únicos (128-d).



Validación de Acceso: Comparación en tiempo real del rostro detectado contra la base de datos de alumnos inscritos.



Interfaz Gráfica: UI interactiva y táctil desarrollada con Kivy.



Registro de Visitantes: Módulo manual para registrar personas externas a la institución.



Tecnologías Utilizadas

Lenguaje: Python 3.



Interfaz: Kivy (Framework de desarrollo NUI).



Visión Artificial: OpenCV, face_recognition, NumPy.



Base de Datos: MySQL (Conector mysql-connector-python).


 Pre-requisitos

Python 3.x instalado.



Servidor MySQL activo (ej. XAMPP).



Cámara web funcional.



 Instalación y Uso

Clonar el repositorio:



Bash



git clone https://github.com/Gab0-23/TU-REPOSITORIO.git

Instalar dependencias:



Bash



pip install -r requirements.txt

(Nota: Instalar dlib para face_recognition puede requerir CMake y compiladores de C++).



Importar la base de datos:



Crea una base de datos llamada prueba en tu gestor MySQL.



Importa el archivo estructura_bd.sql incluido en este repositorio.



Ejecutar la aplicación:



Bash



python InterfazRF.py

Futuras Mejoras (Escalabilidad)

Integración con API de Pagos: Conectar el sistema con la base de datos administrativa real para validar solvencia financiera en tiempo real.



Seguridad: Encriptación de datos sensibles y migración de credenciales a variables de entorno.



Logs: Historial detallado de horas de entrada y salida.



Autor: Gabriel José González Mujica