$('.js-vote').click(function(ev) {
    ev.preventDefault();
    var $this = $(this),
        action=$this.data('action'),
        qid=$this.data('qid');
    $.ajax('/qvote/', {
        method: 'POST',
        data: {
            action: action,
            qid: qid
        }
    }).done(function(data) {
        console.log(data['error']);
        if (data['error'] == "") {
             $('.q-' + qid).html(data['rating']);
        } else {
            alert('Action not permitted')
        }
        $('.js-' + qid).hide();
    }
    );
});

$('.js-vote-ans').click(function(ev) {
    ev.preventDefault();
    var $this = $(this),
        action=$this.data('action'),
        aid=$this.data('aid');
    $.ajax('/avote/', {
        method: 'POST',
        data: {
            action: action,
            aid: aid
        }
    }).done(function(data) {
        console.log(data['error']);
        if (data['error'] == "") {
             $('.ans-' + aid).html(parseInt($('.ans-' + aid).html()) + parseInt(data['rating']));
        } else {
            alert('Action not permitted')
        }
        $('.js-ans-' + aid).hide();
    }
    );
});