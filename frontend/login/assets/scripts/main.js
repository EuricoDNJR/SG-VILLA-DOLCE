const btn = document.getElementById("btn");
btn.addEventListener("click", requestLogin);

function trataDadosLogin(){
    const cellphone = document.getElementById("cellphone");
    const password = document.getElementById("password");
    
    // TRATAR DADOS AQUI 

    return {
        "telefone": cellphone.value,
        "senha": password.value,
    };
}

function requestLogin(){
    const data = trataDadosLogin();

    const options = {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(data),  
    };

    fetch("http://127.0.0.1:8000/v1/usuario/login/", options).then(
        (response) => {
            if(!response.ok){
                const responseJsonPromise = response.json();

                responseJsonPromise.then(
                    (message) => {
                        const errorMessage = document.getElementById("error-message");

                        errorMessage.textContent = message;
                        errorMessage.style.display = block;
                    }
                )
            }else{
                // USUÁRIO AUTORIZADO
                // REDIRECIONAR PARA PÁGINA DASHBOARD
                // PRECISO DE ALGUNS DADOS DO USUÁRIO -> NOME, CARGO e IMAGEM
            }
        })
}
