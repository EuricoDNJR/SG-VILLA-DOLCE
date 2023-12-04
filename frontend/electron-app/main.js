const { app, BrowserWindow, ipcMain } = require('electron')
const path = require('node:path')

const createWindow = () => {
  const win = new BrowserWindow({
    width: 800,
    height: 600,
    webPreferences: {
      preload: path.join(__dirname, 'preload.js'),
      partition: 'persist:secureSession'
    }
  })

  win.loadFile('login/login.html')
}

app.whenReady().then(() => {
  createWindow()

  app.on('activate', () => {
    if (BrowserWindow.getAllWindows().length === 0) {
      createWindow()
    }
  })
})

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') {
    app.quit()
  }
})

ipcMain.handle('salvarDadosNoCookie', async (event, dados) => {
  const mainWindow = BrowserWindow.getAllWindows()[0]; // Obtém a janela principal

  await mainWindow.webContents.session.cookies.set({
      url: 'http://localhost',
      name: 'dadosDoUsuário',
      value: JSON.stringify(dados),
      httpOnly: true,
      secure: true
  });
});

ipcMain.handle('obterDadosDoCookie', async () => {
  const mainWindow = BrowserWindow.getAllWindows()[0]; // Obtém a janela principal
    
  const cookies = await mainWindow.webContents.session.cookies.get({
      url: 'http://localhost',
      name: 'dadosDoUsuário'
    });

    const dados = JSON.parse(cookies[0].value);
    
    return dados;
});