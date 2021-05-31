$('.form-check-input').click(function(ev) {
    ev.preventDefault();
    var $this = $(this),
        aid=$this.data('aid');
    $.ajax('/check/', {
        method: 'POST',
        data: {
            aid: aid
        }
    }).done(function(data) {
        console.log(data['error']);
        if (data['error'] == "") {
            if (data['value']){
                $('.check-' + aid).prop('checked', true);
            } else {
                $('.check-' + aid).prop('checked', false);
            }
        }  else {
            alert('Action not permitted')
        }
    }
    );
});
