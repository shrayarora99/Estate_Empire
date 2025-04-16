document.addEventListener('DOMContentLoaded', function() {
  const statusDiv = document.getElementById('loading-status');
  if (statusDiv) {
    statusDiv.textContent = 'Page loaded successfully! If you can see this message, JavaScript is working.';
    statusDiv.style.color = '#2ecc71';
  }
});