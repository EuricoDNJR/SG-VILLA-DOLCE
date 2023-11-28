const nomeElement = document.getElementById("user");
const cargoElement = document.getElementById("position");
const params = new URLSearchParams(window.location.search);
const nome = params.get('nome');
const cargo = params.get('cargo');
console.log(nomeElement);
// AINDA É NECESSÁRIO ATUALIZAR A IMAGEN
nomeElement.textContent = nome;
cargoElement.textContent = cargo;