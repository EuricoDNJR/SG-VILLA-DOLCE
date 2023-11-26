const btn = document.getElementById("btn");
btn.addEventListener("click", requestLogin);

function requestLogin(){
    const cellphone = document.getElementById("cellphone");
    const password = document.getElementById("password");
    const data = {
        "telefone": cellphone.value,
        "senha": password.value,
    };

    const options = {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(data),  
    };

    // fetch("http://127.0.0.1:8000/v1/usuario/login/", options).then(
    //     (response) => {
    //         console.log(response);
    //         titulo.textContent = `${response.status} `;
    //         return response.json();
    //     }).then(
    //         (jeison) => {
    //         titulo.textContent += jeison.message;
    //     })
}
