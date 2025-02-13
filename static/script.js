document.addEventListener('DOMContentLoaded', () => {
    const themeToggle = document.getElementById('theme-toggle');
    
    // Check for saved theme preference or default to light theme
    const savedTheme = localStorage.getItem('theme') || 'light';
    document.body.className = `${savedTheme}-theme`;
    themeToggle.checked = savedTheme === 'dark';
    
    // Theme toggle functionality
    themeToggle.addEventListener('change', () => {
        if (themeToggle.checked) {
            document.body.className = 'dark-theme';
            localStorage.setItem('theme', 'dark');
        } else {
            document.body.className = 'light-theme';
            localStorage.setItem('theme', 'light');
        }
    });
});

