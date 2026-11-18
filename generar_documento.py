#!/usr/bin/env python3
# Genera DOCUMENTACION.pdf con el modelo visual extraido del PDF de referencia:
# A4, Helvetica/Courier, azul marino #12315A, azul #1D4E89, gris #F4F7FB,
# bordes #B8C4D6, codigo violeta #8A2BE2 y tablas con cabecera azul + cebra.

from pathlib import Path

SALIDA = Path(__file__).with_name("DOCUMENTACION.pdf")
NL = "\n"
BS = "\\"

# Colores en formato PDF (0..1), copiados del archivo de referencia.
C = {
    "navy": ".070588 .192157 .352941",   # #12315A
    "blue": ".113725 .305882 .537255",   # #1D4E89
    "black": "0 0 0",
    "violet": ".541176 .168627 .886275", # #8A2BE2
    "white": "1 1 1",
    "zebra": ".956863 .968627 .984314",  # #F4F7FB
    "border": ".721569 .768627 .839216", # #B8C4D6
}
FUENTE = {"cuerpo": "/F1", "titulo": "/F2", "codigo": "/F3"}
X = 56.69291
ANCHO = 481.8898
ALTO_PAGINA = 790


def esc(s):
    """Escapa parentesis y barras invertidas para cadenas literal de PDF."""
    return s.replace(BS, BS + BS).replace("(", BS + "(").replace(")", BS + ")")


def wrap(s, n):
    """Divide un texto en lineas de como maximo n caracteres."""
    salida = []
    actual = ""
    for palabra in s.split(" "):
        candidata = (actual + " " + palabra).strip()
        if len(candidata) > n and actual:
            salida.append(actual)
            actual = palabra
        else:
            actual = candidata
    if actual:
        salida.append(actual)
    return salida


class Pagina:
    def __init__(self):
        self.comandos = []
        self.y = ALTO_PAGINA

    def texto(self, color, fuente, size, x, y, s):
        self.comandos.append(
            f"{color} rg {fuente} {size} Tf 1 0 0 1 {x} {y} Tm ({esc(s)}) Tj"
        )

    def titulo(self, s):
        self.texto(C["navy"], FUENTE["titulo"], 20, X, self.y, s)
        self.y -= 30

    def seccion(self, s):
        self.y -= 12
        self.texto(C["blue"], FUENTE["titulo"], 14, X, self.y, s)
        self.y -= 24

    def cuerpo(self, s):
        for linea in wrap(s, 95):
            self.texto(C["black"], FUENTE["cuerpo"], 9.5, X + 13, self.y, linea)
            self.y -= 13
        self.y -= 4

    def lista(self, s, numero=None):
        marca = f"{numero}." if numero else BS + "225"
        self.texto(C["black"], FUENTE["cuerpo"], 9.5, X, self.y, marca)
        lineas = wrap(s, 88)
        for i, linea in enumerate(lineas):
            self.texto(C["black"], FUENTE["cuerpo"], 9.5, X + 13, self.y - i * 13, linea)
        self.y -= 13 * len(lineas) + 3

    def tabla(self, cabeceras, filas, anchos, columnas_codigo=()):
        x = X
        alto_cabecera = 16
        total = ANCHO
        top = self.y
        self.comandos.append(
            f"{C['blue']} rg {x} {self.y} {total} {alto_cabecera} re f"
        )
        cx = x + 6
        for i, cabecera in enumerate(cabeceras):
            self.texto(
                C["white"], FUENTE["titulo"], 8, cx, self.y + 5, cabecera
            )
            cx += anchos[i]
        self.y -= alto_cabecera
        separadores = [self.y]
        for r, fila in enumerate(filas):
            celdas = [
                wrap(str(valor), max(1, int(anchos[i] / 4.3)))
                for i, valor in enumerate(fila)
            ]
            nlineas = max(len(c) for c in celdas)
            alto = max(16, 8 + nlineas * 10)
            fondo = C["zebra"] if r % 2 else C["white"]
            self.comandos.append(
                f"{fondo} rg {x} {self.y - alto} {total} {alto} re f"
            )
            cc = x + 6
            for i, celda in enumerate(celdas):
                color = C["violet"] if i in columnas_codigo else C["black"]
                fuente = FUENTE["codigo"] if i in columnas_codigo else FUENTE["cuerpo"]
                for k, linea in enumerate(celda):
                    self.texto(
                        color, fuente, 8, cc, self.y - 9 - k * 10, linea
                    )
                cc += anchos[i]
            self.y -= alto
            separadores.append(self.y)
        self.comandos.append(
            f"{C['border']} RG .4 w {x} {self.y} {total} {top - self.y} re S"
        )
        for sy in separadores[1:-1]:
            self.comandos.append(
                f"{C['border']} RG .4 w {x} {sy} m {x + total} {sy} l S"
            )
        cx = x
        for ancho in anchos[:-1]:
            cx += ancho
            self.comandos.append(
                f"{C['border']} RG .4 w {cx} {self.y} m {cx} {top} l S"
            )
        self.y -= 14


