$(function () {
    $('.profile-entry').each(function (index) {
        var self = $(this);
        self.find('.btn-modify').on('click', function() {
            var inputDOM = self.find('input');
            inputDOM.removeAttr('disabled');
        
        });
    
    });
});
