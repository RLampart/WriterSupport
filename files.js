document.addEventListener("DOMContentLoaded",function ()
{
    addFiles();
});

async function addFiles(){
    const content = document.getElementById('files');
    content.innerHTML = "";
    data = await getData();
    files = data['files'];
    set = data['set'];
    if (set==null)
        set = [];
    content.innerHTML += "<ul>";
    if (files.length>1){
        for (file of files){
            content.innerHTML += "<li>";
            if (set.includes(file))
                content.innerHTML += `<input class="check" type='checkbox' checked="true" id="${file}">`;
            else
                content.innerHTML += `<input class="check" type='checkbox' id="${file}">`;
            content.innerHTML += `<img src='x icon.png' alt='close icon' class='icon' onclick='removeDoc("${file}")' />`;
            content.innerHTML += "<span>"+file+"</span>";
            content.innerHTML += "</li>";
        }
    }else if (files.length==1){
        content.innerHTML += "<li>";
        if (set.includes(files[0]))
            content.innerHTML += `<input class="check" type='checkbox' checked="true" id="${files}">`;
        else
            content.innerHTML += `<input class="check" type='checkbox' id="${files}">`;
        content.innerHTML += `<img src='x icon.png'  alt='close icon' class='icon' onclick='removeDoc("${files}")' />`;
        content.innerHTML += "<span>"+files+"</span>";
        content.innerHTML += "</li>";
    }
    
    content.innerHTML += "</ul>";
}

async function removeDoc(filename){
    choice = confirm(`Remove ${filename}?`);
    if (choice){
        url = 'http://localhost:8080/v1/removeDoc';
        const response = await fetch(url, {
        method: 'POST', 
        headers: {
        'Content-Type': 'application/json'
        },
        body: JSON.stringify({"file":filename})
      });
        const result = await response.json();
        addFiles();
        alert(result['msg']);
  }
    
}

async function sendDoc() {
        input = document.getElementById('fileInput');
        const [file] = input.files;
        const formData = new FormData();

        formData.append('files', file);

        try {
            const response = await fetch('http://localhost:8080/v1/upload', {
                method: 'POST',
                body: formData
            });

            if (!response.ok) {
                throw new Error('Network response was not ok ' + response.statusText);
            }

            const result = await response.json();
            alert(result['msg']);
            addFiles();
        } catch (error) {
            console.log(error);
        }
    }

async function setFiles() {
    var files = [];
    boxes = document.getElementsByClassName("check");
    for (box of boxes){
        if (box.checked == true)
            files.push(box.id);
    }
    files = JSON.stringify({"files":files});
    url = 'http://localhost:8080/v1/files';
    const response = await fetch(url, {
        method: 'POST', 
        headers: {
            'Content-Type': 'application/json'
          },
        body: files
    });
    alert("Files Set");
    return response.json();
}

async function getData() {
    url = 'http://localhost:8080/v1/files';
    const response = await fetch(url, {
      method: 'GET', 
    });
    return response.json();
  }






