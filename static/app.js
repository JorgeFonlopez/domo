document.addEventListener("DOMContentLoaded", function () {
    obtenerTareas(); // Cargar tareas al cargar la página

    // Agregar evento de envío al formulario para crear una nueva tarea
    document.getElementById("form-tarea").addEventListener("submit", function (event) {
        event.preventDefault(); // Evitar el comportamiento predeterminado del formulario

        // Obtener la descripción de la tarea del input
        const descripcion = document.getElementById("descripcion").value;

        // Verificar si la descripción no está vacía
        if (descripcion.trim() !== "") {
            // Crear un objeto con los datos de la nueva tarea
            const nuevaTarea = {
                descripcion: descripcion
            };

            // Realizar una solicitud POST para crear una nueva tarea
            fetch("/tareas", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify(nuevaTarea)
            })
            .then(response => response.json())
            .then(data => {
                console.log(data); // Log de la respuesta del servidor
                obtenerTareas(); // Volver a cargar la lista de tareas actualizada
            })
            .catch(error => console.error("Error al agregar la tarea:", error));
        } else {
            alert("Por favor, ingresa una descripción para la tarea.");
        }
    });
});

// Función para obtener y mostrar todas las tareas
function obtenerTareas() {
    fetch("/tareas")
    .then(response => response.json())
    .then(tareas => {
        const listaTareas = document.getElementById("lista-tareas");
        listaTareas.innerHTML = ""; // Limpiar la lista antes de agregar las nuevas tareas
        tareas.forEach(tarea => {
            const li = document.createElement("li");
            li.textContent = `${tarea.id}: ${tarea.descripcion}`;
            listaTareas.appendChild(li);
        });
    })
    .catch(error => console.error("Error al obtener las tareas:", error));
}