def construir_paginas():
    paginas = []

    p = Pagina()
    p.titulo("DOCUMENTACION - CLON UOAS")
    p.cuerpo("Copia de estudio de https://www.uoas.org.pe/ | HTML5 + CSS3 + JavaScript puro")
    p.seccion("1. Que se hizo y con que")
    p.lista("Origen: se leyo la estructura real del sitio (menu, secciones, textos y enlaces).")
    p.lista("Tecnologias: HTML5, CSS3 (Grid, Flexbox, variables CSS y media queries) y JavaScript puro.")
    p.lista("Sin librerias ni frameworks: se abre con doble clic en index.html.")
    p.lista("Codigo comentado linea a linea con el prefijo L en los tres archivos.")
    p.lista("Imagenes: fotografias libres de Unsplash y dos logos SVG dibujados para el clon.")
    p.lista("No se copiaron las fotos, logos ni videos originales de la institucion.")
    p.lista("Se anadieron 12 paginas internas enlazadas desde el menu y el pie.")
    p.seccion("2. Mapa de archivos")
    p.tabla(
        ["Archivo", "Rol", "Contenido"],
        [
            ["index.html", "HTML", "Portada con 7 slides, aniversario, videos, mision, historia y pie."],
            ["nosotros.html", "HTML", "Historia, mision, vision, valores, objetivos y registros."],
            ["sede-*.html (7)", "HTML", "Fichas de las siete sedes con servicios y datos."],
            ["alianzas.html", "HTML", "Convenios, entidades aliadas y formas de sumarse."],
            ["como-ayudar.html", "HTML", "Voluntariado, proyectos, donaciones y auspicio."],
            ["galeria.html", "HTML", "Siete albumes con visor modal de imagenes."],
            ["contacto.html", "HTML", "Datos institucionales y formulario de demostracion."],
            ["assets/css/styles.css", "CSS", "Paleta, formas, rejillas y responsive. 996 lineas."],
            ["assets/js/main.js", "JS", "Sliders, menu, modal, galeria y formulario. 135 lineas."],
            ["assets/img/*.svg", "SVG", "Dos logos originales: cabecera y cabecera azul."],
            ["DOCUMENTACION.md", "MD", "Indice por bloques, inventario y herramientas."],
            ["DOCUMENTACION.pdf", "PDF", "Esta guia impresa con el cuadro de programas."],
        ],
        [150, 70, 261.89],
        [0],
    )
    paginas.append(p)

    p = Pagina()
    p.seccion("3. Inventario de imagenes")
    p.cuerpo("Fotografias servidas desde images.unsplash.com con ?auto=format&fit=crop&w=...&q=80.")
    p.tabla(
        ["Imagen", "Tipo", "Donde se usa"],
        [
            ["logo-uoas.svg", "SVG propio", "Cabecera (L16) e icono de pestana (L8)."],
            ["logo-uoas-blanco.svg", "SVG propio", "Hero L51 y las 12 paginas internas L51."],
            ["photo-1509062522246-3755977927d7", "Unsplash", "Hero 1 y 7; historico 1; Escuela Ninos; album 3."],
            ["photo-1503676260728-1c00da094a0b", "Unsplash", "Hero 2; mision; historico 2; Nosotros; album 1."],
            ["photo-1491013516836-7db643ee125a", "Unsplash", "Hero 3; video 1; historico 3."],
            ["photo-1516627145497-ae6968895b74", "Unsplash", "Slides 2 y 6; video 2; Escuela Ninas; album 6."],
            ["photo-1544776193-352d25ca82cd", "Unsplash", "Slides 3 y 7; mision; Cuna San Francisco; album 5."],
            ["photo-1580582932707-520aed937b7b", "Unsplash", "Slide 4; foto decorativa; historico 6."],
            ["photo-1571260899304-425eee4c7efc", "Unsplash", "Fondo del hero slide 5."],
            ["photo-1503454537195-1dcabb73ffb9", "Unsplash", "Slide 4; detalle de la mision."],
            ["photo-1596464716127-f2a82984de30", "Unsplash", "Slide 5; Hogar Transitorio; album 4."],
            ["photo-1607453998774-d533f65dac99", "Unsplash", "Hero 6; Cuna Santa Rosa 04."],
            ["photo-1587654780291-39c9404d746b", "Unsplash", "Nido Aurora y album 2."],
            ["photo-1576091160399-112ba8d25d1d", "Unsplash", "Centro Integral Aurora y album 7."],
            ["photo-1559027615-cd4628902d4a", "Unsplash", "Foto de voluntariado en como-ayudar.html."],
        ],
        [150, 70, 261.89],
        [0],
    )
    paginas.append(p)

    p = Pagina()
    p.seccion("4. Cuadro de programas y herramientas utilizadas")
    p.tabla(
        ["Programa", "Para que se uso", "Alternativa"],
        [
            ["OpenCode + Chromium", "Inspeccionar DOM, estilos y tamanos originales.", "DevTools (F12)"],
            ["webfetch", "Descargar el HTML y CSS originales y las 12 paginas internas.", "curl / navegador"],
            ["Visual Studio Code", "Editar HTML, CSS y JavaScript.", "Notepad++, Sublime"],
            ["HTML5", "Estructura del contenido.", "-"],
            ["CSS3", "Colores, formas y diseno responsive.", "-"],
            ["JavaScript DOM", "Sliders, menu movil y modal.", "-"],
            ["SVG (XML)", "Logos e iconos originales.", "Inkscape"],
            ["Unsplash", "Fotografias libres de derechos.", "Pexels, Pixabay"],
            ["Python http.server", "Servir la carpeta por HTTP (opcional).", "Live Server"],
        ],
        [150, 231.89, 100],
        [0],
    )
    p.seccion("5. Flujo de trabajo")
    p.lista("Analizar la web original en el navegador y extraer sus estilos reales.", 1)
    p.lista("Sustituir fotos por imagenes libres y redibujar los logos en SVG.", 2)
    p.lista("Escribir HTML, CSS y JS con un comentario por linea.", 3)
    p.lista("Verificar sliders, menu, modal y vista responsive.", 4)
    p.lista("Extraer las 12 URLs internas y crear una pagina local para cada una.", 5)
    p.lista("Conectar menu y pie con rutas reales y anadir estado activo.", 6)
    p.lista("Comprobar las 13 paginas: sin errores de consola y con enlaces internos.", 7)
    paginas.append(p)

    p = Pagina()
    p.seccion("6. Guia rapida de modificacion")
    p.tabla(
        ["Quieres cambiar", "Ve a"],
        [
            ["Los colores", "styles.css L1-L11"],
            ["El texto de la mision", "index.html L130"],
            ["Las fotos del hero", "index.html L49, L54, L63, L72, L81, L90, L99"],
            ["La velocidad de los sliders", "index.html L46 (5000) y L150 (4000)"],
            ["El listado de sedes", "index.html L28-L34 y L170-L176"],
            ["El pie de pagina", "index.html L181-L211 / styles.css L472-L525"],
            ["El diseno en movil", "styles.css L552-L627"],
            ["El logo", "Editar los dos SVG de assets/img/"],
            ["Los textos internos", "nosotros.html L54-L162 / sede-*.html L49-L119"],
            ["Los convenios", "alianzas.html L68-L123"],
            ["Las formas de ayuda", "como-ayudar.html L64-L119"],
            ["Los albumes", "galeria.html L60-L110"],
            ["El formulario", "contacto.html L62-L74 / main.js L119-L135"],
            ["Paginas internas", "styles.css L628-L996"],
        ],
        [200, 281.89],
        [1],
    )
    p.seccion("7. Aviso")
    p.cuerpo(
        "Este clon se realizo con fines de estudio y practica. No reproduce los videos "
        "ni los archivos multimedia originales de la institucion. Para publicarlo, "
        "sustituye los contenidos por propios o solicita autorizacion."
    )
    paginas.append(p)
    return paginas


