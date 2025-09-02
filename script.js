document.addEventListener('DOMContentLoaded', () => {
    const tabLinks = document.querySelectorAll('.tab-link');
    const tabContents = document.querySelectorAll('.tab-content');

    tabLinks.forEach(link => {
        link.addEventListener('click', (event) => {
            const targetId = event.target.getAttribute('data-tab-target');
            
            tabLinks.forEach(l => l.classList.remove('active-tab'));
            tabContents.forEach(c => c.classList.remove('active-content'));

            event.target.classList.add('active-tab');
            document.querySelector(targetId).classList.add('active-content');
        });
    });
});
