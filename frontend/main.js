function botao(){
    let titulo = document.getElementById("title");

    fetch("http://127.0.0.1:8000").then((response) => {
        return response.text();
    }).then((texto) => {
        titulo.textContent = texto;
    })
}

titulo.textContent = "Carregando requisição";