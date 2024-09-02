function toggleMenu() {
    const menu = document.querySelector(".menu-links");
    const icon = document.querySelector(".hamburger-icon");
    menu.classList.toggle("open");
    icon.classList.toggle("open");
}

function scrollToSection(sectionId) {
    const targetSection = document.getElementById(sectionId);
    if (targetSection) {
        targetSection.scrollIntoView({ behavior: 'smooth' });
    }
}

function openLinkInNewTab(url) {
    window.open(url, '_blank');
}

document.addEventListener("DOMContentLoaded", function() {
    const detailsContainer = document.querySelector('[data-container="details-container1"]');

    if (detailsContainer) {
        const articleContainer = detailsContainer.querySelector('.article-container');

        if (articleContainer) {
            // Function to update the CSS variable
            const updateArticleHeight = () => {
                const articleHeight = articleContainer.scrollHeight;
                detailsContainer.style.setProperty('--article-height', `${articleHeight + 80}px`);
            };

            // Initial update
            updateArticleHeight();

            // Create a ResizeObserver to watch for changes in articleContainer size
            const resizeObserver = new ResizeObserver(updateArticleHeight);
            resizeObserver.observe(articleContainer);

            // Optionally, observe the detailsContainer itself if needed
            resizeObserver.observe(detailsContainer);
        } else {
            console.error('Article container not found');
        }
    } else {
        console.error('Details container not found');
    }
});
