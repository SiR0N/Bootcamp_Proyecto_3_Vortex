/**
 * ClimApp - Fallback GPS Robusto
 * ==============================
 * Fallback automático con múltiples ubicaciones de respaldo
 * Validación de respuesta y reintentos automáticos
 */

// Ubicaciones de fallback (ordenadas por prioridad)
const FALLBACK_LOCATIONS = [
    { lat: 40.4167, lon: -3.7033, nombre: "Madrid-Centro" },
    { lat: 40.4530, lon: -3.6883, nombre: "Madrid-Retiro" },
    { lat: 40.4167, lon: -3.7033, nombre: "Alcala de Henares" },
    { lat: 40.4329, lon: -3.6167, nombre: "Tres Cantos" }
];

const FALLBACK_MAX_RETRIES = 3;

/**
 * Valida que la respuesta de la API tenga datos válidos
 */
function validarRespuestaAPI(data) {
    // Verificar que tiene las propiedades mínimas necesarias
    const camposRequeridos = ['temperatura', 'humedad', 'ciudad'];
    for (const campo of camposRequeridos) {
        if (!(campo in data) || data[campo] === null || data[campo] === undefined) {
            console.warn(`Campo obligatorio '${campo}' faltante o inválido`);
            return false;
        }
    }

    // Validar rangos razonables
    const temp = parseFloat(data.temperatura);
    if (isNaN(temp) || temp < -50 || temp > 60) {
        console.warn(`Temperatura fuera de rango válido: ${temp}`);
        return false;
    }

    const humedad = parseInt(data.humedad);
    if (isNaN(humedad) || humedad < 0 || humedad > 100) {
        console.warn(`Humedad fuera de rango válido: ${humedad}`);
        return false;
    }

    return true;
}

/**
 * Obtiene datos climáticos con reintentos automáticos
 */
async function fetchConFallback(location, intentos = 1) {
    const url = `/api/clima?lat=${location.lat}&lon=${location.lon}`;
    console.log(`[Fallback] Intento ${intentos}/${FALLBACK_MAX_RETRIES} - ${location.nombre}`);

    try {
        const response = await fetch(url);

        if (!response.ok) {
            throw new Error(`HTTP ${response.status}`);
        }

        const data = await response.json();

        // Validar que la respuesta tiene datos válidos
        if (!validarRespuestaAPI(data)) {
            throw new Error("Respuesta inválida - datos incompletos");
        }

        return { success: true, data, location };

    } catch (error) {
        console.warn(`[Fallback] Error en ${location.nombre}:`, error.message);

        // Si quedan intentos, probar siguiente ubicación
        if (intentos < FALLBACK_MAX_RETRIES) {
            const siguienteIdx = FALLBACK_LOCATIONS.indexOf(location) + 1;
            if (siguienteIdx < FALLBACK_LOCATIONS.length) {
                return fetchConFallback(FALLBACK_LOCATIONS[siguienteIdx], intentos + 1);
            }
        }

        return { success: false, error: error.message };
    }
}

/**
 * Muestra los datos en la interfaz
 */
function mostrarDatos(data, location, esFallback = false) {
    const temperature = document.getElementById("temperature");
    const humidity = document.getElementById("humidity");
    const wind = document.getElementById("wind");
    const rain = document.getElementById("rain");
    const stationName = document.getElementById("stationName");
    const cityName = document.getElementById("cityName");
    const mainTitle = document.getElementById("mainTitle");
    const updatedAt = document.getElementById("updatedAt");
    const statusDot = document.getElementById("statusDot");

    // Rellenar datos
    temperature.textContent = `${Math.round(data.temperatura)}°`;
    humidity.textContent = `${data.humedad}%`;
    wind.textContent = `${data.viento} km/h`;
    rain.textContent = `${data.lluvia} mm`;
    stationName.textContent = data.estacion;
    cityName.textContent = data.ciudad;
    mainTitle.textContent = `${data.ciudad} · Tiempo Real`;

    // Hora local
    const horaActual = new Date().toLocaleTimeString("es-ES", {
        hour: "2-digit",
        minute: "2-digit"
    });

    // Mensaje según si es fallback o no
    if (esFallback) {
        updatedAt.textContent = `Fallback: ${location.nombre} (${horaActual})`;
        statusDot.style.background = "#f59e0b";  // Naranja
        statusDot.style.boxShadow = "0 0 12px rgba(245, 158, 11, 0.45)";
    } else {
        updatedAt.textContent = `Última actualización: ${horaActual}`;
        statusDot.style.background = "#22c55e";  // Verde
        statusDot.style.boxShadow = "0 0 12px rgba(34, 197, 94, 0.45)";
    }

    // Icono
    actualizarIconoVisual(data);
}

