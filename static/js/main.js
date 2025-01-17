document.addEventListener('DOMContentLoaded', function() {
    const sidebar = document.getElementById('sidebar');
    const sidebarToggle = document.getElementById('sidebarToggle');
    const mainContent = document.querySelector('.main-content');
    const topNavbar = document.querySelector('.top-navbar');
    const footer = document.querySelector('.footer');

    // Check screen size
    function isMobileScreen() {
        return window.innerWidth <= 768;
    }

    // Check if there's a saved sidebar state in localStorage
    const isMinimized = localStorage.getItem('sidebarMinimized') === 'true';
    
    // Function to apply minimized state
    function applySidebarState(minimized) {
        if (minimized) {
            sidebar.classList.add('minimized');
            mainContent.style.marginLeft = '80px';
            mainContent.style.width = 'calc(100% - 80px)';
            topNavbar.style.marginLeft = '80px';
            topNavbar.style.width = 'calc(100% - 80px)';
            footer.style.marginLeft = '80px';
            footer.style.width = 'calc(100% - 80px)';
        } else {
            sidebar.classList.remove('minimized');
            mainContent.style.marginLeft = '250px';
            mainContent.style.width = 'calc(100% - 250px)';
            topNavbar.style.marginLeft = '250px';
            topNavbar.style.width = 'calc(100% - 250px)';
            footer.style.marginLeft = '250px';
            footer.style.width = 'calc(100% - 250px)';
        }
    }

    // Function to toggle sidebar on mobile
    function toggleMobileSidebar() {
        // If sidebar is hidden, show it fully
        if (sidebar.style.width === '0px' || sidebar.style.width === '') {
            sidebar.style.width = '250px';
            sidebar.style.overflow = 'visible';
            mainContent.style.filter = 'blur(5px)';
            mainContent.style.pointerEvents = 'none';
            
            // Create an overlay to close sidebar when clicking outside
            const overlay = document.createElement('div');
            overlay.id = 'sidebar-overlay';
            overlay.style.cssText = `
                position: fixed;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                background: rgba(0,0,0,0.5);
                z-index: 999;
            `;
            overlay.addEventListener('click', () => {
                toggleMobileSidebar();
            });
            document.body.appendChild(overlay);
        } else {
            // Hide sidebar
            sidebar.style.width = '0px';
            sidebar.style.overflow = 'hidden';
            mainContent.style.filter = 'none';
            mainContent.style.pointerEvents = 'auto';
            
            // Remove overlay
            const overlay = document.getElementById('sidebar-overlay');
            if (overlay) {
                overlay.remove();
            }
        }
    }

    // Apply saved state on page load
    if (isMinimized && !isMobileScreen()) {
        applySidebarState(true);
    }

    // Toggle sidebar on button click
    sidebarToggle.addEventListener('click', function() {
        // Check if it's a mobile screen
        if (isMobileScreen()) {
            toggleMobileSidebar();
        } else {
            // Desktop behavior
            const minimized = !sidebar.classList.contains('minimized');
            applySidebarState(minimized);
            localStorage.setItem('sidebarMinimized', minimized);
        }
    });

    // Preserve minimized state when navigating between pages
    const sidebarLinks = document.querySelectorAll('.sidebar-nav-item');
    sidebarLinks.forEach(link => {
        link.addEventListener('click', function() {
            // Save current minimized state before navigation
            localStorage.setItem('sidebarMinimized', sidebar.classList.contains('minimized'));
            
            // If on mobile, close sidebar after navigation
            if (isMobileScreen()) {
                toggleMobileSidebar();
            }
        });
    });

    // Adjust layout on window resize
    window.addEventListener('resize', function() {
        // Reset sidebar for mobile/desktop
        if (isMobileScreen()) {
            sidebar.style.width = '0px';
            sidebar.style.overflow = 'hidden';
            mainContent.style.marginLeft = '0';
            mainContent.style.width = '100%';
            topNavbar.style.marginLeft = '0';
            topNavbar.style.width = '100%';
            footer.style.marginLeft = '0';
            footer.style.width = '100%';
        } else {
            // Reapply desktop state
            const wasMinimized = localStorage.getItem('sidebarMinimized') === 'true';
            applySidebarState(wasMinimized);
        }
    });
});

