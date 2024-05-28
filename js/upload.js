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