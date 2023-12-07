const { contextBridge, ipcRenderer } = require('electron')

contextBridge.exposeInMainWorld('ipcRenderer', {
  redirectTo: (redirectPageUrl) => ipcRenderer.invoke('redirecionar-pagina', redirectPageUrl),
  setUserDataCookie: (userData) => ipcRenderer.invoke('salvar-dados-no-cookie', userData),
  getUserDataCookie: () => ipcRenderer.invoke('obter-dados-do-cookie')
  // we can also expose variables, not just functions
})