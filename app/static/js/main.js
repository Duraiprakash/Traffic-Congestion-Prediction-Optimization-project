/**
 * Traffic Congestion Prediction & Optimization - Main JavaScript
 * MCA Final Year Project
 */

// Global variables
let currentUser = null;
let refreshIntervals = {};

// Initialize application
document.addEventListener('DOMContentLoaded', function() {
    initializeApp();
    setupEventListeners();
    startAutoRefresh();
});

/**
 * Initialize the application
 */
function initializeApp() {
    console.log('🚦 Traffic Congestion Prediction System initialized');
    
    // Check if user is authenticated (for future implementation)
    checkAuthentication();
    
    // Initialize tooltips
    initializeTooltips();
    
    // Initialize charts if on dashboard
    if (document.getElementById('trafficTrendsChart')) {
        initializeDashboardCharts();
    }
    
    // Initialize maps if present
    if (document.getElementById('map') || document.getElementById('routeMap')) {
        initializeMaps();
    }
}

/**
 * Setup event listeners
 */
function setupEventListeners() {
    // Navigation active state
    const navLinks = document.querySelectorAll('.nav-link');
    navLinks.forEach(link => {
        link.addEventListener('click', function() {
            navLinks.forEach(l => l.classList.remove('active'));
            this.classList.add('active');
        });
    });
    
    // Form validation
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            if (!validateForm(this)) {
                e.preventDefault();
            }
        });
    });
    
    // Auto-save form data
    const formInputs = document.querySelectorAll('input, select, textarea');
    formInputs.forEach(input => {
        input.addEventListener('change', function() {
            saveFormData(this);
        });
    });
}

/**
 * Initialize tooltips
 */
function initializeTooltips() {
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
}

/**
 * Initialize dashboard charts
 */
function initializeDashboardCharts() {
    // This will be implemented by individual page scripts
    console.log('Dashboard charts initialized');
}

/**
 * Initialize maps
 */
function initializeMaps() {
    // This will be implemented by individual page scripts
    console.log('Maps initialized');
}

/**
 * Start auto-refresh for real-time data
 */
function startAutoRefresh() {
    // Refresh dashboard data every 30 seconds
    if (window.location.pathname === '/' || window.location.pathname === '/dashboard') {
        refreshIntervals.dashboard = setInterval(refreshDashboardData, 30000);
    }
    
    // Refresh map data every 30 seconds
    if (window.location.pathname.includes('/map')) {
        refreshIntervals.map = setInterval(refreshMapData, 30000);
    }
    
    // Refresh alerts every 60 seconds
    if (window.location.pathname.includes('/alerts')) {
        refreshIntervals.alerts = setInterval(refreshAlerts, 60000);
    }
}

/**
 * Stop auto-refresh
 */
function stopAutoRefresh() {
    Object.values(refreshIntervals).forEach(interval => {
        clearInterval(interval);
    });
    refreshIntervals = {};
}

/**
 * Check user authentication
 */
function checkAuthentication() {
    // For now, assume user is always authenticated
    // In a real implementation, this would check JWT tokens or session
    currentUser = {
        id: 1,
        email: 'user@example.com',
        name: 'Demo User'
    };
    
    console.log('User authenticated:', currentUser);
}

/**
 * Validate form data
 */
function validateForm(form) {
    const requiredFields = form.querySelectorAll('[required]');
    let isValid = true;
    
    requiredFields.forEach(field => {
        if (!field.value.trim()) {
            showFieldError(field, 'This field is required');
            isValid = false;
        } else {
            clearFieldError(field);
        }
    });
    
    // Email validation
    const emailFields = form.querySelectorAll('input[type="email"]');
    emailFields.forEach(field => {
        if (field.value && !isValidEmail(field.value)) {
            showFieldError(field, 'Please enter a valid email address');
            isValid = false;
        }
    });
    
    return isValid;
}

/**
 * Show field error
 */
function showFieldError(field, message) {
    clearFieldError(field);
    
    field.classList.add('is-invalid');
    const errorDiv = document.createElement('div');
    errorDiv.className = 'invalid-feedback';
    errorDiv.textContent = message;
    field.parentNode.appendChild(errorDiv);
}

/**
 * Clear field error
 */
function clearFieldError(field) {
    field.classList.remove('is-invalid');
    const errorDiv = field.parentNode.querySelector('.invalid-feedback');
    if (errorDiv) {
        errorDiv.remove();
    }
}

/**
 * Validate email format
 */
function isValidEmail(email) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
}

/**
 * Save form data to localStorage
 */
function saveFormData(input) {
    const form = input.closest('form');
    if (form) {
        const formData = new FormData(form);
        const data = Object.fromEntries(formData);
        localStorage.setItem(`form_${form.id || 'default'}`, JSON.stringify(data));
    }
}

/**
 * Load saved form data
 */
function loadFormData(formId) {
    const savedData = localStorage.getItem(`form_${formId}`);
    if (savedData) {
        const data = JSON.parse(savedData);
        Object.entries(data).forEach(([key, value]) => {
            const field = document.querySelector(`[name="${key}"]`);
            if (field) {
                field.value = value;
            }
        });
    }
}

/**
 * Show notification
 */
