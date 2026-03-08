function openModal(title,img,instr,video){

var modal = document.getElementById("modal");

var titleBox = document.getElementById("title");
var imageBox = document.getElementById("img");
var instrBox = document.getElementById("instructions");
var videoLink = document.getElementById("video");

modal.style.display = "block";

titleBox.innerText = title;
imageBox.src = img;
instrBox.innerText = instr;
videoLink.href = video;

}

function closeModal(){

document.getElementById("modal").style.display="none";

}

function toggleMode(){

document.body.classList.toggle("dark");

}