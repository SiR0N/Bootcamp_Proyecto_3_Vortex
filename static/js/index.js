/**
 * VORTEX - Weather Dashboard
 */

const API_BASE = "/api/clima";
const DEFAULT_LOCATION = { lat: 40.4167, lon: -3.7033, nombre: "Madrid" };

function validarRespuestaAPI(data) {
    const camposRequeridos = ['temperatura', 'humedad', 'ciudad'];
    for (const campo of camposRequeridos) {
        if (!(campo in data) || data[campo] === null || data[campo] === undefined) {
            return false;
        }
    }
    return true;
}

async function fetchConFallback(location) {
    const url = API_BASE + '?lat=' + location.lat + '&lon=' + location.lon;
    try {
        const response = await fetch(url);
        if (!response.ok) throw new Error('HTTP ' + response.status);
        const data = await response.json();
        if (!validarRespuestaAPI(data)) throw new Error('Datos incompletos');
        return { success: true, data: data, location: location };
    } catch (error) {
        return { success: false, error: error.message, location: location };
    }
}

function mostrarDatos(data, esFallback) {
    // Determinar fuente real (no por si usó fallback)
    var fuenteReal = data.fuente || 'AEMET';
    
    // Hero card
    document.getElementById('cityName').textContent = data.ciudad || 'Ubicación Detectada';
    document.getElementById('stationName').textContent = data.estacion || 'Estación AEMET';
    document.getElementById('temperature').textContent = Math.round(data.temperatura) + '°';
    
    // Weather details
    document.getElementById('humidity').textContent = data.humedad + '%';
    document.getElementById('wind').textContent = data.viento + ' km/h';
    document.getElementById('rain').textContent = data.lluvia + ' mm';
    
    // Metrics card - Fuente real de los datos
    document.getElementById('humidity2').textContent = data.humedad + '%';
    document.getElementById('wind2').textContent = data.viento + ' km/h';
    document.getElementById('rain2').textContent = data.lluvia + ' mm';
    document.getElementById('source').textContent = fuenteReal.toUpperCase();
    
    // Info del sistema
    document.getElementById('stationInfo').textContent = data.estacion || data.ciudad || 'N/A';
    document.getElementById('coordsInfo').textContent = (data.lat ? data.lat.toFixed(4) : '--') + ', ' + (data.lon ? data.lon.toFixed(4) : '--');
    
    var hora = new Date().toLocaleTimeString('es-ES', { hour: '2-digit', minute: '2-digit' });
    document.getElementById('timeInfo').textContent = hora;
    
    // Solo mostrar "fallback" si la fuente real es fallback
    if (fuenteReal === 'fallback') {
        document.getElementById('updatedAt').textContent = 'Modo backup (' + hora + ')';
        document.getElementById('statusInfo').textContent = 'Datos backup';
    } else {
        document.getElementById('updatedAt').textContent = 'Última actualización: ' + hora;
        document.getElementById('statusInfo').textContent = 'Conexión OK';
        document.getElementById('statusInfo').style.color = '';
    }
    
    // Map card
    var mapCity = document.getElementById('mapCity');
    var openMaps = document.getElementById('openMaps');
    if (mapCity) mapCity.textContent = data.ciudad || 'Ubicación detectada';
    if (openMaps && data.lat && data.lon) {
        openMaps.href = 'https://www.google.com/maps?q=' + data.lat + ',' + data.lon;
        openMaps.style.display = 'inline-block';
    }
}

function mostrarError(mensaje) {
    document.getElementById('temperature').textContent = '--°';
    document.getElementById('humidity').textContent = '--%';
    document.getElementById('wind').textContent = '-- km/h';
    document.getElementById('rain').textContent = '-- mm';
    document.getElementById('statusInfo').textContent = 'Sin conexión';
    document.getElementById('mapCity').textContent = 'Sin ubicación';
    document.getElementById('openMaps').style.display = 'none';
}

function btnReset() {
    var btn = document.getElementById('refreshBtn');
    if (btn) {
        btn.disabled = false;
        btn.innerHTML = 'Actualizar Datos';
    }
}

async function actualizarClima() {
    var btn = document.getElementById('refreshBtn');
    var spinner = btn ? btn.querySelector('.spinner') : null;
    
    if (btn) {
        btn.disabled = true;
        if (spinner) spinner.style.display = 'inline-block';
        btn.innerHTML = '<span class="spinner"></span> Actualizando...';
    }

    if (!navigator.geolocation) {
        var result = await fetchConFallback(DEFAULT_LOCATION);
        if (result.success) {
            mostrarDatos(result.data, false);
        } else {
            mostrarError('Sin datos disponibles');
        }
        btnReset();
        return;
    }

    try {
        var position = await new Promise(function(resolve, reject) {
            navigator.geolocation.getCurrentPosition(resolve, reject, { timeout: 5000 });
        });
        
        var lat = position.coords.latitude;
        var lon = position.coords.longitude;
        var result = await fetchConFallback({ lat: lat, lon: lon, nombre: 'GPS' });

        if (result.success) {
            mostrarDatos(result.data, false);
        } else {
            var fbResult = await fetchConFallback(DEFAULT_LOCATION);
            if (fbResult.success) {
                mostrarDatos(fbResult.data, true);
            } else {
                mostrarError('Sin conexión');
            }
        }
    } catch (error) {
        var fbResult = await fetchConFallback(DEFAULT_LOCATION);
        if (fbResult.success) {
            mostrarDatos(fbResult.data, true);
        } else {
            mostrarError('Sin conexión');
        }
    }

    btnReset();
}

document.addEventListener('DOMContentLoaded', function() {
    actualizarClima();
    
    var refreshBtn = document.getElementById('refreshBtn');
    if (refreshBtn) {
        refreshBtn.addEventListener('click', actualizarClima);
    }
});