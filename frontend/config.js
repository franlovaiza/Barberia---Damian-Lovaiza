//export const API_URL='http://localhost:8000'

// config.js
const isLocal = window.location.hostname === 'localhost' || 
                window.location.hostname === '127.0.0.1';

export const API_URL = isLocal 
    ? 'http://localhost:8000' 
    : 'https://barberia-lovaiza.onrender.com';  