# Alberto Ortiz Sánchez — Portfolio Oficial & Showcase de Ingeniería

[![Sitio Web Oficial](https://img.shields.io/badge/Sitio_Web-albertoortiz.is--a.dev-0b5ed7?style=for-the-badge&logo=googlechrome&logoColor=white)](https://albertoortiz.is-a.dev/)
[![GitHub](https://img.shields.io/badge/GitHub-alberto2005--coder-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/alberto2005-coder)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Alberto_Ortiz-0077b5?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/alberto-ortiz-sanchez)
[![Itch.io](https://img.shields.io/badge/Itch.io-alberto--coder2005-fa5c5c?style=for-the-badge&logo=itch.io&logoColor=white)](https://alberto-coder2005.itch.io/)
[![Google Play](https://img.shields.io/badge/Google_Play-GR_Games-414141?style=for-the-badge&logo=googleplay&logoColor=white)](https://play.google.com/store/apps/details?id=com.grgames.thememorygames)

---

## Español

### Índice

1. [Proyectos Interactivos y Videojuegos (Detalle Técnico)](#proyectos-interactivos-y-videojuegos-detalle-técnico)
2. [Proyectos Destacados de Software & IA](#proyectos-destacados-de-software-ia)
3. [Arquitectura Web & Optimizaciones del Portfolio](#arquitectura-web-optimizaciones-del-portfolio)
4. [Mantenimiento del sitio](#mantenimiento-del-sitio)

Repositorio del sitio web personal y portfolio profesional de **Alberto Ortiz Sánchez** ([@alberto2005-coder](https://github.com/alberto2005-coder)), Desarrollador Full Stack y Técnico Superior DAM especializado en Inteligencia Artificial y Machine Learning en Granada, España.

Desplegado en producción en: **[https://albertoortiz.is-a.dev/](https://albertoortiz.is-a.dev/)**

---

### Proyectos Interactivos y Videojuegos (Detalle Técnico)

#### 1. Tetris C++
* **Tecnologías**: C++ moderno (C++17/20), lógica algorítmica matricial, renderizado eficiente en consola/búfer gráfico.
* **Enlace**: [Jugar en Itch.io](https://alberto-coder2005.itch.io/tetris-game-c)
* **Retos superados en el código**:
  * **Sistema de rotación SRS (*Super Rotation System*)**: Implementación matemática de matrices de colisión y tablas de *wall kick* para permitir giros en espacios ajustados sin atravesar los bordes ni piezas fijas.
  * **Gestión de memoria y ciclos de render**: Control estricto de memoria sin dependencias externas pesadas, desacoplando el bucle de actualización lógica (*tick rate* constante de gravedad acelerada por nivel) del bucle de pintado.
  * **Eliminación y colapso de líneas simultáneas**: Algoritmo recursivo de desplazamiento de filas con verificación bitwise para detectar Tetris cuádruples sin fugas de memoria.

#### 2. Neon Dash
* **Tecnologías**: Flutter, Dart, Canvas 2D interactivo, audio posicional, animaciones reactivas a 60/120 FPS.
* **Enlace**: [Jugar en Itch.io](https://alberto-coder2005.itch.io/neon-dash)
* **Retos superados en el código**:
  * **Sincronización milimétrica ritmo-física**: Creación de un motor de colisiones elástico con cálculo de bounding boxes continuas (*Continuous Collision Detection*) para prevenir el efecto *tunneling* a altas velocidades de desplazamiento horizontal.
  * **Optimización de renderizado en Flutter Web**: Sustitución de árboles complejos de Widgets por capas personalizadas en `CustomPainter`, reduciendo el tiempo de repintado a menos de 8 ms por cuadro para evitar caídas de frames en navegadores móviles.
  * **Shader de brillo neón adaptativo**: Simulación visual de iluminación Bloom mediante gradientes radiales optimizados sin sobrecargar la GPU del cliente.

#### 3. The Memory Game (Google Play Store)
* **Tecnologías**: Unity, C#, Android SDK, Google Play Games Services, serialización JSON cifrada.
* **Enlace**: [Descargar en Google Play](https://play.google.com/store/apps/details?id=com.grgames.thememorygames)
* **Retos superados en el código**:
  * **Curva de dificultad procedural y memorización progresiva**: Algoritmo de secuencias pseudoaleatorias controladas para garantizar que los patrones generados sean estimulantes pero humanamente alcanzables bajo presión de tiempo.
  * **Persistencia local segura anti-trampas**: Cifrado simétrico AES en almacenamiento local de mejores puntuaciones para impedir manipulación antes de la sincronización con la nube.
  * **Gestión del ciclo de vida móvil**: Gestión de estados `OnApplicationPause` y retención de memoria para evitar pérdidas de progreso en llamadas entrantes o cambios de app.

#### 4. Echo Protocol (FPS 3D en Navegador & Escritorio)
* **Tecnologías**: React 19, TypeScript, Three.js, WebGL 2.0, Web Audio API procedural, Tauri (Windows Desktop).
* **Enlace**: [Repositorio en GitHub](https://github.com/alberto2005-coder/echo-protocol)
* **Retos superados en el código**:
  * **Física y detección de impactos en Three.js**: Implementación de Raycasting multihilo con optimización de BVH (*Bounding Volume Hierarchy*) para calcular trayectorias balísticas en tiempo real con decenas de entidades concurrentes.
  * **Audio procedural con Web Audio API**: Generación de sintetizadores en tiempo real en lugar de cargar archivos `.wav`/`.mp3` pesados, ahorrando ancho de banda y permitiendo disparos y pasos dinámicos según el material de la superficie.
  * **Empaquetado multiplataforma con Tauri**: Integración de Rust como backend nativo de bajo consumo de RAM (< 80 MB frente a los 300+ MB de Electron).

---

### Proyectos Destacados de Software & IA

| Proyecto | Stack Principal | Descripción Clave |
| :--- | :--- | :--- |
| **[auto-clipper-ai](https://github.com/alberto2005-coder/auto-clipper-ai)** | Python, Faster-Whisper, Ollama, Groq, FFmpeg | Extracción automática de clips virales para TikTok/Shorts mediante LLMs, subtítulos ASS dinámicos y reencuadre vertical 9:16. |
| **[aegis-osint-suite](https://github.com/alberto2005-coder/aegis-osint-suite)** | JavaScript, Node.js, Docker, Criptografía | Plataforma de inteligencia en fuentes abiertas (OSINT), análisis forense de metadatos EXIF y esteganografía. |
| **[NovaEscrow](https://github.com/alberto2005-coder/NovaEscrow)** | Python, Web3, AES-256, Discord API | Bot automatizado de custodia criptográfica multi-red (BTC, LTC, ETH, SOL, USDT, USDC) con derivación determinista de billeteras. |
| **[eco-lang](https://github.com/alberto2005-coder/eco-lang)** | Python, Compiladores, Lexer/Parser, AST | Lenguaje de programación estructurado con sintaxis nativa en español, analizador sintáctico, AST e IDE propio. |
| **[AviTrack](https://github.com/alberto2005-coder/AviTrack)** | Flutter, Dart, SQLite | Aplicación móvil nativa para criadores de aves: trazabilidad genealógica y almacenamiento privado sin nube. |
| **[Noticias_android](https://github.com/alberto2005-coder/Noticias_android)** | Kotlin, Jetpack Compose, Room, WorkManager | Aplicación móvil Android con arquitectura limpia, sincronización en segundo plano y persistencia reactiva. |
| **[HermitVault](https://github.com/alberto2005-coder/HermitVault)** | Python, Criptografía, AES-256 | Gestor de credenciales Zero-Knowledge offline-first sin servidores intermedios para máxima resistencia a filtraciones. |
| **[FFmpegSuit](https://github.com/alberto2005-coder/ffmpeg)** | Java, Swing, Concurrencia, FFmpeg | Herramienta de escritorio con interfaz gráfica y procesamiento multimedia multihilo con soporte Drag & Drop. |
| **[odoo-dynamic-pricing](https://github.com/alberto2005-coder/odoo-dynamic-pricing)** | Python, Odoo ERP, Web Scraping | Módulo ERP para monitorización de precios de competencia en tiempo real y ajuste algorítmico de márgenes. |
| **[MonitorPro](https://github.com/alberto2005-coder/MonitorPro)** | Swift, SwiftUI, macOS Kernel (sysctl) | Monitor de sistema nativo para la barra de menú de macOS con métricas por núcleo de CPU y sensores térmicos. |

---

### Arquitectura Web & Optimizaciones del Portfolio

* **Rendimiento extremo sin frameworks pesados**: Maquetación en HTML5 semántico, CSS moderno con variables y animaciones nativas por GPU, y JavaScript ES6+ modular diferido.
* **PWA & Offline Ready**: Service Worker y [site.webmanifest](site.webmanifest) con iconos maskable y convenciones PWA de escritorio y móvil.
* **SEO Local & Datos Estructurados**: Integración Schema.org en formato JSON-LD (`WebSite`, `Person`, credenciales y autoría) para Knowledge Graph de Google.
* **Compatibilidad Canónica con Agentes de IA**:
  * [llms.txt](llms.txt): Índice y resumen estructurado para LLMs (`LLM Context Summary`).
  * [llms-full.txt](llms-full.txt): Contexto completo sin compresión (`Full LLM Context`) con todo el historial de proyectos y formación.
* **Seguridad reforzada**: Políticas estrictas de *Content Security Policy* (CSP), cabeceras HTTP de protección y `.well-known/security.txt` bajo estándar RFC 9116.
### Mantenimiento del sitio

- **Fuente única**: edita `index.html` (español, con los textos en inglés en `data-lang-en`). La versión inglesa `en/index.html` **se genera**, no se edita a mano:

  ```bash
  pip install beautifulsoup4
  python3 scripts/build_en.py      # regenera /en/index.html
  python3 scripts/verify_site.py   # enlaces, canonical, hreflang, sitemap, JSON-LD, sincronía
  ```

- El CSS incrustado en `index.html` debe coincidir con `assets/css/style.css` (el verificador avisa si no).
- Si cambias `assets/js/script.js`, sube el parámetro `?v=` en `index.html` para invalidar la caché (GitHub Pages cachea ~10 min).
- Al añadir una página nueva, inclúyela en `sitemap.xml` y en la lista de `.github/workflows/indexnow.yml`.

---

## English

### Table of contents

1. [Interactive Projects & Video Games (Technical Deep Dive)](#interactive-projects-video-games-technical-deep-dive)
2. [Featured Software & AI Engineering Projects](#featured-software-ai-engineering-projects)
3. [AI & Machine-Readable Standards](#ai-machine-readable-standards)
4. [Site maintenance](#site-maintenance)

Repository of the official personal website and engineering portfolio of **Alberto Ortiz Sánchez** ([@alberto2005-coder](https://github.com/alberto2005-coder)), Full Stack Developer and Higher Technician in Multiplatform Application Development specialized in Artificial Intelligence and Machine Learning based in Granada, Spain.

Live in production at: **[https://albertoortiz.is-a.dev/](https://albertoortiz.is-a.dev/)**

---

### Interactive Projects & Video Games (Technical Deep Dive)

#### 1. Tetris C++
* **Technologies**: Modern C++ (C++17/20), matrix algorithm logic, low-level console / graphic buffer rendering.
* **Link**: [Play on Itch.io](https://alberto-coder2005.itch.io/tetris-game-c)
* **Engineering challenges solved**:
  * **SRS (Super Rotation System)**: Precise mathematical implementation of collision matrices and wall-kick tables to allow rotations in tight spots without clipping through borders or placed pieces.
  * **Zero-overhead memory & game loop**: Decoupling the game tick logic (constant accelerated gravity per level) from the rendering cycle, avoiding memory leaks and keeping zero external dependencies.
  * **Simultaneous line clearing algorithm**: Recursive row shifting with bitwise verification to accurately process single, double, triple, and quadruple Tetris clears.

#### 2. Neon Dash
* **Technologies**: Flutter, Dart, interactive 2D Canvas, positional audio, reactive animations locked at 60/120 FPS.
* **Link**: [Play on Itch.io](https://alberto-coder2005.itch.io/neon-dash)
* **Engineering challenges solved**:
  * **Rhythm-physics synchronization**: Custom elastic collision engine using Continuous Collision Detection (CCD) to prevent tunneling artifacts at high horizontal velocities.
  * **Rendering optimization on Flutter Web**: Replaced heavy widget trees with custom `CustomPainter` render layers, cutting repaint frame times below 8 ms to eliminate frame drops on mobile web browsers.
  * **Adaptive bloom shader simulation**: Lightweight GPU-friendly radial gradient blending mimicking real-time arcade neon glow effects.

#### 3. The Memory Game (Google Play Store)
* **Technologies**: Unity, C#, Android SDK, Google Play Games Services, encrypted JSON serialization.
* **Link**: [Download on Google Play](https://play.google.com/store/apps/details?id=com.grgames.thememorygames)
* **Engineering challenges solved**:
  * **Procedural difficulty & progressive memory curves**: Controlled pseudorandom pattern generators engineered to challenge cognitive retention while remaining solvable under time constraints.
  * **Anti-tamper local storage**: Symmetric AES encryption on local high-score records preventing score manipulation prior to cloud leaderboard sync.
  * **Mobile lifecycle management**: Graceful handling of `OnApplicationPause` states and memory cleanup ensuring no loss of game progress during phone calls or app switching.

#### 4. Echo Protocol (3D Cyberpunk Arena FPS)
* **Technologies**: React 19, TypeScript, Three.js, WebGL 2.0, procedural Web Audio API, Tauri (Windows Desktop).
* **Link**: [GitHub Repository](https://github.com/alberto2005-coder/echo-protocol)
* **Engineering challenges solved**:
  * **Real-time Raycasting & BVH**: High-performance multi-ray collision detection for ballistic calculations across dynamic moving entities without frame latency.
  * **Procedural Web Audio API sound synthesis**: Fully synthesized audio effects created directly in code without loading heavy audio assets, drastically reducing download payload.
  * **Desktop build with Tauri**: Lightweight Rust native desktop packaging reducing idle RAM footprint to under 80 MB (compared to 300+ MB on Electron).

---

### Featured Software & AI Engineering Projects

* **[auto-clipper-ai](https://github.com/alberto2005-coder/auto-clipper-ai)**: Automated viral short clip creator powered by Faster-Whisper, LLMs (Ollama/Groq) and FFmpeg 9:16 smart reframing.
* **[aegis-osint-suite](https://github.com/alberto2005-coder/aegis-osint-suite)**: Open-source intelligence platform, forensic metadata inspection, and real-time steganography in Docker.
* **[NovaEscrow](https://github.com/alberto2005-coder/NovaEscrow)**: Multi-chain crypto escrow Discord bot supporting BTC, LTC, ETH, SOL, USDT, USDC with deterministic wallet derivation and AES encryption.
* **[eco-lang](https://github.com/alberto2005-coder/eco-lang)**: Spanish-syntax programming language with custom lexer, AST parser, desktop IDE, and standalone executable runner.
* **[AviTrack](https://github.com/alberto2005-coder/AviTrack)**: Native Flutter Android mobile app for avian breeders with genealogical tracking and zero-cloud private storage.
* **[Noticias_android](https://github.com/alberto2005-coder/Noticias_android)**: Native Android news reader with Kotlin, Jetpack Compose, Room SQLite database, and WorkManager background sync.
* **[HermitVault](https://github.com/alberto2005-coder/HermitVault)**: Offline-first Zero-Knowledge password manager with AES-256 symmetric encryption and no cloud dependencies.
* **[FFmpegSuit](https://github.com/alberto2005-coder/ffmpeg)**: Java Swing desktop GUI and CLI tool for multi-threaded multimedia recoding, scaling, and batch Drag & Drop workflows.
* **[odoo-dynamic-pricing](https://github.com/alberto2005-coder/odoo-dynamic-pricing)**: Enterprise Odoo ERP module for real-time competitor web scraping and automated margin repricing.
* **[MonitorPro](https://github.com/alberto2005-coder/MonitorPro)**: Native macOS menu bar hardware monitor written in Swift/SwiftUI querying low-level UNIX kernel sysctl metrics.

---

### AI & Machine-Readable Standards

* `llms.txt`: Canonical markdown summary designed for LLM agents ([LLM Context Summary](https://albertoortiz.is-a.dev/llms.txt)).
* `llms-full.txt`: Comprehensive uncompressed project & credential documentation ([Full LLM Context](https://albertoortiz.is-a.dev/llms-full.txt)).
* `site.webmanifest`: PWA compliance with maskable & any icon variants.
* `sitemap.xml`: Canonical sitemap with live change frequency and priorities.
* `.well-known/security.txt`: RFC 9116 security disclosure guidelines.
### Site maintenance

- **Single source**: edit `index.html` (Spanish, with the English strings in `data-lang-en`). The English version `en/index.html` **is generated**, never hand-edited:

  ```bash
  pip install beautifulsoup4
  python3 scripts/build_en.py      # regenerates /en/index.html
  python3 scripts/verify_site.py   # links, canonical, hreflang, sitemap, JSON-LD, sync
  ```

- The CSS embedded in `index.html` must match `assets/css/style.css` (the verifier warns otherwise).
- If you change `assets/js/script.js`, bump the `?v=` parameter in `index.html` to invalidate the cache (GitHub Pages caches for ~10 min).
- When adding a new page, list it in `sitemap.xml` and in `.github/workflows/indexnow.yml`.

---

## Contact & Links

* **Official Website**: [https://albertoortiz.is-a.dev/](https://albertoortiz.is-a.dev/)
* **Email**: [contacto@albertoortiz.is-a.dev](mailto:contacto@albertoortiz.is-a.dev) / [albertoortixsanchez@gmail.com](mailto:albertoortixsanchez@gmail.com)
* **LinkedIn**: [https://www.linkedin.com/in/alberto-ortiz-sanchez](https://www.linkedin.com/in/alberto-ortiz-sanchez)
* **GitHub**: [https://github.com/alberto2005-coder](https://github.com/alberto2005-coder)
* **Itch.io**: [https://alberto-coder2005.itch.io/](https://alberto-coder2005.itch.io/)

---

⭐ *Desarrollado y mantenido por Alberto Ortiz Sánchez — 2026*
