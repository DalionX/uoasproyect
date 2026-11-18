// L1: me aseguro de que el script se ejecute solo cuando el HTML ya esté listo
document.addEventListener('DOMContentLoaded', function () { // L2: escucho el evento DOMContentLoaded

  // L3: CABECERA: añade sombra cuando el usuario baja la página
  const header = document.getElementById('site-header'); // L4: guardo referencia a la cabecera
  window.addEventListener('scroll', function () { // L5: escucho el desplazamiento de la ventana
    header.classList.toggle('is-scrolled', window.scrollY > 10); // L6: activo la clase de sombra después de 10px
  }); // L7: ciero el listener de scroll

  // L8: MENÚ MÓVIL: abre y cierra el panel lateral
  const menuToggle = document.getElementById('menu-toggle'); // L9: botón de hamburguesa
  const mainNav = document.getElementById('main-nav'); // L10: panel de navegación
  menuToggle.addEventListener('click', function () { // L11: al pulsar la hamburguesa
    const isOpen = mainNav.classList.toggle('is-open'); // L12: alterno la clase que muestra el panel
    menuToggle.classList.toggle('is-open', isOpen); // L13: la hamburguesa se transforma en X
    menuToggle.setAttribute('aria-expanded', String(isOpen)); // L14: actualizo el atributo de accesibilidad
  }); // L15: cierra el listener

  // L16: SUBMENÚ DE SEDES: se abre al pulsar en móvil
  const submenuItem = document.querySelector('.has-submenu'); // L17: ítem que contiene el desplegable
  const submenuToggle = document.querySelector('.submenu-toggle'); // L18: botón "Sedes"
  submenuToggle.addEventListener('click', function (event) { // L19: al pulsar el botón
    event.preventDefault(); // L20: evito que el botón haga otras acciones por defecto
    const isOpen = submenuItem.classList.toggle('is-open'); // L21: alterno la clase de apertura
    submenuToggle.setAttribute('aria-expanded', String(isOpen)); // L22: actualizo accesibilidad
  }); // L23: cierra el listener

  // L24: cierro el menú móvil al pulsar cualquier enlace interno
  mainNav.querySelectorAll('a').forEach(function (link) { // L25: recorro todos los enlaces del menú
    link.addEventListener('click', function () { // L26: al hacer clic en uno
      mainNav.classList.remove('is-open'); // L27: oculto el panel
      menuToggle.classList.remove('is-open'); // L28: devuelvo la hamburguesa a su forma original
      menuToggle.setAttribute('aria-expanded', 'false'); // L29: actualizo accesibilidad
      submenuItem.classList.remove('is-open'); // L30: cierro también el desplegable
    }); // L31: cierra el listener
  }); // L32: cierra el recorrido

  // L33: SLIDERS: función reutilizable para el hero (7 fotos) y el historial (6 fotos)
  function initSlider(root) { // L34: declaro la función que recibe el contenedor del slider
    const slides = Array.from(root.querySelectorAll('.slides > .slide')); // L35: convierto los slides en array
    if (slides.length === 0) { return; } // L36: si no hay slides, salgo de la función
    let current = slides.findIndex(function (slide) { return slide.classList.contains('is-active'); }); // L37: busco el slide activo inicial
    if (current < 0) { current = 0; slides[0].classList.add('is-active'); } // L38: si no hay ninguno, activo el primero
    const dotsBox = root.querySelector('.slider-dots'); // L39: contenedor de puntos del hero
    const counter = root.querySelector('.slider-counter b'); // L40: número del contador del slider pequeño
    const total = slides.length; // L41: guardo el total de slides

    if (dotsBox) { // L42: solo el hero tiene puntos
      slides.forEach(function (slide, index) { // L43: creo un punto por slide
        const li = document.createElement('li'); // L44: elemento de lista
        const btn = document.createElement('button'); // L45: botón del punto
        btn.type = 'button'; // L46: evito que sea de tipo submit
        btn.setAttribute('aria-label', 'Ir a la diapositiva ' + (index + 1)); // L47: etiqueta para lectores de pantalla
        btn.addEventListener('click', function () { goTo(index); }); // L48: al pulsar, voy a esa diapositiva
        li.appendChild(btn); // L49: meto el botón dentro del ítem
        dotsBox.appendChild(li); // L50: meto el ítem en la lista
      }); // L51: cierra la creación de puntos
    } // L52: cierra el bloque de puntos

    function paint() { // L53: función interna que actualiza puntos y contador
      if (dotsBox) { // L54: si existen puntos
        Array.from(dotsBox.children).forEach(function (li, index) { // L55: recorro los puntos
          li.classList.toggle('is-active', index === current); // L56: marco solo el punto actual
        }); // L57: cierra el recorrido
      } // L58: cierra puntos
      if (counter) { // L59: si existe el contador
        counter.textContent = String(current + 1).padStart(2, '0'); // L60: muestro 01, 02... con dos dígitos
      } // L61: cierra contador
    } // L62: cierra paint

    function goTo(index) { // L63: cambia a la diapositiva indicada
      slides[current].classList.remove('is-active'); // L64: quito el estado activo a la actual
      current = (index + total) % total; // L65: ajusto el índice para que sea circular
      slides[current].classList.add('is-active'); // L66: activo la nueva diapositiva
      paint(); // L67: actualizo puntos y contador
    } // L68: cierra goTo

    const nextBtn = root.querySelector('.nav-next'); // L69: flecha derecha del slider pequeño
    const prevBtn = root.querySelector('.nav-prev'); // L70: flecha izquierda del slider pequeño
    if (nextBtn) { nextBtn.addEventListener('click', function () { goTo(current + 1); }); } // L71: avanzar
    if (prevBtn) { prevBtn.addEventListener('click', function () { goTo(current - 1); }); } // L72: retroceder

    const interval = Number(root.dataset.interval || 5000); // L73: leo el intervalo del atributo data-interval
    window.setInterval(function () { goTo(current + 1); }, interval); // L74: reproducción automática circular

    paint(); // L75: pinto el estado inicial al cargar
  } // L76: cierra initSlider

  document.querySelectorAll('[data-slider]').forEach(initSlider); // L77: inicializo los dos sliders de la página

  // L78: MODAL: muestra la imagen de portada de cada video
  const modal = document.getElementById('modal'); // L79: referencia al modal
  const modalImage = document.getElementById('modal-image'); // L80: imagen dentro del modal
  const modalClose = document.getElementById('modal-close'); // L81: botón de cierre

  function backgroundUrl(el) { // L82: extrae la URL de la imagen de fondo de un elemento
    const bg = window.getComputedStyle(el).backgroundImage; // L83: leo la propiedad calculada
    const match = bg.match(/url\(["']?(.*?)["']?\)/); // L84: busco la parte url(...)
    return match ? match[1] : ''; // L85: devuelvo la URL o una cadena vacía
  } // L86: cierra backgroundUrl

  document.querySelectorAll('.play-button').forEach(function (button) { // L87: recorro los botones de play
    button.addEventListener('click', function () { // L88: al pulsar uno
      const card = button.closest('.video-card, .mission-main'); // L89: busco su tarjeta contenedora
      const url = card ? backgroundUrl(card) : ''; // L90: obtengo la foto de portada
      if (url && modal && modalImage) { modalImage.src = url; modal.hidden = false; } // L91: muestro el modal con esa foto
    }); // L92: cierra el listener
  }); // L93: cierra el recorrido

  modalClose?.addEventListener('click', function () { modal.hidden = true; }); // L94: cierro con el botón ×
  modal?.addEventListener('click', function (event) { // L95: cierro al pulsar fuera de la imagen
    if (event.target === modal) { modal.hidden = true; } // L96: solo si el clic fue en el fondo oscuro
  }); // L97: cierra el listener
  document.addEventListener('keydown', function (event) { // L98: cierro también con la tecla Escape
    if (event.key === 'Escape' && modal) { modal.hidden = true; } // L99: Escape oculta el modal
  }); // L100: cierra el listener

}); // L101: cierra DOMContentLoaded

// L102: resalto en el menú la página indicada en body[data-page]
const paginaActual = document.body.dataset.page; // L103: leo el identificador de la página
if (paginaActual) { // L104: solo si la página lo declara
  document.querySelectorAll('[data-page-link]').forEach(function (enlace) { // L105: recorro los enlaces marcados
    if (enlace.dataset.pageLink === paginaActual) { enlace.classList.add('is-active'); } // L106: resalto el coincidente
  }); // L107: cierra el recorrido
} // L108: cierra la condición

// L109: la galería abre la foto pulsada en el mismo modal de la portada
document.querySelectorAll('.gallery-card').forEach(function (tarjeta) { // L110: recorro los álbumes
  tarjeta.addEventListener('click', function () { // L111: al pulsar uno
    const imagen = tarjeta.querySelector('img'); // L112: busco su imagen
    const visor = document.getElementById('modal'); const foto = document.getElementById('modal-image'); if (imagen && visor && foto) { // L113: compruebo que existan los elementos
      foto.src = imagen.src.replace(/w=\d+/, 'w=1400'); // L114: pido una versión más grande
      visor.hidden = false; // L115: muestro el modal
    } // L116: cierra la condición
  }); // L117: cierra el listener
}); // L118: cierra el recorrido

// L119: el formulario de contacto valida y confirma sin enviar a ningún servidor
const formulario = document.getElementById('contact-form'); // L120: referencia al formulario
if (formulario) { // L121: solo en la página de contacto
  formulario.addEventListener('submit', function (evento) { // L122: intercepto el envío
    evento.preventDefault(); // L123: evito que se recargue la página
    if (!formulario.checkValidity()) { // L124: si faltan campos obligatorios
      formulario.reportValidity(); // L125: dejo que el navegador avise
      return; // L126: salgo sin borrar nada
    } // L127: cierra la validación
    const aviso = document.getElementById('form-message'); // L128: busco el mensaje de confirmación
    if (aviso) { // L129: si existe
      aviso.textContent = 'Gracias. Hemos recibido tu mensaje (demostración local).'; // L130: escribo el aviso
      aviso.classList.add('is-visible'); // L131: lo hago visible
    } // L132: cierra la condición
    formulario.reset(); // L133: limpio los campos
  }); // L134: cierra el listener
} // L135: cierra la condición
