Sistema de Gestión de Inventario para Cafeterías (API & Dashboard)
📌 Descripción del Proyecto
Este proyecto es un prototipo de backend desarrollado para optimizar la gestión de inventarios en cafeterías de alto volumen. A través de una API RESTful y una base de datos relacional, el sistema automatiza el seguimiento de insumos (Clasificación ABC) y renderiza un panel de control visual para facilitar la toma de decisiones de reabastecimiento en tiempo real.

🎯 Problema a Resolver
Las operaciones de alto volumen en cafeterías (manejando múltiples cuentas simultáneas) requieren un control estricto de las mermas y existencias. La gestión manual es ineficiente y propensa a errores que afectan la rentabilidad y la disponibilidad de los productos clave, dificultando la visibilidad del stock crítico.

🛠️ Tecnologías Utilizadas
Lenguaje: Python

Framework Backend: FastAPI

ORM & Base de Datos: SQLAlchemy (SQLite integrado)

Frontend / Visualización: HTML & CSS embebido

Servidor ASGI: Uvicorn

⚙️ Metodología (Qué Hice)
Diseño de Base de Datos: Modelado de tablas relacionales (products, inventory_counts, menu_items) usando SQLAlchemy para rastrear productos por unidad base y categoría ABC.

Desarrollo de API: Creación de la estructura base de la aplicación con FastAPI.

Simulación de Datos: Implementación de un script de inicialización (boot_system) para poblar la base de datos con inventario y recetas de prueba.

Dashboard Dinámico: Construcción de un endpoint principal (/) que realiza consultas SQL agregadas y renderiza tarjetas HTML con indicadores de colores según el nivel de stock (Verde: Óptimo, Amarillo: Medio, Rojo: Crítico).

📊 Resultados y Aprendizajes
Se construyó un sistema capaz de automatizar el seguimiento de insumos de manera eficiente.

Las alertas visuales en el dashboard permiten identificar instantáneamente qué productos requieren atención, optimizando la cadena de suministro local.

El uso de FastAPI demuestra la capacidad de crear arquitecturas web escalables y de rápida ejecución.
