

import 'jquery-validation';

const PyAMS_form = {

	init: (forms) => {

		$('label', forms).removeClass('col-md-3');
		$('.col-md-9', forms).removeClass('col-md-9');
		$('input, select, textarea', forms).addClass('form-control');
		$('button', forms).addClass('border');
		$('button[type="submit"]', forms).addClass('btn-primary');

		const lang = $('html').attr('lang');
		const defaultOptions = {
			submitHandler: PyAMS_form.submitHandler,
			messages: {}
		};

		const getFormOptions = (form, options) => {
			$('[data-ams-validate-messages]', form).each((idx, elt) => {
				options.messages[$(elt).attr('name')] = $(elt).data('ams-validate-messages');
			});
			return options;
		};

		const validateForms = () => {
			$(forms).each((idx, form) => {
				const options = $.extend({}, defaultOptions);
				$(form).validate(getFormOptions(form, options));
			});
		}

		if (lang === 'fr') {
			import("jquery-validation/dist/localization/messages_fr").then(() => {
				validateForms();
			});
		} else {
			validateForms();
		}
	},


	submitHandler: (form) => {

		const doSubmit = (form) => {
			const
				button = $('button[type="submit"]', form),
				name = button.attr('name'),
				input = $('input[name="' + name + '"]', form);
			if (input.length === 0) {
				$('<input />')
					.attr('type', 'hidden')
					.attr('name', name)
					.attr('value', button.attr('value'))
					.appendTo(form);
			}
			form.submit();
		};

		if (window.grecaptcha) {  // check if recaptcha was loaded
			const captcha_key = $(form).data('ams-form-captcha-key');
			grecaptcha.execute(captcha_key, {
				action: 'form_submit'
			}).then((token) => {
				$('.state-error', form).removeClass('state-error');
				$('input[name="g-recaptcha-response"]', form).val(token);
				doSubmit(form);
			});
		} else {
			doSubmit(form);
		}
	}

};


export default PyAMS_form;
