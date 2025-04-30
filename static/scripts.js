// Smooth scroll to the features section
function scrollToFeatures() {
    document.querySelector('#features').scrollIntoView({ behavior: 'smooth' });
}

// Open the login modal
function openLoginModal() {
    document.getElementById('login-modal').style.display = "block";
}

// Close the login modal
function closeModal() {
    document.getElementById('login-modal').style.display = "none";
}

// Event listener to close the modal when clicking outside of it
window.onclick = function(event) {
    if (event.target == document.getElementById('login-modal')) {
        closeModal();
    }
}