function showNotification(message, type = 'info', duration = 3000) {
    const notification = document.createElement('div');
    notification.className = `alert alert-${type} alert-dismissible fade show position-fixed`;
    notification.style.cssText = 'top: 20px; right: 20px; z-index: 9999; min-width: 300px;';
    notification.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    document.body.appendChild(notification);
    
    // Auto-remove after duration
    setTimeout(() => {
        if (notification.parentNode) {
            notification.remove();
        }
    }, duration);
}

/**
 * Show loading spinner
 */
function showLoading(element = null) {
    const target = element || document.body;
    const spinner = document.createElement('div');
    spinner.id = 'loadingSpinner';
    spinner.className = 'position-fixed top-0 start-0 w-100 h-100 d-flex justify-content-center align-items-center';
    spinner.style.cssText = 'background: rgba(0,0,0,0.5); z-index: 9999;';
    spinner.innerHTML = `
        <div class="spinner-border text-light" role="status">
            <span class="visually-hidden">Loading...</span>
        </div>
    `;
    
    target.appendChild(spinner);
}

/**
 * Hide loading spinner
 */
function hideLoading() {
    const spinner = document.getElementById('loadingSpinner');
    if (spinner) {
        spinner.remove();
    }
}

/**
 * Format date for display
 */
function formatDate(date, includeTime = true) {
    const d = new Date(date);
    const options = {
        year: 'numeric',
        month: 'short',
        day: 'numeric'
    };
    
    if (includeTime) {
        options.hour = '2-digit';
        options.minute = '2-digit';
    }
    
    return d.toLocaleDateString('en-US', options);
}

/**
 * Format number with commas
 */
function formatNumber(num) {
    return num.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ',');
}

/**
 * Get congestion color class
 */
function getCongestionColor(level) {
    switch(level.toLowerCase()) {
        case 'low': return 'success';
        case 'medium': return 'warning';
        case 'high': return 'danger';
        default: return 'secondary';
    }
}

/**
 * Get severity color class
 */
function getSeverityColor(severity) {
    switch(severity.toLowerCase()) {
        case 'critical': return 'danger';
        case 'high': return 'warning';
        case 'medium': return 'info';
        case 'low': return 'success';
        default: return 'secondary';
    }
}

/**
 * Debounce function
 */
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

/**
 * Throttle function
 */
function throttle(func, limit) {
    let inThrottle;
    return function() {
        const args = arguments;
        const context = this;
        if (!inThrottle) {
            func.apply(context, args);
            inThrottle = true;
            setTimeout(() => inThrottle = false, limit);
        }
    };
}

/**
 * API request helper
 */
async function apiRequest(url, options = {}) {
    const defaultOptions = {
        headers: {
            'Content-Type': 'application/json',
        },
    };
    
    const config = { ...defaultOptions, ...options };
    
    try {
        const response = await fetch(url, config);
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        return await response.json();
    } catch (error) {
        console.error('API request failed:', error);
        showNotification('Request failed. Please try again.', 'danger');
        throw error;
    }
}

/**
 * Refresh dashboard data
 */
async function refreshDashboardData() {
    try {
        const data = await apiRequest('/api/dashboard-data');
        console.log('Dashboard data refreshed:', data);
        
        // Trigger custom event for components to update
        window.dispatchEvent(new CustomEvent('dashboardDataUpdated', { detail: data }));
    } catch (error) {
        console.error('Failed to refresh dashboard data:', error);
    }
}

/**
 * Refresh map data
 */
async function refreshMapData() {
    try {
        const data = await apiRequest('/api/heatmap-data');
        console.log('Map data refreshed:', data);
        
        // Trigger custom event for map components to update
        window.dispatchEvent(new CustomEvent('mapDataUpdated', { detail: data }));
    } catch (error) {
        console.error('Failed to refresh map data:', error);
    }
}

/**
 * Refresh alerts
 */
async function refreshAlerts() {
    try {
        // This would typically fetch from an alerts API
        console.log('Alerts refreshed');
        
        // Trigger custom event for alert components to update
        window.dispatchEvent(new CustomEvent('alertsUpdated'));
    } catch (error) {
        console.error('Failed to refresh alerts:', error);
    }
}

/**
 * Export data to CSV
 */
function exportToCSV(data, filename = 'export.csv') {
    if (!data || data.length === 0) {
        showNotification('No data to export', 'warning');
        return;
    }
    
    const headers = Object.keys(data[0]);
    const csvContent = [
        headers.join(','),
        ...data.map(row => headers.map(header => `"${row[header] || ''}"`).join(','))
    ].join('\n');
    
    const blob = new Blob([csvContent], { type: 'text/csv' });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = filename;
    a.click();
    window.URL.revokeObjectURL(url);
}

/**
 * Print current page
 */
function printPage() {
    window.print();
}

/**
 * Handle page visibility change
 */
document.addEventListener('visibilitychange', function() {
    if (document.hidden) {
        // Page is hidden, pause auto-refresh
        stopAutoRefresh();
    } else {
        // Page is visible, resume auto-refresh
        startAutoRefresh();
    }
});

/**
 * Handle page unload
 */
window.addEventListener('beforeunload', function() {
    stopAutoRefresh();
});

// Export functions for global use
window.TrafficApp = {
    showNotification,
    showLoading,
    hideLoading,
    formatDate,
    formatNumber,
    getCongestionColor,
    getSeverityColor,
    apiRequest,
    exportToCSV,
    printPage
};
