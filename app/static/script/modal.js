$(document).ready(function () {
    // example: https://getbootstrap.com/docs/4.2/components/modal/
    // show modal
    $('#state-modal').on('show.bs.modal', function (event) {
        const button = $(event.relatedTarget) // Button that triggered the modal
        const taskID = button.data('source') // Extract info from data-* attributes
        const content = button.data('content') // Extract info from data-* attributes

        const modal = $(this)
        if (taskID === 'New State') {
            modal.find('.modal-title').text(taskID)
            $('#task-form-display').removeAttr('taskID')
        } else {
            modal.find('.modal-title').text('Edit State ' + taskID)
            $('#task-form-display').attr('taskID', taskID)
        }

        if (content) {
            modal.find('.form-control').val(content);
        } else {
            modal.find('.form-control').val('');
        }
    })


    $('#submit-state').click(function () {
        const tID = $('#task-form-display').attr('taskID');
        console.log($('#state-modal').find('.form-control').val())
        $.ajax({
            type: 'POST',
            url: tID ? '/edit/' + tID : '/create',
            contentType: 'application/json;charset=UTF-8',
            data: JSON.stringify({
                'Safety_Index': $('#state-modal').find('.form-control').val()
            }),
            success: function (res) {
                console.log(res.response)
                location.reload();
            },
            error: function () {
                console.log('Error');
            }
        });
    });

    $('.remove').click(function () {
        const remove = $(this)
        $.ajax({
            type: 'POST',
            url: '/delete/' + remove.data('source'),
            success: function (res) {
                console.log(res.response)
                location.reload();
            },
            error: function () {
                console.log('Error');
            }
        });
    });

});