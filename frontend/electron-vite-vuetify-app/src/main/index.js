import { app, shell, BrowserWindow, ipcMain, dialog } from 'electron'
import { join } from 'path'
import { spawn } from 'child_process'
import { electronApp, optimizer, is } from '@electron-toolkit/utils'
import icon from '../../resources/icon.png?asset'

let mainWindow = undefined;
let backendProcess = undefined;

function resolveBackendExecutablePath() {
  return join(process.resourcesPath, 'backend', 'villa-api.exe')
}

async function waitForBackendReady(timeoutMs = 15000) {
  const startTime = Date.now()

  while (Date.now() - startTime < timeoutMs) {
    try {
      const response = await fetch('http://127.0.0.1:8000/')
      if (response.ok) {
        return true
      }
    } catch (error) {
      // Backend not available yet.
    }

    await new Promise((resolve) => setTimeout(resolve, 500))
  }

  return false
}

async function startBackend() {
  if (is.dev) {
    console.log('[backend] Development mode: backend must be started manually.')
    return true
  }

  const backendExecutablePath = resolveBackendExecutablePath()
  backendProcess = spawn(backendExecutablePath, [], {
    cwd: join(process.resourcesPath, 'backend'),
    windowsHide: true,
  })

  backendProcess.on('error', (error) => {
    console.error('[backend] Failed to start backend process:', error)
  })

  backendProcess.on('exit', (code, signal) => {
    console.log(`[backend] Process exited with code=${code} signal=${signal}`)
  })

  const isBackendReady = await waitForBackendReady()
  if (!isBackendReady) {
    console.error('[backend] Backend did not respond on http://127.0.0.1:8000 in time.')
  }

  return isBackendReady
}

function stopBackend() {
  if (backendProcess && !backendProcess.killed) {
    backendProcess.kill()
  }
}

function createWindow() {
  mainWindow = new BrowserWindow({
    width: 1280,
    height: 720,
    minWidth: 1280,
    minHeight: 720,
    show: false,
    autoHideMenuBar: true,
    ...(process.platform === 'linux' ? { icon } : {}),
    webPreferences: {
      preload: join(__dirname, '../preload/index.js'),
      sandbox: false,
    }
  })

  mainWindow.on('ready-to-show', () => {
    // mainWindow.setFullScreen(true);
    // mainWindow.maximize(true);
    mainWindow.show()
  })

  mainWindow.webContents.setWindowOpenHandler((details) => {
    shell.openExternal(details.url)
    return { action: 'deny' }
  })

  // HMR for renderer base on electron-vite cli.
  // Load the remote URL for development or the local html file for production.
  if (is.dev && process.env['ELECTRON_RENDERER_URL']) {
    mainWindow.loadURL(process.env['ELECTRON_RENDERER_URL'])
    mainWindow.webContents.openDevTools()
  } else {
    mainWindow.loadFile(join(__dirname, '../renderer/index.html'))
  }
}

// This method will be called when Electron has finished
// initialization and is ready to create browser windows.
// Some APIs can only be used after this event occurs.
app.whenReady().then(async () => {
  // Set app user model id for windows
  electronApp.setAppUserModelId('com.electron')

  // Default open or close DevTools by F12 in development
  // and ignore CommandOrControl + R in production.
  // see https://github.com/alex8088/electron-toolkit/tree/master/packages/utils
  app.on('browser-window-created', (_, window) => {
    optimizer.watchWindowShortcuts(window)
  })

  await startBackend()
  createWindow()

  app.on('activate', function () {
    // On macOS it's common to re-create a window in the app when the
    // dock icon is clicked and there are no other windows open.
    if (BrowserWindow.getAllWindows().length === 0) createWindow()
  })
})

// Quit when all windows are closed, except on macOS. There, it's common
// for applications and their menu bar to stay active until the user quits
// explicitly with Cmd + Q.
app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') {
    stopBackend()
    app.quit()
  }
})

app.on('before-quit', () => {
  stopBackend()
})

// In this file you can include the rest of your app"s specific main process
// code. You can also put them in separate files and require them here.
ipcMain.handle('window-confirm', async (event, msg) => {
   const dialogObjResponse = await dialog.showMessageBox(
      mainWindow,
      {
          type: 'question',
          buttons: ['Sim', 'Não'],
          title: 'Confirm',
          message: msg,
      }
  );
  
  return dialogObjResponse.response == 0; 
});
