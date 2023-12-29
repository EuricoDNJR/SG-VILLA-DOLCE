const modal = document.querySelector('#modal-select-client')
const selectClientBtn = document.querySelector('#select-client-btn')
const registerClientBtn = document.querySelector('#register-client-btn')
const closeModalBtn = document.querySelector('#close-modal-btn')

selectClientBtn.addEventListener('click', () => {
    modal.showModal();
})

closeModalBtn.addEventListener('click', () => {
    modal.close();
})
