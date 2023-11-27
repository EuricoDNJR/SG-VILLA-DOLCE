function botao(){
    let titulo = document.getElementById("title");
    const update = {
        "senha": "senha_abashla",
        "telefone": "123456782"
    };

    const options = {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(update),  
    };

    fetch("http://127.0.0.1:8000/v1/usuario/login/", options).then(
        (response) => {
            console.log(response);
            titulo.textContent = `${response.status} `;
            return response.json();
        }).then((jeison) => {
            titulo.textContent += jeison.message;
        })
}

const btn = document.getElementById("btn");
btn.addEventListener("click", botao);
