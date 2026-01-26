#!/usr/bin/env node
/**
 * Servidor web simple para la herramienta de anotación de callos (Node.js).
 * 
 * Requisito: npm install -g http-server
 * 
 * Uso:
 *    node servidor_local.js
 * 
 * O directamente:
 *    npx http-server web -p 8000 -c-1
 */

const http = require('http');
const fs = require('fs');
const path = require('path');
const os = require('os');

const PORT = 8000;
const WEB_DIR = path.join(__dirname, 'web');

// Verificar que existe el directorio web
if (!fs.existsSync(WEB_DIR)) {
  console.error(`[ERROR] No se encontró el directorio web: ${WEB_DIR}`);
  process.exit(1);
}

// Obtener IP local
function getLocalIP() {
  const interfaces = os.networkInterfaces();
  for (const name of Object.keys(interfaces)) {
    for (const iface of interfaces[name]) {
      if (iface.family === 'IPv4' && !iface.internal) {
        return iface.address;
      }
    }
  }
  return 'localhost';
}

// MIME types
const mimeTypes = {
  '.html': 'text/html',
  '.js': 'application/javascript',
  '.css': 'text/css',
  '.json': 'application/json',
  '.png': 'image/png',
  '.jpg': 'image/jpeg',
  '.jpeg': 'image/jpeg',
  '.gif': 'image/gif',
  '.svg': 'image/svg+xml',
  '.ico': 'image/x-icon'
};

const server = http.createServer((req, res) => {
  let filePath = path.join(WEB_DIR, req.url === '/' ? 'index.html' : req.url);
  
  // Seguridad: prevenir acceso fuera del directorio web
  if (!filePath.startsWith(WEB_DIR)) {
    res.writeHead(403);
    res.end('Forbidden');
    return;
  }

  const ext = path.extname(filePath).toLowerCase();
  const contentType = mimeTypes[ext] || 'application/octet-stream';

  fs.readFile(filePath, (err, content) => {
    if (err) {
      if (err.code === 'ENOENT') {
        res.writeHead(404);
        res.end('File not found');
      } else {
        res.writeHead(500);
        res.end(`Server error: ${err.code}`);
      }
    } else {
      res.writeHead(200, {
        'Content-Type': contentType,
        'Access-Control-Allow-Origin': '*'
      });
      res.end(content);
    }
  });
});

const localIP = getLocalIP();

console.log('='.repeat(60));
console.log('Servidor web para Callos Annotation Tool');
console.log('='.repeat(60));
console.log(`\n[INFO] Directorio web: ${WEB_DIR}`);
console.log(`[INFO] Servidor iniciado en:`);
console.log(`       - Local:    http://localhost:${PORT}`);
console.log(`       - Red:      http://${localIP}:${PORT}`);
console.log(`\n[INFO] Para detener el servidor, presiona Ctrl+C`);
console.log('='.repeat(60));

server.listen(PORT, () => {
  // Servidor iniciado
});
