const infoButton = document.getElementById('info-button');
const infoModal = document.getElementById('info-modal');
const closeInfo = document.getElementById('close-info');
const infoContent = document.getElementById('info-content');
const tabButtons = document.querySelectorAll('.tab-btn');

async function loadMarkdown(page) {
    const res = await fetch(`/info-md/${page}`);
    const html = await res.text();
    infoContent.innerHTML = html;
}

tabButtons.forEach(function (btn) {
    btn.addEventListener('click', function () {
        tabButtons.forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        loadMarkdown(btn.dataset.page);
    });
});

infoButton.addEventListener('click', function () {
    infoModal.classList.remove('hidden');

    tabButtons.forEach(b => b.classList.remove('active'));

    const firstTab = tabButtons[0];
    if (firstTab) {
        firstTab.classList.add('active');
        loadMarkdown(firstTab.dataset.page);
    }
});

closeInfo.addEventListener('click', function () {
    infoModal.classList.add('hidden');
});

infoModal.addEventListener('click', function (e) {
    if (e.target === infoModal) {
        infoModal.classList.add('hidden');
    }
});
