// Evento cuando se envía el formulario de inicio de sesión
document.getElementById('login-form').addEventListener('submit', function(event) {
    event.preventDefault(); // Evita el envío del formulario por defecto
    
    // Obtiene los valores del formulario
    var email = document.getElementById('email').value;
    var password = document.getElementById('password').value;
    
    // Realiza una petición AJAX para enviar los datos al servidor
    var xhr = new XMLHttpRequest();
    xhr.open('POST', '/login', true);
    xhr.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');
    xhr.onreadystatechange = function() {
        if (xhr.readyState === 4 && xhr.status === 200) {
            // Redirige a la página de perfil si el inicio de sesión fue exitoso
            window.location.href = '/profile';
        } else if (xhr.readyState === 4) {
            // Muestra un mensaje de error si el inicio de sesión falló
            var errorElement = document.getElementById('error');
            errorElement.innerHTML = 'Credenciales incorrectas. Inténtalo de nuevo.';
            errorElement.style.display = 'block';
        }
    };
    xhr.send('email=' + encodeURIComponent(email) + '&password=' + encodeURIComponent(password));
});

// Evento cuando se envía el formulario de registro
document.getElementById('register-form').addEventListener('submit', function(event) {
    event.preventDefault(); // Evita el envío del formulario por defecto
    
    // Obtiene los valores del formulario
    var email = document.getElementById('email').value;
    var password = document.getElementById('password').value;
    
    // Realiza una petición AJAX para enviar los datos al servidor
    var xhr = new XMLHttpRequest();
    xhr.open('POST', '/register', true);
    xhr.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');
    xhr.onreadystatechange = function() {
        if (xhr.readyState === 4 && xhr.status === 200) {
            // Redirige a la página de inicio de sesión si el registro fue exitoso
            window.location.href = '/login';
        } else if (xhr.readyState === 4) {
            // Muestra un mensaje de error si el registro falló
            var errorElement = document.getElementById('error');
            errorElement.innerHTML = 'Error en el registro. Inténtalo de nuevo.';
            errorElement.style.display = 'block';
        }
    };
    xhr.send('email=' + encodeURIComponent(email) + '&password=' + encodeURIComponent(password));
});
