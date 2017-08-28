(function($) {
    // nav dropdown
    $('#nav-profile').dropdown();

    // apps dropdown
    $('#nav-apps').dropdown();

    // events modal
    $('#event-link').on('click', function() {
        $('#event-modal .header').text('Testing...');
        $('#event-modal').modal('show');
    });

    // board members
    var members = 14;
    for (var i = 0; i <= members; i++) {
        var prof_id = '#prof-' + i;

        $(prof_id).on('mouseover', function() {
            var img = $(this).find('img');
            img.css('cursor', 'pointer');
            img.css('-webkit-filter', 'grayscale(0%)');
            img.css('filter', 'grayscale(0%)');
        });

        $(prof_id).on('mouseleave', function() {
            var img = $(this).find('img');
            img.css('cursor', 'auto');
            img.css('-webkit-filter', 'grayscale(100%)');
            img.css('filter', 'grayscale(100%)');
        });

        $(prof_id).on('click', function() {
            var id = this.id.split('-')[1];
            var modal_id = '#modal-' + id;
            $(modal_id).modal('show');
        });
    }

    // follow/unfollow buttons
    $('.follow').on('click', function() {
        var mode = $(this).text();
        var user_id = $(this).attr('user');
        var api_url = '/api/v1/users/';
        var new_text = '';
        var self = this;

        if (mode == 'Follow') {
            api_url += 'follow/';
            new_text = 'Unfollow';
        } else {
            api_url += 'unfollow/';
            new_text = 'Follow';
        }

        $.ajax({
            url: api_url,
            method: 'POST',
            data: {
                'user_id': user_id
            },
            success: function(data) {
                if (data['success']) {
                    var classes = $(self).attr('class');

                    if (classes.indexOf('red') != -1) {
                        classes = classes.replace('red', 'green');
                    } else {
                        classes = classes.replace('green', 'red');
                    }

                    $(self).attr('class', classes);
                    $(self).text(new_text);
                }
            }
        })
    });

})(jQuery);
