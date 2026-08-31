// Configuration file for API endpoints and app settings
const APP_CONFIG = {
    // Backend API URL
    // Options:
    // - 'http://127.0.0.1:8000' for local development
    // - 'http://10.0.2.2:8000' for Android emulator
    // - 'http://YOUR_COMPUTER_IP:8000' for physical device on same network
    // - 'https://your-deployed-backend.com' for production
    API_BASE: 'http://192.168.1.100:8000',
    
    // App settings
    APP_NAME: 'Garden Mystery',
    APP_VERSION: '1.0.0'
};

// Export for use in other files
if (typeof module !== 'undefined' && module.exports) {
    module.exports = APP_CONFIG;
}
