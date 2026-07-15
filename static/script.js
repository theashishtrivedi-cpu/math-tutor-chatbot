async function solveQuestion(){

const question=document.getElementById("question").value;

if(question.trim()===""){

alert("Please enter a question.");

return;

}

document.getElementById("answer").innerHTML="⏳ AI is thinking...";

const response=await fetch("/solve?question="+encodeURIComponent(question));

const data=await response.json();

document.getElementById("answer").innerText=data.answer;

}