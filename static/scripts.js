


// Este script es de la pestaña de inicio
        
    // El elemento del enlace
    var scrollLink = document.querySelector('.scroll-link');
    
    // Evento de clic al enlace
    scrollLink.addEventListener('click', function(event) {
      event.preventDefault(); // Evita el comportamiento predeterminado del enlace
      
      // Obtén la posición de desplazamiento actual
      var currentPosition = window.pageYOffset || document.documentElement.scrollTop || document.body.scrollTop;
      
      // Define la posición objetivo a la que deseas desplazarte (en este caso, el principio de la página)
      var targetPosition = 0;
      
      // Calcula la distancia que se debe desplazar
      var distance = targetPosition - currentPosition;
      
      // Duración de la animación en milisegundos
      var duration = 50000;
      
      // Realiza la animación de desplazamiento suave
      scrollToTarget(distance, duration);
    });
    
    // Función para realizar la animación de desplazamiento suave
    function scrollToTarget(distance, duration) {
      var start = window.pageYOffset || document.documentElement.scrollTop || document.body.scrollTop;
      var currentTime = 10;
      var increment = 20;
    
      // Función de animación
      var animateScroll = function() {
        currentTime += increment;
        var easing = easeInOutQuad(currentTime, start, distance, duration);
        window.scrollTo(0, easing);
        if (currentTime < duration) {
          requestAnimationFrame(animateScroll);
        }
      };
      
      // Función de interpolación para obtener un desplazamiento suave
      var easeInOutQuad = function(t, b, c, d) {
        t /= d / 2;
        if (t < 1) return c / 2 * t * t + b;
        t--;
        return -c / 2 * (t * (t - 2) - 1) + b;
      };
    
      animateScroll();
    }
    

    // Hasta aquí llega el Srcipt de la pestaña de inicio


    
// Este es el Script del Navbar


function scrollToTop() {
    window.scrollTo({
        top: 0,
        behavior: "smooth"
    });
}

function viewUserProfile() {
    // Lógica para ver el perfil del usuario
    // Aquí puedes redirigir a la página del perfil del usuario o mostrar un modal con la información
}

function logout() {
    // Lógica para cerrar sesión
    // Aquí puedes redirigir a la página de inicio de sesión o realizar otras acciones necesarias
}

// Hasta aquí llega el Script del Navbar


    // Este es el JS del chat
    
        function openChat() {
            var chatContainer = document.getElementById("chatContainer");
            chatContainer.style.display = "block";
        }

        function closeChat() {
            var chatContainer = document.getElementById("chatContainer");
            chatContainer.style.display = "none";
        }

        function sendMessage(event) {
            var messageInput = document.getElementById("messageInput");
            var message = messageInput.value;

            if (message !== "") {
                var chatBody = document.getElementById("chatBody");
                var newMessage = document.createElement("div");
                newMessage.className = "chat-message sent"; // Agregar la clase "sent" al mensaje enviado
                var messageText = document.createElement("p");
                messageText.textContent = message;
                newMessage.appendChild(messageText);
                chatBody.appendChild(newMessage);
                messageInput.value = "";

                // Respuesta automática
                setTimeout(function() {
                    var response = "Gracias por tu mensaje. Nos pondremos en contacto contigo pronto.";
                    var responseMessage = document.createElement("div");
                    responseMessage.className = "chat-message";
                    var responseText = document.createElement("p");
                    responseText.textContent = response;
                    responseMessage.appendChild(responseText);
                    chatBody.appendChild(responseMessage);
                }, 1000);
            }

            // Evitar el envío del formulario al presionar Enter
            event.preventDefault();
        }

    
    // Final del JS del chat

    







