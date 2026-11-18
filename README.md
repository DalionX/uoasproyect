# Clon de estudio — UOAS

Copia visual de `https://www.uoas.org.pe/` hecha con **HTML + CSS + JavaScript puro**, sin frameworks ni dependencias. Reproduce colores, tipografías, formas, tamaños, posiciones y comportamiento de los sliders. Incluye también las 12 páginas internas (Nosotros, siete sedes, Alianzas, Cómo Ayudar, Galería y Contacto), todas enlazadas desde el menú y el pie. Las fotografías originales se sustituyeron por imágenes libres; el logo es un SVG creado para este proyecto.

## Cómo verlo

1. Abre la carpeta `uoas-clone` en tu editor de código.
2. Haz doble clic en `index.html` (funciona sin servidor).
3. Si prefieres un servidor local, ejecuta en esta carpeta:
   - Con Python: `python -m http.server 8000` y entra en `http://localhost:8000`.
   - Con VS Code: instala la extensión **Live Server** y pulsa *Go Live*.

## Estructura

```
uoas-clone/
├── index.html                  → portada: sliders, aniversario, videos, misión e historia
├── nosotros.html               → página institucional
├── sede-*.html (7 archivos)    → fichas de las siete sedes
├── alianzas.html               → convenios y alianzas
├── como-ayudar.html            → formas de colaborar
├── galeria.html                → álbumes con visor de imágenes
├── contacto.html               → datos y formulario de demostración
├── assets/css/styles.css       → estilos, colores y media queries
├── assets/js/main.js           → sliders, menú, modal, galería y formulario
├── assets/img/logo-uoas.svg        → logo para la cabecera (original)
├── assets/img/logo-uoas-blanco.svg → logo para el hero (original)
├── DOCUMENTACION.md            → explicación línea a línea e inventario de imágenes
├── DOCUMENTACION.pdf           → la misma documentación en PDF, con el cuadro de programas
├── generar_documento.py        → plantilla Python para regenerar el PDF con el modelo visual
├── generar_pdf_navegador.html  → alternativa en JS si Python está bloqueado
├── verificar_pdf.html          → comprobador de tamaño, páginas y fuentes del PDF
├── ESTILO_DOCUMENTACION.md     → guía de estilo extraída del PDF de referencia
└── README.md                   → este archivo
```

## Documentación en PDF

Abre `DOCUMENTACION.pdf` para ver el resumen impreso en 4 páginas:

1. Qué se hizo y mapa de archivos (portada, páginas internas, CSS y JS).
2. Inventario de imágenes (SVG propios y fotos de Unsplash, con su página).
3. **Cuadro de programas y herramientas utilizadas** + flujo de trabajo.
4. Guía rápida de modificación, enlaces internos y aviso legal.

El PDF sigue el **modelo visual extraído del PDF de referencia** que adjuntaste: A4, Helvetica/Helvetica-Bold/Courier, tablas azules con filas alternas y código violeta. Los detalles están en `ESTILO_DOCUMENTACION.md`; las futuras documentaciones deben usar esa misma guía. Para regenerarlo, ejecuta `python generar_documento.py` en esta carpeta. Si Python está bloqueado, abre `generar_pdf_navegador.html`, pulsa *Descargar PDF* y guarda el archivo como `DOCUMENTACION.pdf`; con `verificar_pdf.html` puedes confirmar que tiene 4 páginas, 23.605 bytes, `xref` válido y las tres fuentes del modelo.

## Programas y herramientas utilizados

| Herramienta | Para qué se usó |
|---|---|
| **Navegador integrado de OpenCode (Chromium)** | Abrir la web original, leer su DOM, estilos computados, posiciones y textos; comprobar el resultado. |
| **webfetch** | Descargar el HTML original y sus reglas CSS para analizarlas. |
| **Visual Studio Code (recomendado)** | Editar HTML, CSS y JS. Cualquier editor de texto sirve: Notepad++, Sublime Text, Atom. |
| **Google Chrome / Firefox / Edge** | Probar el clon y la vista responsive. |
| **Python 3 o Live Server (opcional)** | Servir la carpeta por HTTP. |
| **SVG (XML)** | Crear los dos logos originales sin depender de imágenes con copyright. |
| **Unsplash** | Fuente de las fotografías bajo licencia gratuita. |

No se usó WordPress, Joomla ni gestores de paquetes: todo es estático.

## Cómo modificarlo

- **Cambiar colores:** edita las variables en `styles.css`, líneas 1-11 (`--azul`, `--naranja`, etc.).
- **Cambiar textos:** busca el texto en `index.html` y reemplázalo; los textos institucionales están en las líneas 112, 130, 144-145 y 186-194.
- **Cambiar fotos:** sustituye las URLs de Unsplash en `index.html` por tus archivos locales, por ejemplo `assets/img/mi-foto.jpg`. El inventario completo está en `DOCUMENTACION.md`.
- **Cambiar la velocidad del slider:** modifica `data-interval="5000"` en la línea 46 de `index.html` (milisegundos).
- **Añadir una sede:** copia `sede-escuela-hogar-ancon-de-ninas.html`, cambia el título, el `data-page` y los textos; luego añade el enlace en el menú (L28-L34) y en el listado del pie de todas las páginas.
- **Cambiar el texto de una sección interna:** abre el HTML correspondiente y edita los bloques `page-hero` y `section` (por ejemplo `alianzas.html` L46-L123).
- **Añadir un álbum:** copia un bloque `gallery-card` en `galeria.html` (L61-L109) y cambia la URL de Unsplash y la leyenda.
- **Cambiar tamaños responsive:** ajusta las media queries al final de `styles.css` (L552-L627 y L979-L996 para las páginas internas).

## Nota legal

Este proyecto es una **copia de estudio** de la estructura visual. No incluye los videos, logotipos ni fotografías originales de la institución. Las fotos proceden de Unsplash (licencia gratuita que permite uso comercial y modificación sin atribución obligatoria) y los SVG son creaciones originales hechas para este clon.
