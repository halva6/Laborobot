// Create tooltip element
const tooltip = document.createElement('div');
tooltip.className = 'tooltip';
document.body.appendChild(tooltip);

let activeElement = null;

// Show the tooltip for a given element
function showTooltip(element) {
  const text = element.getAttribute('data-tooltip');
  if (!text) {
    return
  }

  tooltip.textContent = text;
  tooltip.classList.add('show');
  positionTooltip(element);
}

// Hide the tooltip
function hideTooltip() {
  tooltip.classList.remove('show');
}

// Position the tooltip above the element and keep it on screen
function positionTooltip(element) {
  const rect = element.getBoundingClientRect();
  const ttRect = tooltip.getBoundingClientRect();

  let top = rect.top - ttRect.height - 8; // distance above the element
  let left = rect.left + (rect.width / 2) - (ttRect.width / 2);

  // Prevent tooltip from going outside the viewport
  if (top < 0) {
    top = rect.bottom + 8; // place below if there's no space above
  }
  if (left < 0) {
    left = 8;
  }
  if (left + ttRect.width > window.innerWidth) {
    left = window.innerWidth - ttRect.width - 8;
  }

  tooltip.style.top = `${top}px`;
  tooltip.style.left = `${left}px`;
}

// Handle mouseover event
document.addEventListener('mouseover', function (event) {
  const target = event.target.closest('[data-tooltip]');
  if (target && target !== activeElement) {
    activeElement = target;
    showTooltip(target);
  }
});

// Handle mouseout event
document.addEventListener('mouseout', function (event) {
  if (activeElement && !event.relatedTarget?.closest('[data-tooltip]')) {
    hideTooltip();
    activeElement = null;
  }
});

// Reposition tooltip when scrolling or resizing
window.addEventListener('scroll', function () {
  if (activeElement) {
    positionTooltip(activeElement);
  }
}, true);

window.addEventListener('resize', function () {
  if (activeElement) {
    positionTooltip(activeElement);
  }
});
