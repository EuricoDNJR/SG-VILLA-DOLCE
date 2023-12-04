const { contextBridge, ipcRenderer } = require('electron')

contextBridge.exposeInMainWorld('ipcRenderer', {
  setUserDataCookie: (userData) => ipcRenderer.invoke('salvarDadosNoCookie', userData),
  getUserDataCookie: () => ipcRenderer.invoke('obterDadosDoCookie')
  // we can also expose variables, not just functions
})