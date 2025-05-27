document.getElementById('bookingForm').addEventListener('submit', function () {
    document.getElementById('loading').style.display = 'block';
});

function showModal(message) {
    const modal = document.getElementById('confirmationModal');
    document.getElementById('confirmationMessage').textContent = message;
    modal.style.display = 'block';
}

function closeModal() {
    document.getElementById('confirmationModal').style.display = 'none';
}

