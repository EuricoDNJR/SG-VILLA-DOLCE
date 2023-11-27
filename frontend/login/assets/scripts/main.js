const btn = document.getElementById("btn");
btn.addEventListener("click", requestLogin);

//function trataDadosLogin(){}

async function requestLogin(event){
    event.preventDefault();
    //const data = trataDadosLogin();
    const cellphone = document.getElementById("cellphone");
    const password = document.getElementById("password");

    const options = {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            telefone: String(cellphone.value),
            senha: String(password.value),
        })
    };
    console.log(options);
    fetch("http://127.0.0.1:8000/v1/usuario/login/", options).then(
        (response) => {
            console.log(response);
            if(!response.ok){
                const responseJsonPromise = response.json();

                responseJsonPromise.then(
                    (responseJson) => {
                        console.log(responseJson);
                        const errorMessage = document.getElementById("error-message");

                        errorMessage.textContent = responseJson.message;
                        errorMessage.style.display = "block";
                    }
                )
            }else{
                // USUÁRIO AUTORIZADO
                // REDIRECIONAR PARA PÁGINA DASHBOARD
                // PRECISO DE ALGUNS DADOS DO USUÁRIO -> NOME, CARGO e IMAGEM
            }
        })
    }