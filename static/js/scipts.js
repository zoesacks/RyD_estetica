// Mobile Menu Toggle
document.addEventListener('DOMContentLoaded', function() {
    const menuToggle = document.getElementById('menuToggle');
    const navMenu = document.getElementById('navMenu');
    
    menuToggle.addEventListener('click', function() {
        navMenu.classList.toggle('active');
    });
    
    // Close menu when clicking on a link
    const navLinks = document.querySelectorAll('.nav-link');
    navLinks.forEach(link => {
        link.addEventListener('click', function() {
            navMenu.classList.remove('active');
        });
    });
    
    // Set current year in footer
    document.getElementById('currentYear').textContent = new Date().getFullYear();
    
    // Form submission
    const contactForm = document.getElementById('contactForm');
    if (contactForm) {
        contactForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            // Get form values
            const name = document.getElementById('name').value;
            const email = document.getElementById('email').value;
            const phone = document.getElementById('phone').value;
            const message = document.getElementById('message').value;
            
            // Basic validation
            if (!name || !email || !message) {
                alert('Por favor completa todos los campos requeridos.');
                return;
            }
            
            // Here you would typically send the form data to a server
            // For this example, we'll just show a success message
            alert('¡Gracias por tu mensaje! Te contactaremos pronto.');
            contactForm.reset();
        });
    }
    
    // Smooth scrolling for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            e.preventDefault();
            
            const targetId = this.getAttribute('href');
            if (targetId === '#') return;
            
            const targetElement = document.querySelector(targetId);
            if (targetElement) {
                window.scrollTo({
                    top: targetElement.offsetTop - 80, // Adjust for navbar height
                    behavior: 'smooth'
                });
            }
        });
    });
    
    // Add animation on scroll
    const animateOnScroll = function() {
        const elements = document.querySelectorAll('.service-card, .testimonial-card');
        
        elements.forEach(element => {
            const elementPosition = element.getBoundingClientRect().top;
            const windowHeight = window.innerHeight;
            
            if (elementPosition < windowHeight - 100) {
                element.style.opacity = '1';
                element.style.transform = 'translateY(0)';
            }
        });
    };
    
    // Set initial state for animation
    document.querySelectorAll('.service-card, .testimonial-card').forEach(element => {
        element.style.opacity = '0';
        element.style.transform = 'translateY(20px)';
        element.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
    });
    
    // Run animation on scroll
    window.addEventListener('scroll', animateOnScroll);
    // Run once on load
    animateOnScroll();
});


// Funcionalidad para filtrar servicios
document.addEventListener('DOMContentLoaded', function() {
    const filterButtons = document.querySelectorAll('.filter-btn');
    const serviceItems = document.querySelectorAll('.service-item');
    
    // Función para filtrar servicios
    function filterServices(category) {
        serviceItems.forEach(item => {
            if (category === 'all' || item.dataset.category === category) {
                item.style.display = 'flex';
                // Añadir animación de aparición
                setTimeout(() => {
                    item.style.opacity = '1';
                    item.style.transform = 'translateY(0)';
                }, 100);
            } else {
                item.style.display = 'none';
                item.style.opacity = '0';
                item.style.transform = 'translateY(20px)';
            }
        });
    }
    
    // Event listeners para botones de filtro
    filterButtons.forEach(button => {
        button.addEventListener('click', function() {
            // Remover clase active de todos los botones
            filterButtons.forEach(btn => btn.classList.remove('active'));
            // Añadir clase active al botón clickeado
            this.classList.add('active');
            // Filtrar servicios
            filterServices(this.dataset.filter);
        });
    });
    
    // Enlaces de filtro en el footer
    document.querySelectorAll('.footer-links a[data-filter]').forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const category = this.dataset.filter;
            
            // Activar el botón de filtro correspondiente
            filterButtons.forEach(btn => {
                if (btn.dataset.filter === category) {
                    btn.click();
                }
            });
            
            // Scroll hasta la sección de servicios
            window.scrollTo({
                top: document.querySelector('.services-list').offsetTop - 100,
                behavior: 'smooth'
            });
        });
    });
    
    // Inicializar animaciones
    serviceItems.forEach(item => {
        item.style.opacity = '0';
        item.style.transform = 'translateY(20px)';
        item.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
    });
    
    // Mostrar todos los servicios al cargar
    setTimeout(() => {
        serviceItems.forEach(item => {
            item.style.opacity = '1';
            item.style.transform = 'translateY(0)';
        });
    }, 200);
    
    // Animación al hacer scroll
    window.addEventListener('scroll', function() {
        const serviceItems = document.querySelectorAll('.service-item');
        
        serviceItems.forEach(item => {
            const itemPosition = item.getBoundingClientRect().top;
            const windowHeight = window.innerHeight;
            
            if (itemPosition < windowHeight - 100 && item.style.display !== 'none') {
                item.style.opacity = '1';
                item.style.transform = 'translateY(0)';
            }
        });
    });
});


document.addEventListener('DOMContentLoaded', function() {
    // Mobile Menu Toggle
    const menuToggle = document.getElementById('menuToggle');
    const navMenu = document.getElementById('navMenu');
    
    if (menuToggle && navMenu) {
        menuToggle.addEventListener('click', function() {
            navMenu.classList.toggle('active');
        });
        
        // Close menu when clicking on a link
        const navLinks = document.querySelectorAll('.nav-link');
        navLinks.forEach(link => {
            link.addEventListener('click', function() {
                navMenu.classList.remove('active');
            });
        });
    }
    
    // Set current year in footer
    const currentYearElement = document.getElementById('currentYear');
    if (currentYearElement) {
        currentYearElement.textContent = new Date().getFullYear();
    }
    
    // Form submission
    const contactForm = document.getElementById('contactForm');
    if (contactForm) {
        contactForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            // Get form values
            const name = document.getElementById('name').value;
            const email = document.getElementById('email').value;
            const phone = document.getElementById('phone').value;
            const subject = document.getElementById('subject').value;
            const message = document.getElementById('message').value;
            const privacy = document.getElementById('privacy').checked;
            
            // Basic validation
            if (!name || !email || !message || !privacy) {
                alert('Por favor completa todos los campos requeridos y acepta la política de privacidad.');
                return;
            }
            
            // Here you would typically send the form data to a server
            // For this example, we'll just show a success message
            alert('¡Gracias por tu mensaje! Te contactaremos pronto.');
            contactForm.reset();
        });
    }
    
    // Animation on scroll for elements
    const animateOnScroll = function() {
        const elements = document.querySelectorAll('.value-card, .tech-item, .brand-item, .category-item');
        
        elements.forEach(element => {
            const elementPosition = element.getBoundingClientRect().top;
            const windowHeight = window.innerHeight;
            
            if (elementPosition < windowHeight - 100) {
                element.style.opacity = '1';
                element.style.transform = 'translateY(0)';
            }
        });
    };
    
    // Set initial state for animation
    document.querySelectorAll('.value-card, .tech-item, .brand-item, .category-item').forEach(element => {
        element.style.opacity = '0';
        element.style.transform = 'translateY(20px)';
        element.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
    });
    
    // Run animation on scroll
    window.addEventListener('scroll', animateOnScroll);
    // Run once on load
    animateOnScroll();
});