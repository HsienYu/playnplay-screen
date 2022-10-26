const { app, BrowserWindow, screen } = require('electron')
const path = require('path')
// const url = require('url')


let win;

function createWindow() {
    const win = new BrowserWindow({
        x: 0,
        y: 0,
        width: 800,
        height: 600,
        focusable: false,
        transparent: true,
        frame: false,
        fullscreen: false,
        alwaysOnTop: true,
        skipTaskbar: true,
        enableLargerThanScreen: false,
        webPreferences: {
            preload: path.join(__dirname, './js/preload.js'),
            nodeIntegration: true,
            contextIsolation: false,
            nodeIntegrationInWorker: true,
            webSecurity: false,
            allowRunningInsecureContent: true
        }
    })

    win.setSize(800, 600);
    // //add mouse press through
    //win.setIgnoreMouseEvents(true);

    // Open the DevTools.
    win.webContents.openDevTools();


    win.loadFile('./index.html')
}

app.commandLine.appendSwitch('ignore-certificate-errors');

//enable hardware acceleration
app.disableHardwareAcceleration(true);

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

// In this file you can include the rest of your app's specific main process
// code. You can also put them in separate files and require them here.