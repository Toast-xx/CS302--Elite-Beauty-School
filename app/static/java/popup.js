window.addEventListener('load', function() {
    initDragAndDrop();
});
function overlay(id)
{
    document.getElementById('popup').style.display='flex';
    const targets = document.querySelectorAll('.overlay');
    targets.forEach(target => {
    target.classList.remove('active');
    if (target.dataset.id === id) {
      target.classList.add('active');
    }});
}
function CloseOverlay()
{
    document.getElementById('popup').style.display='none';
}
let file_data= null;
function initDragAndDrop() {
  const dropArea = document.getElementById('drop-area');
  if (!dropArea) return; // Exit if no drop area

  // Prevent default drag behaviors
  ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
    dropArea.addEventListener(eventName, e => {
      e.preventDefault();
      e.stopPropagation();
    }, false);
  });

  // Highlight drop area on dragenter and dragover
  ['dragenter', 'dragover'].forEach(eventName => {
    dropArea.addEventListener(eventName, () => {
      dropArea.classList.add('highlight');
    }, false);
  });

  // Remove highlight on dragleave and drop
  ['dragleave', 'drop'].forEach(eventName => {
    dropArea.addEventListener(eventName, () => {
      dropArea.classList.remove('highlight');
    }, false);
  });

  // Handle dropped files
  dropArea.addEventListener('drop', e => {
    const files = e.dataTransfer.files;
    handleFiles(files);
  });

  // Optional: handle files selected with file input inside drop area
  const fileInput = dropArea.querySelector('input[type="file"]');
  if (fileInput) {
    fileInput.addEventListener('change', () => {
      handleFiles(fileInput.files);
    });
  }
}
function handleFiles(files) {
  const fileList = document.getElementById('file-list');
  if (!fileList) return;

  if (files.length === 0) {
    file_data = null;
    return;
  }

  // Only allow PDF files
  const file = files[0];
  if (file && !['image/jpeg', 'image/png'].includes(file.type)) {
  alert('Only JPG and PNG files are allowed.');
  return;
  }
  file_data = file;
  fileList.innerHTML = ''; // Clear previous files
  [...files].forEach(file => {
    const item = document.createElement('div');
    item.textContent = file.name;
    fileList.appendChild(item);
  });
}
function transferStock()
{
    const campus=document.getElementById('transferCampus');
    const reason=document.getElementById('transferReason');
    const quantity=document.getElementById('transferQuantity');
    if(campus.value=="all")
    {
        alert("Please select the campus!");
        return;
    }
    if(quantity.value.trim()===""||quantity.value==0)
    {
        alert("Please input a valid quantity!");
        return;
    }
    if(reason.value.trim()==="")
    {
        alert("Please input the reason!");
        return;
    }
}
function addStock()
{
    const quantity=document.getElementById('addQuantity');
    if(quantity.value.trim()===""||quantity.value==0)
    {
        alert("Please input a valid quantity!");
        return;
    }
}
function deleteProduct()
{

}