# Dashboard de Ventas - Bodega El Porvenir

Estudiante: Luis Atto
Curso: Programacion Avanzada para la Ciencia de Datos
Fecha: Mayo 2025

Aplicacion web desarrollada con Streamlit para visualizar las ventas
de una bodega local en Miraflores, Lima, durante el primer semestre de 2024.

## Estructura del proyecto

tarea_streamlit/
├── app.py

├── requirements.txt
├── README.md
├── data/
│   └── datos.csv
└── evidencias/

## Como ejecutar

1. Crear y activar el entorno virtual:
   python3 -m venv venv
   source venv/bin/activate

2. Instalar dependencias:
   pip install -r requirements.txt

3. Ejecutar la aplicacion:
   streamlit run app.py --server.address 0.0.0.0 --server.port 8501

4. Abrir en el navegador:
   - Desde el equipo: http://localhost:8501
   - Desde el celular: http://<IP_LOCAL>:8501

## Verificacion del servidor

   ps aux | grep streamlit
   ss -tulpn | grep 8501

## Dataset

Archivo: data/datos.csv
Campos: fecha, producto, categoria, cantidad, precio_unitario, total, vendedor, distrito
Registros: 60 ventas de enero a junio 2024
