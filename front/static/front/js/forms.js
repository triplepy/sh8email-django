var forms = forms || {};

forms.submitForms = function() {
    $('.js-forms-submitform').submit();
};

forms.attachSubmitEvents = function() {
    $('.js-forms-submitbutton').click(forms.submitForms);
};


$(function() {
    forms.attachSubmitEvents();
});