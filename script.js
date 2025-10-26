document.addEventListener('DOMContentLoaded', () => {
    // --- ANIMACIÓN DE APARICIÓN AL SCROLL (SECCIONES) ---
    const sections = document.querySelectorAll('.section-container, .hero-section');

    const observer = new IntersectionObserver(entries => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('is-visible');
                // Desconectar observador una vez visible para que no se repita
                // observer.unobserve(entry.target);
            } else {
                // Opcional: para que la animación se repita al salir de la vista
                // entry.target.classList.remove('is-visible');
            }
        });
    }, {
        threshold: 0.2 // El 20% de la sección debe ser visible para activar la animación
    });

    sections.forEach(section => {
        observer.observe(section);
    });


    // --- ANIMACIÓN DE BARRAS DE PROGRESO DE IDIOMAS ---
    const progressBarObserver = new IntersectionObserver(entries => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const progressBars = entry.target.querySelectorAll('.progress-bar-fill');
                progressBars.forEach(bar => {
                    const width = bar.style.width; // Obtiene el ancho definido en el CSS inline
                    bar.style.width = '0%'; // Reinicia a 0
                    setTimeout(() => {
                        bar.style.width = width; // Aplica el ancho final
                        bar.classList.add('animated'); // Añade la clase para mostrar el nivel
                    }, 300); // Pequeño retraso para que la transición sea visible
                });
                progressBarObserver.unobserve(entry.target); // Detener la observación una vez animado
            }
        });
    }, {
        threshold: 0.5 // Cuando el 50% del contenedor de habilidades es visible
    });

    const skillsSection = document.getElementById('skills');
    if (skillsSection) {
        progressBarObserver.observe(skillsSection);
    }


    // --- RESALTAR ENLACE DE NAVEGACIÓN AL HACER SCROLL ---
    const navLinks = document.querySelectorAll('.nav-links a');
    
    const highlightNav = () => {
        let current = '';
        sections.forEach(section => {
            const sectionTop = section.offsetTop;
            const sectionHeight = section.clientHeight;
            if (scrollY >= sectionTop - sectionHeight / 3) { // Ajuste para que se active un poco antes
                current = section.getAttribute('id');
            }
        });

        navLinks.forEach(link => {
            link.classList.remove('active');
            if (link.getAttribute('href').includes(current)) {
                link.classList.add('active');
            }
        });
    };

    window.addEventListener('scroll', highlightNav);
    highlightNav(); // Ejecutar al cargar para establecer la sección activa
});