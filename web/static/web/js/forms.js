var forms = forms || {};

forms.attachSubmitEvents = function() {
    $('.js-forms-submitbutton').click(function(event) {
        $(event.target).parents('.js-forms-submitform').submit();
    });
};


$(function() {
    forms.attachSubmitEvents();
});