$(document).ready(function() {
    $('#task-form').submit(function(event) {
        event.preventDefault();
        var task = $('#task').val();
        $.post('/add_task', {task: task}, function(data) {
            alert(data.message);
            location.reload(); 
        });
    });

    $('.delete-btn').click(function() {
        var index = $(this).parent().index(); 
        $.post('/delete_task', {index: index}, function(data) {
            alert(data.message);
            location.reload(); 
        });
    });
});
