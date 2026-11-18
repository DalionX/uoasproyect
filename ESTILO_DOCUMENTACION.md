# Modelo visual para documentaciones (extraído del PDF de referencia)

A partir de ahora, **toda documentación entregada en PDF debe seguir este modelo**. Fue extraído programáticamente de `C:\Users\g0j\Downloads\DOCUMENTACION.pdf` (ReportLab, 4 páginas, A4) y aplicado a `DOCUMENTACION.pdf` de este proyecto.

## 1. Página

| Parámetro | Valor del PDF de referencia | Valor usado en el generador |
|---|---|---|
| Formato | A4 | A4 |
| `MediaBox` | `[0 0 595.2756 841.8898]` | `[0 0 595.2756 841.8898]` |
| Margen izquierdo | `62.69291 pt` | `56.69291 pt` (da un poco más de ancho útil a las tablas) |
| Ancho de contenido | `481.8898 pt` | `481.8898 pt` |
| Alto útil inicial | `~790 pt` | `790 pt` |

## 2. Tipografía

| Rol | Fuente PDF | Tamaño | Interlineado | Color |
|---|---|---:|---:|---|
| Título principal | `/F2` Helvetica-Bold | 20 pt | 30 pt | Azul marino |
| Encabezado de sección | `/F2` Helvetica-Bold | 14 pt | 24 pt | Azul |
| Texto de cuerpo y viñetas | `/F1` Helvetica | 9.5 pt | 13 pt | Negro |
| Cabecera de tabla | `/F2` Helvetica-Bold | 8 pt | — | Blanco |
|Celda de tabla | `/F1` Helvetica | 8 pt | 10 pt | Negro |
| Celda de código / ruta | `/F3` Courier | 8 pt | 10 pt | Violeta |

Recursos del PDF:

```pdf
/F1 3 0 R  → Helvetica
/F2 4 0 R  → Helvetica-Bold
/F3 5 0 R  → Courier
```

Codificación: `/WinAnsiEncoding`. El texto se escribe en ASCII (sin tildes) para que el PDF propio no dependa de fuentes incrustadas.

## 3. Paleta

| Nombre | Valor PDF (0–1) | Hex | Uso |
|---|---|---|---|
| Azul marino | `.070588 .192157 .352941` | `#12315A` | Título principal |
| Azul | `.113725 .305882 .537255` | `#1D4E89` | Secciones y relleno de cabeceras de tabla |
| Negro | `0 0 0` | `#000000` | Cuerpo y celdas normales |
| Violeta | `.541176 .168627 .886275` | `#8A2BE2` | Código, rutas y etiquetas `<...>` |
| Blanco | `1 1 1` | `#FFFFFF` | Texto sobre cabecera azul y filas pares |
| Gris claro | `.956863 .968627 .984314` | `#F4F7FB` | Filas impares (efecto cebra) |
| Borde gris | `.721569 .768627 .839216` | `#B8C4D6` | Líneas de tabla, 0.4 pt |

## 4. Tablas

- Cabecera: rectángulo relleno de azul `#1D4E89`, texto blanco en Helvetica-Bold 8 pt.
- Filas: altura mínima 16 pt; crece 10 pt por cada línea de texto envuelto.
- Fondo alterno: blanco / `#F4F7FB`.
- Borde exterior: `re S` con color `#B8C4D6` y grosor `.4 w`.
- Líneas horizontales interiores en cada cambio de fila.
- Líneas verticales sólo en los límites entre columnas, desde el borde inferior hasta el superior de la tabla.
- Las columnas de código usan Courier violeta 8 pt.

## 5. Listas y texto

- Viñetas: carácter `\225` (• en WinAnsi) en Helvetica 9.5 pt, separado 13 pt del texto.
- Listas numeradas: `1.`, `2.`, `3.`… en la misma posición.
- Párrafos: se envuelven a ~95 caracteres; sangría de 13 pt respecto al margen.
- Cada sección lleva 12 pt de espacio antes y 24 pt después.

## 6. Regla de aplicación futura

Para cada documentación nueva:

1. Usa `generar_documento.py` como plantilla: contiene la paleta, fuentes, márgenes y funciones `titulo`, `seccion`, `cuerpo`, `lista` y `tabla`.
2. Sustituye sólo los textos y los datos de las filas; **no cambies colores, fuentes ni grosores**.
3. Mantén el cuadro de programas y herramientas como sección numerada.
4. Genera el PDF con `python generar_documento.py` (o `py -3 generar_documento.py` en Windows).
5. Verifica: 4 páginas A4, fuentes Helvetica/Helvetica-Bold/Courier, colores anteriores y `xref` válido.

> Nota: en este entorno la consola está bloqueada por directiva de grupo, por lo que el PDF entregado se generó con el mismo código ejecutado en el navegador y se guardó directamente. El script queda como plantilla reproducible para cuando la consola esté disponible.
