{
  "name": "nusashop-app",
  "version": "1.0.0",
  "description": "NusaShop E-Commerce Platform - LKS Cloud Computing 2026",
  "main": "server.js",
  "scripts": {
    "start":   "node server.js",
    "dev":     "nodemon server.js",
    "test":    "jest --coverage",
    "lint":    "eslint . --ext .js"
  },
  "dependencies": {
    "express": "^4.18.2"
  },
  "devDependencies": {
    "jest":       "^29.0.0",
    "supertest":  "^6.3.0",
    "nodemon":    "^3.0.0",
    "eslint":     "^8.0.0"
  },
  "engines": {
    "node": ">=20.0.0"
  }
}
