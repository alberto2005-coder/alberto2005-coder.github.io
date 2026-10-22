document.addEventListener('DOMContentLoaded', () => {

    // =============================================
    // 1. TEMA (claro/oscuro)
    // =============================================
    const themeSwitcher = document.getElementById('theme-switcher');
    const systemPrefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
    const storedTheme = localStorage.getItem('theme');

    // Determinar el tema inicial
    let currentTheme = 'light';
    if (storedTheme) {
        currentTheme = storedTheme;
    } else if (systemPrefersDark) {
        currentTheme = 'dark';
    }

    // Función para aplicar el tema
    const langCode = () => (localStorage.getItem('language') || 'es');

    const applyTheme = (theme) => {
        const en = langCode() === 'en';
        if (theme === 'dark') {
            document.body.setAttribute('data-theme', 'dark');
            themeSwitcher.innerHTML = '<i class="fas fa-sun" aria-hidden="true"></i>';
            themeSwitcher.setAttribute('aria-label', en ? 'Switch to light theme' : 'Cambiar a tema claro');
        } else {
            document.body.removeAttribute('data-theme');
            themeSwitcher.innerHTML = '<i class="fas fa-moon" aria-hidden="true"></i>';
            themeSwitcher.setAttribute('aria-label', en ? 'Switch to dark theme' : 'Cambiar a tema oscuro');
        }
    };

    // Aplicar tema inicial
    applyTheme(currentTheme);

    // Manejar el botón de cambio de tema
    themeSwitcher.addEventListener('click', () => {
        const isDark = document.body.getAttribute('data-theme') === 'dark';
        const newTheme = isDark ? 'light' : 'dark';
        applyTheme(newTheme);
        localStorage.setItem('theme', newTheme);
    });

    // Escuchar cambios en la preferencia del sistema en tiempo real
    window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', e => {
        if (!localStorage.getItem('theme')) {
            applyTheme(e.matches ? 'dark' : 'light');
        }
    });

    // =============================================
    // 2. IDIOMA
    // =============================================
    const langBtn = document.getElementById('lang-btn');
    const langDropdown = document.getElementById('lang-dropdown');
    const langLabel = document.getElementById('lang-label');
    const langOptions = document.querySelectorAll('.lang-dropdown a');

    const metaByLang = {
        es: {
            title: 'Alberto Ortiz Sánchez | Técnico Superior DAM · Portfolio & CV',
            description: 'Portfolio y CV de Alberto Ortiz Sánchez, Técnico Superior en Desarrollo de Aplicaciones Multiplataforma. Experiencia en HTML, CSS, JavaScript, Python, Java y más.',
            expand: 'Abrir menú de idioma',
            openMenu: 'Abrir menú',
            closeMenu: 'Cerrar menú'
        },
        en: {
            title: 'Alberto Ortiz Sánchez | Full Stack Developer · Portfolio & CV',
            description: 'Portfolio and CV of Alberto Ortiz Sánchez, Higher Technician in Multiplatform Application Development. Experience with HTML, CSS, JavaScript, Python, Java and more.',
            expand: 'Open language menu',
            openMenu: 'Open menu',
            closeMenu: 'Close menu'
        }
    };

    const translatePage = (language) => {
        localStorage.setItem('language', language);

        const allTranslatable = document.querySelectorAll('[data-lang-es], [data-lang-en]');
        allTranslatable.forEach(el => {
            const text = el.getAttribute(`data-lang-${language}`);
            if (text) el.innerHTML = text;
        });

        // Idioma del documento + metadatos (SEO y lectores de pantalla)
        document.documentElement.lang = language;
        const meta = metaByLang[language] || metaByLang.es;
        document.title = meta.title;
        const desc = document.querySelector('meta[name="description"]');
        if (desc) desc.setAttribute('content', meta.description);

        if (langLabel) langLabel.textContent = language.toUpperCase();
        langBtn.setAttribute('aria-label', meta.expand);

        // CV en el idioma activo
        document.querySelectorAll('[data-cv-link]').forEach(link => {
            const file = language === 'en' ? link.dataset.cvEn : link.dataset.cvEs;
            if (file) {
                link.href = file;
                link.setAttribute('hreflang', language);
            }
        });

        // Textos accesibles del menú móvil y tema
        const navToggle = document.getElementById('nav-toggle');
        if (navToggle) {
            const open = navToggle.getAttribute('aria-expanded') === 'true';
            navToggle.setAttribute('aria-label', open ? meta.closeMenu : meta.openMenu);
        }
        applyTheme(document.body.getAttribute('data-theme') === 'dark' ? 'dark' : 'light');

        langDropdown.classList.remove('show');
        langBtn.setAttribute('aria-expanded', 'false');
    };

    const currentLang = localStorage.getItem('language') || 'es';
    translatePage(currentLang);

    langBtn.addEventListener('click', () => {
        const isOpen = langDropdown.classList.toggle('show');
        langBtn.setAttribute('aria-expanded', String(isOpen));
    });

    langOptions.forEach(option => {
        option.addEventListener('click', (e) => {
            e.preventDefault();
            translatePage(e.currentTarget.getAttribute('data-lang'));
        });
    });

    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape') {
            langDropdown.classList.remove('show');
            langBtn.setAttribute('aria-expanded', 'false');
            langBtn.focus();
        }
    });

    window.addEventListener('click', (e) => {
        if (!langBtn.contains(e.target) && !langDropdown.contains(e.target)) {
            langDropdown.classList.remove('show');
            langBtn.setAttribute('aria-expanded', 'false');
        }
    });

    // =============================================
    // 2b. MENÚ MÓVIL
    // =============================================
    const navToggle = document.getElementById('nav-toggle');
    const navLinks = document.getElementById('nav-links');

    const closeNav = () => {
        if (!navLinks) return;
        navLinks.classList.remove('is-open');
        navToggle.setAttribute('aria-expanded', 'false');
        navToggle.setAttribute('aria-label', metaByLang[langCode()].openMenu);
        navToggle.innerHTML = '<i class="fas fa-bars" aria-hidden="true"></i>';
    };

    if (navToggle && navLinks) {
        navToggle.addEventListener('click', () => {
            const isOpen = navLinks.classList.toggle('is-open');
            navToggle.setAttribute('aria-expanded', String(isOpen));
            navToggle.setAttribute('aria-label', metaByLang[langCode()][isOpen ? 'closeMenu' : 'openMenu']);
            navToggle.innerHTML = isOpen
                ? '<i class="fas fa-times" aria-hidden="true"></i>'
                : '<i class="fas fa-bars" aria-hidden="true"></i>';
        });

        navLinks.querySelectorAll('a').forEach(link => {
            link.addEventListener('click', closeNav);
        });

        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape' && navLinks.classList.contains('is-open')) closeNav();
        });

        window.addEventListener('resize', () => {
            if (window.innerWidth > 1250) closeNav();
        });
    }

    // =============================================
    // 3. TYPING EFFECT
    // =============================================
    const typingEl = document.getElementById('typing-text');
    const textsEs = [
        'Técnico Superior de DAM',
        'Desarrollador Web',
        'Desarrollador de Videojuegos',
        'Apasionado por la tecnología',
        'Hacker Ético certificado',
        'Siempre aprendiendo...'
    ];
    const textsEn = [
        'Higher Technician in DAM',
        'Web Developer',
        'Game Developer',
        'Tech Enthusiast',
        'Certified Ethical Hacker',
        'Always learning...'
    ];

    let typingIndex = 0;
    let charIndex = 0;
    let isDeleting = false;
    const typingSpeed = 80;
    const deletingSpeed = 40;
    const pauseTime = 2000;

    function getTexts() {
        return (localStorage.getItem('language') || 'es') === 'es' ? textsEs : textsEn;
    }

    const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

    function typeLoop() {
        if (!typingEl) return;
        if (prefersReducedMotion) {
            typingEl.textContent = getTexts()[0];
            return;
        }
        const texts = getTexts();
        const currentText = texts[typingIndex];

        if (!isDeleting) {
            typingEl.textContent = currentText.substring(0, charIndex + 1);
            charIndex++;
            if (charIndex === currentText.length) {
                isDeleting = true;
                setTimeout(typeLoop, pauseTime);
                return;
            }
        } else {
            typingEl.textContent = currentText.substring(0, charIndex - 1);
            charIndex--;
            if (charIndex === 0) {
                isDeleting = false;
                typingIndex = (typingIndex + 1) % texts.length;
            }
        }
        setTimeout(typeLoop, isDeleting ? deletingSpeed : typingSpeed);
    }

    typeLoop();

    // =============================================
    // 4. PARTÍCULAS EN HERO
    // =============================================
    const canvas = document.getElementById('particles-canvas');
    if (canvas && !prefersReducedMotion) {
        const ctx = canvas.getContext('2d');
        let particles = [];

        function resizeCanvas() {
            canvas.width = canvas.offsetWidth;
            canvas.height = canvas.offsetHeight;
        }
        resizeCanvas();
        window.addEventListener('resize', resizeCanvas);

        class Particle {
            constructor() { this.reset(); }
            reset() {
                this.x = Math.random() * canvas.width;
                this.y = Math.random() * canvas.height;
                this.size = Math.random() * 2 + 0.5;
                this.speedX = (Math.random() - 0.5) * 0.5;
                this.speedY = (Math.random() - 0.5) * 0.5;
                this.opacity = Math.random() * 0.6 + 0.2;
            }
            update() {
                this.x += this.speedX;
                this.y += this.speedY;
                if (this.x < 0 || this.x > canvas.width || this.y < 0 || this.y > canvas.height) this.reset();
            }
            draw() {
                ctx.beginPath();
                ctx.arc(this.x, this.y, this.size, 0, Math.PI * 2);
                ctx.fillStyle = `rgba(255,255,255,${this.opacity})`;
                ctx.fill();
            }
        }

        for (let i = 0; i < 80; i++) particles.push(new Particle());

        function connectParticles() {
            for (let i = 0; i < particles.length; i++) {
                for (let j = i + 1; j < particles.length; j++) {
                    const dx = particles[i].x - particles[j].x;
                    const dy = particles[i].y - particles[j].y;
                    const dist = Math.sqrt(dx * dx + dy * dy);
                    if (dist < 120) {
                        ctx.beginPath();
                        ctx.strokeStyle = `rgba(255,255,255,${0.15 * (1 - dist / 120)})`;
                        ctx.lineWidth = 0.5;
                        ctx.moveTo(particles[i].x, particles[i].y);
                        ctx.lineTo(particles[j].x, particles[j].y);
                        ctx.stroke();
                    }
                }
            }
        }

        function animateParticles() {
            ctx.clearRect(0, 0, canvas.width, canvas.height);
            particles.forEach(p => { p.update(); p.draw(); });
            connectParticles();
            requestAnimationFrame(animateParticles);
        }
        animateParticles();
    }

    // =============================================
    // 5. BARRA DE PROGRESO DE LECTURA
    // =============================================
    const readProgress = document.getElementById('read-progress');
    window.addEventListener('scroll', () => {
        if (!readProgress) return;
        const scrollTop = window.scrollY;
        const docHeight = document.documentElement.scrollHeight - window.innerHeight;
        const progress = (scrollTop / docHeight) * 100;
        readProgress.style.width = progress + '%';
    });

    // =============================================
    // 6. ANIMACIONES AL HACER SCROLL
    // =============================================
    const sections = document.querySelectorAll('.section-container, .hero-section');
    const observer = new IntersectionObserver(entries => {
        entries.forEach(entry => {
            if (entry.isIntersecting) entry.target.classList.add('is-visible');
        });
    }, { threshold: 0.1 });
    sections.forEach(section => observer.observe(section));

    // =============================================
    // 7. BARRAS DE PROGRESO DE IDIOMAS
    // =============================================
    const progressBarObserver = new IntersectionObserver(entries => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const bars = entry.target.querySelectorAll('.progress-bar-fill');
                bars.forEach(bar => {
                    const width = bar.style.width;
                    bar.style.width = '0%';
                    setTimeout(() => { bar.style.width = width; bar.classList.add('animated'); }, 300);
                });
                progressBarObserver.unobserve(entry.target);
            }
        });
    }, { threshold: 0.5 });

    const skillsSection = document.getElementById('skills');
    if (skillsSection) progressBarObserver.observe(skillsSection);

    // =============================================
    // 8. PROYECTOS DESDE GITHUB API
    // =============================================
    const projectsGrid = document.getElementById('projects-grid');
    const contributionsGrid = document.getElementById('contributions-grid');
    const GITHUB_USER = 'alberto2005-coder';
    const lang = localStorage.getItem('language') || 'es';

    const langColors = {
        JavaScript: '#f1e05a', Python: '#3572A5', Java: '#b07219',
        HTML: '#e34c26', CSS: '#563d7c', 'C++': '#f34b7d',
        TypeScript: '#2b7489', PHP: '#4F5D95', default: '#007bff'
    };

    function getLangColor(language) {
        return langColors[language] || langColors.default;
    }

    async function loadGitHubProjects() {
        try {
            // Aumentamos per_page a 50 para asegurar capturar suficientes proyectos propios y contribuciones (forks)
            const res = await fetch(`https://api.github.com/users/${GITHUB_USER}/repos?sort=created&per_page=50&type=public`);
            if (!res.ok) throw new Error('API error');
            const repos = await res.json();

            // Filtrar y separar
            // 1. Proyectos propios (no forks y omitiendo la web del portfolio)
            const ownRepos = repos.filter(r => !r.fork && r.name !== `${GITHUB_USER}.github.io`).slice(0, 6);
            // 2. Contribuciones (forks)
            const forkedRepos = repos.filter(r => r.fork && r.name !== `${GITHUB_USER}.github.io`).slice(0, 6);

            // Renderizar proyectos propios
            if (ownRepos.length === 0) {
                projectsGrid.innerHTML = `<p style="grid-column:1/-1;text-align:center;color:var(--text-color);" data-lang-es="No se encontraron repositorios públicos." data-lang-en="No public repositories found.">${lang === 'es' ? 'No se encontraron repositorios públicos.' : 'No public repositories found.'}</p>`;
            } else {
                projectsGrid.innerHTML = ownRepos.map(repo => {
                    const descEs = repo.description || 'Sin descripción';
                    const descEn = repo.description || 'No description';
                    const language = repo.language || '';
                    const langBadge = language
                        ? `<span class="project-lang" style="border-left: 3px solid ${getLangColor(language)}">${language}</span>`
                        : '';
                    const stars = repo.stargazers_count > 0
                        ? `<span class="project-stars">⭐ ${repo.stargazers_count}</span>`
                        : '';
                    const linkTextEs = 'Ver repositorio →';
                    const linkTextEn = 'View repository →';

                    return `
                    <div class="project-card">
                        <div class="project-card-header">
                            <i class="fab fa-github"></i>
                            <h3>${repo.name}</h3>
                        </div>
                        <p data-lang-es="${descEs}" data-lang-en="${descEn}">${lang === 'es' ? descEs : descEn}</p>
                        <div class="project-card-meta">
                            ${langBadge}
                            ${stars}
                        </div>
                        <a href="${repo.html_url}" target="_blank" rel="noopener noreferrer" class="project-card-link" data-lang-es="${linkTextEs}" data-lang-en="${linkTextEn}">
                            ${lang === 'es' ? linkTextEs : linkTextEn}
                        </a>
                    </div>`;
                }).join('');
            }

            // Renderizar contribuciones
            if (forkedRepos.length === 0) {
                contributionsGrid.innerHTML = `<p style="grid-column:1/-1;text-align:center;color:var(--text-color);" data-lang-es="No se encontraron contribuciones públicas." data-lang-en="No public contributions found.">${lang === 'es' ? 'No se encontraron contribuciones públicas.' : 'No public contributions found.'}</p>`;
            } else {
                contributionsGrid.innerHTML = forkedRepos.map(repo => {
                    const descEs = repo.description || 'Sin descripción';
                    const descEn = repo.description || 'No description';
                    const language = repo.language || '';
                    const langBadge = language
                        ? `<span class="project-lang" style="border-left: 3px solid ${getLangColor(language)}">${language}</span>`
                        : '';
                    const stars = repo.stargazers_count > 0
                        ? `<span class="project-stars">⭐ ${repo.stargazers_count}</span>`
                        : '';
                    const linkTextEs = 'Ver contribución →';
                    const linkTextEn = 'View contribution →';

                    return `
                    <div class="project-card">
                        <div class="project-card-header">
                            <i class="fas fa-code-branch" style="color: var(--accent-color);"></i>
                            <h3>${repo.name}</h3>
                        </div>
                        <p data-lang-es="${descEs}" data-lang-en="${descEn}">${lang === 'es' ? descEs : descEn}</p>
                        <div class="project-card-meta">
                            ${langBadge}
                            ${stars}
                        </div>
                        <a href="${repo.html_url}" target="_blank" rel="noopener noreferrer" class="project-card-link" data-lang-es="${linkTextEs}" data-lang-en="${linkTextEn}">
                            ${lang === 'es' ? linkTextEs : linkTextEn}
                        </a>
                    </div>`;
                }).join('');
            }

        } catch (err) {
            const errorMsgEs = 'No se pudieron cargar los proyectos. Visita el perfil de GitHub directamente.';
            const errorMsgEn = 'Could not load projects. Visit the GitHub profile directly.';
            const errorHtml = `
                <div class="projects-loading">
                    <i class="fas fa-exclamation-triangle fa-2x" style="color:#dc3545"></i>
                    <p data-lang-es="${errorMsgEs}" data-lang-en="${errorMsgEn}">${lang === 'es' ? errorMsgEs : errorMsgEn}</p>
                </div>`;
            projectsGrid.innerHTML = errorHtml;
            contributionsGrid.innerHTML = errorHtml;
        }
    }

    loadGitHubProjects();

    // =============================================
    // 9. COPIAR AL PORTAPAPELES
    // =============================================
    document.querySelectorAll('[data-copy]').forEach(btn => {
        btn.addEventListener('click', async () => {
            const label = btn.querySelector('span');
            if (!label) return;
            const original = label.textContent;
            const es = langCode() === 'es';

            try {
                await navigator.clipboard.writeText(btn.dataset.copy);
            } catch (err) {
                const helper = document.createElement('textarea');
                helper.value = btn.dataset.copy;
                helper.setAttribute('readonly', '');
                helper.style.position = 'absolute';
                helper.style.left = '-9999px';
                document.body.appendChild(helper);
                helper.select();
                document.execCommand('copy');
                helper.remove();
            }

            btn.classList.add('is-copied');
            label.textContent = es ? btn.dataset.copiedEs : btn.dataset.copiedEn;
            setTimeout(() => {
                btn.classList.remove('is-copied');
                label.textContent = original;
            }, 2000);
        });
    });

});
