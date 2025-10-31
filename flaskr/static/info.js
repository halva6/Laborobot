const infoModal = document.getElementById('info-modal');
const infoContent = document.getElementById('info-content');
const infoButton = document.getElementById('info-button');
const closeBtn = document.getElementById('close-info');

infoButton.addEventListener('click', () => {
    fetch('/info-md')
        .then(res => res.text())
        .then(html => {
            infoContent.innerHTML = html;
            infoModal.classList.remove('hidden');
        });
});

closeBtn.addEventListener('click', () => {
    infoModal.classList.add('hidden');
});

infoModal.addEventListener('click', (e) => {
    if (e.target === infoModal) {
        infoModal.classList.add('hidden');
    }
});