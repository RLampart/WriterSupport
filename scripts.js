document.addEventListener("DOMContentLoaded",function ()
{
    input = document.getElementById('fileInput');
});
function execCmd(command, value = null) {
    document.execCommand(command, false, value);
}
function saveDoc() {
    const content = document.getElementById('editor').innerHTML;
    localStorage.setItem('document', content);
    alert('Document saved!');
}

function loadDoc() {
    input.click(); 
}

function readDoc() {
    input = document.getElementById('fileInput');
    input.addEventListener("change", async () => {
        const [file] = input.files;
        if (file) {
            reader = new FileReader();
            text = await file;
            reader.addEventListener("load", () => {
                document.getElementById('editor').innerText = reader.result;
              }, false);
            reader.readAsText(text);
        } 
    });}

