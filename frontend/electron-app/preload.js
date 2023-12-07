const { contextBridge, ipcRenderer } = require('electron')

contextBridge.exposeInMainWorld('ipcRenderer', {
  successfulLogin: (redirectPage) => ipcRenderer.invoke('login-bem-sucedido', redirectPage),
  setUserDataCookie: (userData) => ipcRenderer.invoke('salvar-dados-no-cookie', userData),
  getUserDataCookie: () => ipcRenderer.invoke('obter-dados-do-cookie')
  // we can also expose variables, not just functions
})