def construir_pdf(paginas):
    objetos = []
    def add(s):
        objetos.append(s)
        return len(objetos)

    add("<< /Type /Catalog /Pages 2 0 R >>")
    add("<< /Type /Pages /Kids [] /Count 0 >>")
    add("<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica /Encoding /WinAnsiEncoding >>")
    add("<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica-Bold /Encoding /WinAnsiEncoding >>")
    add("<< /Type /Font /Subtype /Type1 /BaseFont /Courier /Encoding /WinAnsiEncoding >>")

    numeros_pagina = []
    for pagina in paginas:
        contenido = NL.join(pagina.comandos) + NL
        ncontenido = add(f"<< /Length {len(contenido.encode('latin-1'))} >>{NL}stream{NL}{contenido}endstream")
        npagina = add(
            f"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 595.2756 841.8898] "
            f"/Resources << /Font << /F1 3 0 R /F2 4 0 R /F3 5 0 R >> >> "
            f"/Contents {ncontenido} 0 R >>"
        )
        numeros_pagina.append(npagina)
    objetos[1] = (
        "<< /Type /Pages /Kids ["
        + " ".join(f"{n} 0 R" for n in numeros_pagina)
        + f"] /Count {len(numeros_pagina)} >>"
    )

    pdf = "%PDF-1.4" + NL
    off = [0]
    for i, obj in enumerate(objetos, 1):
        off.append(len(pdf.encode("latin-1")))
        pdf += f"{i} 0 obj{NL}{obj}{NL}endobj{NL}"
    xref = len(pdf.encode("latin-1"))
    pdf += f"xref{NL}0 {len(objetos) + 1}{NL}0000000000 65535 f {NL}"
    for o in off[1:]:
        pdf += f"{o:010d} 00000 n {NL}"
    pdf += f"trailer{NL}<< /Size {len(objetos) + 1} /Root 1 0 R >>{NL}startxref{NL}{xref}{NL}%%EOF"
    return pdf.encode("latin-1")


if __name__ == "__main__":
    datos = construir_pdf(construir_paginas())
    SALIDA.write_bytes(datos)
    print(f"Generado {SALIDA} ({len(datos)} bytes, 4 paginas)")
