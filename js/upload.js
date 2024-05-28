function updateFileName() {
    const fileInput = document.getElementById('dropzone-file');
    const fileNameDisplay = document.getElementById('file-name');
    const removeFileBtn = document.getElementById('remove-file-btn');
    const file = fileInput.files[0];

    if (file) {
        fileNameDisplay.textContent = `Selected file: ${file.name}`;
        removeFileBtn.classList.remove('hidden');
    } else {
        fileNameDisplay.textContent = '';
        removeFileBtn.classList.add('hidden');
    }
}

function removeFile() {
    const fileInput = document.getElementById('dropzone-file');
    const fileNameDisplay = document.getElementById('file-name');
    const removeFileBtn = document.getElementById('remove-file-btn');

    fileInput.value = '';
    fileNameDisplay.textContent = '';
    removeFileBtn.classList.add('hidden');
}

document.addEventListener('DOMContentLoaded', function() {
    const urlParams = new URLSearchParams(window.location.search);
    const success = urlParams.get('s');
    if (success === 'T') {
        document.getElementById('upload-success-message').classList.remove('hidden');
        setTimeout(function() {
            document.getElementById('upload-success-message').classList.add('hidden');
            
            // Remove success parameter from URL
            const newParams = new URLSearchParams(window.location.search);
            newParams.delete('s');
            const newParamsString = newParams.toString();
            const newUrl = window.location.pathname + (newParamsString ? '?' + newParamsString : '');
            window.history.replaceState({}, '', newUrl);
        }, 2500);
    }
});

function validateFileType() {
    const fileInput = document.getElementById('dropzone-file');
    const fileName = fileInput.value;
    const allowedExtensions = /(\.rar|\.zip)$/i;

    if (!allowedExtensions.exec(fileName)) {
        alert('Invalid file type. Only .rar and .zip files are allowed.');
        return false;
    } else {
        return true;
    }
}

// Function to show spinner when form is submitted
function showSpinner() {
    document.getElementById('upload-spinner').classList.remove('hidden');
    return true; // Allow form submission
}

// Add event listener to form submission
document.getElementById('upload-form').addEventListener('submit', showSpinner);