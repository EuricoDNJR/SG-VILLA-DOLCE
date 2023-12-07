const { app, BrowserWindow, ipcMain } = require('electron')
const path = require('node:path')

let mainWindow;

const createWindow = () => {
  mainWindow = new BrowserWindow({
    width: 800,
    height: 600,
    minWidth: 800,
    minHeight: 600,
    autoHideMenuBar: true,
    webPreferences: {
      preload: path.join(__dirname, 'preload.js'),
      partition: 'persist:secureSession'
    }
  })

  mainWindow.loadFile('login/login.html')
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

ipcMain.handle('login-bem-sucedido', (event, redirectPage) => {
  mainWindow.loadFile(redirectPage);
});

ipcMain.handle('salvar-dados-no-cookie', async (event, dados) => {
  await mainWindow.webContents.session.cookies.set({
      url: 'http://localhost',
      name: 'dadosDoUsuário',
      value: JSON.stringify(dados),
      httpOnly: true,
      secure: true
  });
});

ipcMain.handle('obter-dados-do-cookie', async () => {
  const cookies = await mainWindow.webContents.session.cookies.get({
      url: 'http://localhost',
      name: 'dadosDoUsuário'
  });

    const dados = JSON.parse(cookies[0].value);
    
    return dados;
});