/**
 * Muestra error en la interfaz
 */
function mostrarError(mensaje) {
    const updatedAt = document.getElementById("updatedAt");
    const statusDot = document.getElementById("statusDot");

    updatedAt.textContent = mensaje;
    statusDot.style.background = "#ef4444";  // Rojo
    statusDot.style.boxShadow = "0 0 12px rgba(239, 68, 68, 0.45)";
}

/**
 * Función principal actualizada
 */
async function actualizarClima() {
    if (!navigator.geolocation) {
        mostrarError("GPS no soportado");
        return;
    }

    console.log("[ClimApp] Iniciando...");

    // Opción 1: Intentar GPS primero
    try {
        const position = await new Promise((resolve, reject) => {
            navigator.geolocation.getCurrentPosition(
                resolve,
                reject,
                { timeout: 5000, enableHighAccuracy: false }
            );
        });

        const { latitude, longitude } = position.coords;
        console.log(`[GPS] Ubicación obtenida: ${latitude}, ${longitude}`);

        // Intentar con ubicación del GPS
        const result = await fetchConFallback({ lat: latitude, lon: longitude, nombre: "GPS" });

        if (result.success) {
            mostrarDatos(result.data, result.location, false);
            console.log("[ClimApp] ✅ Datos obtenidos por GPS");
        } else {
            // Si falla el GPS, probar fallbacks
            console.warn("[GPS] Respuesta inválida, probando fallbacks...");
            const fallbackResult = await fetchConFallback(FALLBACK_LOCATIONS[0]);

            if (fallbackResult.success) {
                mostrarDatos(fallbackResult.data, fallbackResult.location, true);
                console.log("[ClimApp] ✅ Fallback usado");
            } else {
                mostrarError("Error: Sin datos disponibles");
                console.error("[ClimApp] ❌ Todos los intentos fallidos");
            }
        }

    } catch (error) {
        // GPS falló - usar fallbacks automáticamente
        console.warn(`[GPS] Error: ${error.message}. Usando fallback...`);

        const fallbackResult = await fetchConFallback(FALLBACK_LOCATIONS[0]);

        if (fallbackResult.success) {
            mostrarDatos(fallbackResult.data, fallbackResult.location, true);
            console.log("[ClimApp] ✅ Fallback automático usado");
        } else {
            mostrarError("Error: Sin conexión");
            console.error("[ClimApp] ❌ Fallback también falló");
        }
    }
}

/**
 * Actualiza los elementos visuales del icono (Sol/Luna/Nubes/Lluvia)
 */
function actualizarIconoVisual(data) {
    const container = document.getElementById("weather-icon-container");
    const sun = document.getElementById("sun-icon");

    if (!container || !sun) return;

    // Limpiar iconos anteriores
    container.querySelectorAll('.cloud, .rain-drops').forEach(el => el.remove());

    // Resetear clases
    sun.className = "sun";

    // Noche o día
    if (data.es_noche) {
        sun.classList.add("is-night");
    }

    // Color por temperatura
    const temp = Math.round(data.temperatura);
    if (temp <= 12) {
        sun.classList.add("temp-cold");
    } else if (temp >= 28) {
        sun.classList.add("temp-hot");
    }

    // Nubes o lluvia
    if (data.lluvia > 0) {
        crearNube(container, true);
    } else if (data.humedad > 75) {
        crearNube(container, false);
    }
}

/**
 * Crea nube y lluvia opcional
 */
function crearNube(parent, conLluvia) {
    const cloud = document.createElement("div");
    cloud.className = "cloud";

    if (conLluvia) {
        const drops = document.createElement("div");
        drops.className = "rain-drops";

        for (let i = 0; i < 3; i++) {
            const d = document.createElement("div");
            d.className = "drop";
            d.style.left = (20 + i * 25) + "px";
            d.style.animationDelay = (i * 0.2) + "s";
            drops.appendChild(d);
        }

        cloud.appendChild(drops);
    }

    parent.appendChild(cloud);
}

// Inicio
document.addEventListener("DOMContentLoaded", () => {
    console.log("[ClimApp] Inicializado - Fallback GPS robusto activo");
    actualizarClima();

    const refreshBtn = document.getElementById("refreshBtn");
    if (refreshBtn) {
        refreshBtn.addEventListener("click", actualizarClima);
    }
});