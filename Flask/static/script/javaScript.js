var navLinks = document.getElementsById("navLinks");

var clicked = false;

text.onclick = copyFun;

function copyFun(){
    navigator.clipboard.writeText("bartjozwicki@gmail.com")
    .then((res) => alert("Copied: bartjozwicki@gmail.com"))
    .catch((err) => alert("Copy failed..."))
}

function showMenu(){
    navLinks.style.right = "0";
}
function hideMenu(){
    navLinks.style.right = "-200px";
 
}