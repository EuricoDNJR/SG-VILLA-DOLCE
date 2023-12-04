window.addEventListener('DOMContentLoaded', () => {
  window.ipcRenderer.getUserDataCookie().then(
    (dados) => {
        const nomeElement = document.getElementById("user");
        const cargoElement = document.getElementById("position");

        // AINDA É NECESSÁRIO ATUALIZAR A IMAGEN
        //dados.imagem
        //dados.token
        nomeElement.textContent = dados.nome;
        cargoElement.textContent = dados.cargo;
    })
});
