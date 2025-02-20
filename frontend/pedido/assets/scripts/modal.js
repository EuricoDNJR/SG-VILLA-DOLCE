const modalSelectClient = document.querySelector('#modal-select-client')
const selectClientBtn = document.querySelector('#select-client-btn')
const closeModalSelectClientBtn = document.querySelector('#close-modal-select-client-btn')

const modalRegisterClient = document.querySelector('#modal-register-client')
const registerClientBtn = document.querySelector('#register-client-btn')
const closeModalRegisterClient = document.querySelector('#close-modal-register-client-btn')

selectClientBtn.addEventListener('click', () => {
    modalSelectClient.showModal();
})

closeModalSelectClientBtn.addEventListener('click', () => {
    modalSelectClient.close();
})


registerClientBtn.addEventListener('click', () => {
    modalRegisterClient.showModal();
})

closeModalRegisterClient.addEventListener('click', () => {
    modalRegisterClient.close();
})
