var GET=[];
cQueryString = location.search.substr(1);
aQueryString = cQueryString.split("&");

for(i=0,len=aQueryString.length; i<len; i++){
    aKeyVal = aQueryString[i].split("=");
    cKey=aKeyVal[0];
    cVal=aKeyVal[1];
    GET[cKey]=decodeURI(cVal);
}

if(GET['f']){
    if (GET['f'] == "windows") {
        document.getElementById("forX").innerHTML = "para Windows";
    }
    if (GET['f'] == "python") {
        document.getElementById("forX").innerHTML = "C&oacute;digo Fuente ";
    }
}

function download() {
    let lang = document.getElementById("lang").value;
    if (lang == "english" && GET['f'] == "windows") {
        window.open("https://github.com/PasteLuengas/MyTag/blob/main/MyTag%20-%20English.exe?raw=true");
    }
    if (lang == "english" && GET['f'] == "python") {
        window.open("https://raw.githubusercontent.com/PasteLuengas/MyTag/main/main_english.py");
    }
    if (lang == "spanish" && GET['f'] == "windows") {
        window.open("https://github.com/PasteLuengas/MyTag/blob/main/MyTag%20-%20Spanish.exe?raw=true");
    }
    if (lang == "spanish" && GET['f'] == "python") {
        window.open("https://raw.githubusercontent.com/PasteLuengas/MyTag/main/main_spanish.py");
    }
}