document.addEventListener('DOMContentLoaded', () => {
    const themeSwitcher = document.getElementById('theme-switcher');
    const langBtn = document.getElementById('lang-btn');
    const langDropdown = document.getElementById('lang-dropdown');
    const langOptions = document.querySelectorAll('.lang-dropdown a');

    // --- LÓGICA DEL MODO OSCURO ---
    const currentTheme = localStorage.getItem('theme');
    if (currentTheme) {
        document.body.setAttribute('data-theme', currentTheme);
        if (currentTheme === 'dark') {
            themeSwitcher.innerHTML = '<i class="fas fa-sun"></i>';
        }
    }

    themeSwitcher.addEventListener('click', () => {
        let theme = document.body.getAttribute('data-theme');
        if (theme === 'dark') {
            document.body.removeAttribute('data-theme');
            localStorage.removeItem('theme');
            themeSwitcher.innerHTML = '<i class="fas fa-moon"></i>';
        } else {
            document.body.setAttribute('data-theme', 'dark');
            localStorage.setItem('theme', 'dark');
            themeSwitcher.innerHTML = '<i class="fas fa-sun"></i>';
        }
    });

    // --- LÓGICA DEL CAMBIO DE IDIOMA ---
    const elementsToTranslate = document.querySelectorAll('[data-lang-es], [data-lang-en]');
    
    const translatePage = (language) => {
        elementsToTranslate.forEach(el => {
            el.innerText = el.getAttribute(`data-lang-${language}`);
        });
        langBtn.firstChild.textContent = language.toUpperCase() + ' ';
        localStorage.setItem('language', language);
        langDropdown.classList.remove('show');
    };

    const currentLang = localStorage.getItem('language') || 'es';
    translatePage(currentLang);

    langBtn.addEventListener('click', () => {
        langDropdown.classList.toggle('show');
    });

    langOptions.forEach(option => {
        option.addEventListener('click', (e) => {
            e.preventDefault();
            const selectedLang = e.target.getAttribute('data-lang');
            translatePage(selectedLang);
        });
    });

    // Cierra el dropdown si se hace clic fuera
    window.addEventListener('click', (e) => {
        if (!langBtn.contains(e.target) && !langDropdown.contains(e.target)) {
            langDropdown.classList.remove('show');
        }
    });


    // --- LÓGICA DE ANIMACIONES (YA EXISTENTE) ---
    const sections = document.querySelectorAll('.section-container, .hero-section');
    const observer = new IntersectionObserver(entries => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('is-visible');
            }
        });
    }, { threshold: 0.1 });

    sections.forEach(section => observer.observe(section));

    const progressBarObserver = new IntersectionObserver(entries => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const progressBars = entry.target.querySelectorAll('.progress-bar-fill');
                progressBars.forEach(bar => {
                    const width = bar.style.width;
                    bar.style.width = '0%';
                    setTimeout(() => {
                        bar.style.width = width;
                        bar.classList.add('animated');
                    }, 300);
                });
                progressBarObserver.unobserve(entry.target);
            }
        });
    }, { threshold: 0.5 });

    const skillsSection = document.getElementById('skills');
    if (skillsSection) {
        progressBarObserver.observe(skillsSection);
    }
});