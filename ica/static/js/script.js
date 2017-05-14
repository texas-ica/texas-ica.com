jQuery(document).ready(function($) {
    // nav dropdown
    $('#nav-profile').dropdown();

    // board members
    var members = 14;
    for (var i = 0; i <= members; i++) {
        var prof_id = '#prof-' + i;
        $(prof_id).on('click', function() {
            var id = this.id.split('-')[1];
            var modal_id = '#modal-' + id;
            $(modal_id).modal('show');
        });
    }
});
