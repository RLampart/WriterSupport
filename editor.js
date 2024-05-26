document.addEventListener("DOMContentLoaded",function ()
{
    const content = document.getElementById('editor');
    content.addEventListener('keypress',(KeyboardEvent) => reference());
});
function execCmd(command, value = null) {
    document.execCommand(command, false, value);
}

function saveDoc() {
   content = document.getElementById('editor').innerHTML;
   const text = content.innerText;

   // Create a Blob object with the text
   const blob = new Blob([text], { type: 'text/plain' });

   // Create a URL for the Blob
   const url = URL.createObjectURL(blob);

   // Create a temporary link element
   const a = document.createElement('a');
   a.href = url;
   a.download = 'textfile.txt'; // Set the default file name

   // Programmatically click the link to trigger the download
   a.click();

   // Clean up the URL object
   URL.revokeObjectURL(url);
}

function openDocs() {
    location.assign('files.html');
}


function unhighlightEntries(){   
    choices = document.getElementsByTagName('p');
    for (ele of choices){
        if (ele.classList.contains('highlight')){
            ele.classList.remove('highlight');
        } 
    }
}

function updateAside(results, search,len){
    const aside = document.getElementById('results');
    editor = document.getElementById('editor');
    child = editor.firstChild;
    if (child.innerText == undefined){
        const sp1 = document.createElement("span");
        sp1.textContent = child.nodeValue;
        editor.replaceChild(sp1,child);
    }
    children = editor.childNodes;
    choices = []
    for (child of children){
        if (child.innerText!='\n'){
            choices.push(child);
        }
    }
    total = results.pop();
    aside.innerText = search.slice(0,60) + '...';
    print = '\n';
    for (r of results){
         r0 = r.split(':');
         numbers = r0[0].split(' ');
         num = numbers[1];
         if (num >= total-len+1){
            index = num-(total-len+1);
            para = choices[index].innerText;
            r1 = r0[1].split('(');
            r3 = '(' + r1[1] + ': ' + r0[2].slice(0,8) + '])';
            if (para.length>100){
                para = para.slice(0,100) + '...';
            }
            r2 = r0[0]+': '+ para + ' '+ r3;
            choices[index].classList.add("highlight");
         }
         else{
            r2 = 'Paragraph '+num+': Refer to document';
         }
         
         print += r2;
         print += '\n';
    }
    aside.innerText += print;
}

async function reference(){
    if (event.key == 'Enter'){
        unhighlightEntries();
        let aside = document.getElementById('results');
        aside.innerText = '';
        content = document.getElementById('editor');
        text = content.innerText;
        format = content.innerHTML;
        lines = text.split('\n');
        lines = lines.filter((x)=> x!='');
        sentence = lines.length;
        if (sentence>1){
            paper = lines.slice(0,sentence-1);
            paper = paper.join('\n');
            search = lines[sentence-1];
            json = JSON.stringify({doc:paper,term:search});
            result = await postData(json);
            updateAside(result,search,sentence-1);
        }
        
    }
       
}

async function postData(json) {
    url = 'http://localhost:8080/v1/references';
    const response = await fetch(url, {
      method: 'POST', 
      headers: {
        'Content-Type': 'application/json'
      },
      body: json
    });
    return response.json();
  }






