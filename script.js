document.addEventListener('DOMContentLoaded', () => {

    // =============================================
    // 1. TEMA (claro/oscuro)
    // =============================================
    const themeSwitcher = document.getElementById('theme-switcher');
    const currentTheme = localStorage.getItem('theme');
    if (currentTheme) {
        document.body.setAttribute('data-theme', currentTheme);
        if (currentTheme === 'dark') themeSwitcher.innerHTML = '<i class="fas fa-sun"></i>';
    }

    themeSwitcher.addEventListener('click', () => {
        const theme = document.body.getAttribute('data-theme');
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

    // =============================================
    // 2. IDIOMA
    // =============================================
    const langBtn = document.getElementById('lang-btn');
    const langDropdown = document.getElementById('lang-dropdown');
    const langOptions = document.querySelectorAll('.lang-dropdown a');
    const elementsToTranslate = document.querySelectorAll('[data-lang-es], [data-lang-en]');

    const translatePage = (language) => {
        elementsToTranslate.forEach(el => {
            const text = el.getAttribute(`data-lang-${language}`);
            if (text) el.innerText = text;
        });
        langBtn.firstChild.textContent = language.toUpperCase() + ' ';
        localStorage.setItem('language', language);
        langDropdown.classList.remove('show');
    };

    const currentLang = localStorage.getItem('language') || 'es';
    translatePage(currentLang);

    langBtn.addEventListener('click', () => langDropdown.classList.toggle('show'));

    langOptions.forEach(option => {
        option.addEventListener('click', (e) => {
            e.preventDefault();
            translatePage(e.target.getAttribute('data-lang'));
        });
    });

    window.addEventListener('click', (e) => {
        if (!langBtn.contains(e.target) && !langDropdown.contains(e.target)) {
            langDropdown.classList.remove('show');
        }
    });

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

    function typeLoop() {
        if (!typingEl) return;
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
    if (canvas) {
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
            const res = await fetch(`https://api.github.com/users/${GITHUB_USER}/repos?sort=updated&per_page=9&type=public`);
            if (!res.ok) throw new Error('API error');
            const repos = await res.json();

            // Filtrar el repo de la propia web
            const filtered = repos.filter(r => r.name !== `${GITHUB_USER}.github.io`).slice(0, 6);

            if (filtered.length === 0) {
                projectsGrid.innerHTML = `<p style="grid-column:1/-1;text-align:center;color:var(--text-color);">No se encontraron repositorios públicos.</p>`;
                return;
            }

            projectsGrid.innerHTML = filtered.map(repo => {
                const description = repo.description
                    ? repo.description
                    : (lang === 'es' ? 'Sin descripción' : 'No description');
                const language = repo.language || '';
                const langBadge = language
                    ? `<span class="project-lang" style="border-left: 3px solid ${getLangColor(language)}">${language}</span>`
                    : '';
                const stars = repo.stargazers_count > 0
                    ? `<span class="project-stars">⭐ ${repo.stargazers_count}</span>`
                    : '';
                const linkText = lang === 'es' ? 'Ver repositorio →' : 'View repository →';

                return `
                <div class="project-card">
                    <div class="project-card-header">
                        <i class="fab fa-github"></i>
                        <h3>${repo.name}</h3>
                    </div>
                    <p>${description}</p>
                    <div class="project-card-meta">
                        ${langBadge}
                        ${stars}
                    </div>
                    <a href="${repo.html_url}" target="_blank" rel="noopener noreferrer" class="project-card-link">
                        ${linkText}
                    </a>
                </div>`;
            }).join('');

        } catch (err) {
            projectsGrid.innerHTML = `
                <div class="projects-loading">
                    <i class="fas fa-exclamation-triangle fa-2x" style="color:#dc3545"></i>
                    <p>${lang === 'es' ? 'No se pudieron cargar los proyectos. Visita el perfil de GitHub directamente.' : 'Could not load projects. Visit the GitHub profile directly.'}</p>
                </div>`;
        }
    }

    loadGitHubProjects();

    // =============================================
    // 9. DESCARGAR CV (PDF DINÁMICO)
    // =============================================
    const downloadBtn = document.getElementById('download-cv');
    if (downloadBtn) {
        downloadBtn.addEventListener('click', () => {
            const element = document.getElementById('cv-template');
            const lang = localStorage.getItem('language') || 'es';
            
            // Forzamos el renderizado para que html2canvas lo capture correctamente
            element.style.display = 'block';

            const opt = {
                margin:       [10, 10, 10, 10],
                filename:     `CV_Alberto_Ortiz_Sanchez_${lang.toUpperCase()}.pdf`,
                image:        { type: 'jpeg', quality: 0.98 },
                html2canvas:  { 
                    scale: 2, 
                    useCORS: true, 
                    logging: false,
                    letterRendering: true,
                    windowWidth: 800
                },
                jsPDF:        { unit: 'mm', format: 'a4', orientation: 'portrait' }
            };

            // Ejecutar la conversión
            html2pdf().set(opt).from(element).save().then(() => {
                element.style.display = 'none';
            }).catch(err => {
                console.error("Error generando PDF:", err);
                element.style.display = 'none';
            });
        });
    }


});