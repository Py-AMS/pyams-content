"use strict";
(self["webpackChunkpyams_default_theme"] = self["webpackChunkpyams_default_theme"] || []).push([["src_pyams_content_skin_resources_src__form_js"],{

/***/ "./src/pyams_content/skin/resources/src/_form.js":
/*!*******************************************************!*\
  !*** ./src/pyams_content/skin/resources/src/_form.js ***!
  \*******************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var jquery_validation__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! jquery-validation */ "./node_modules/jquery-validation/dist/jquery.validate.js");
/* harmony import */ var jquery_validation__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(jquery_validation__WEBPACK_IMPORTED_MODULE_0__);
/* provided dependency */ var $ = __webpack_require__(/*! jquery */ "./node_modules/jquery/dist/jquery.js");

var PyAMS_form = {
  init: function init(forms) {
    $('label', forms).removeClass('col-md-3');
    $('.col-md-9', forms).removeClass('col-md-9');
    $('input, select, textarea', forms).addClass('form-control');
    $('button', forms).addClass('border');
    $('button[type="submit"]', forms).addClass('btn-primary');
    var lang = $('html').attr('lang');
    var defaultOptions = {
      submitHandler: PyAMS_form.submitHandler,
      messages: {}
    };

    var getFormOptions = function getFormOptions(form, options) {
      $('[data-ams-validate-messages]', form).each(function (idx, elt) {
        options.messages[$(elt).attr('name')] = $(elt).data('ams-validate-messages');
      });
      return options;
    };

    var validateForms = function validateForms() {
      $(forms).each(function (idx, form) {
        var options = $.extend({}, defaultOptions);
        $(form).validate(getFormOptions(form, options));
      });
    };

    if (lang === 'fr') {
      __webpack_require__.e(/*! import() */ "node_modules_jquery-validation_dist_localization_messages_fr_js").then(__webpack_require__.t.bind(__webpack_require__, /*! jquery-validation/dist/localization/messages_fr */ "./node_modules/jquery-validation/dist/localization/messages_fr.js", 23)).then(function () {
        validateForms();
      });
    } else {
      validateForms();
    }
  },
  submitHandler: function submitHandler(form) {
    var doSubmit = function doSubmit(form) {
      var button = $('button[type="submit"]', form),
          name = button.attr('name'),
          input = $('input[name="' + name + '"]', form);

      if (input.length === 0) {
        $('<input />').attr('type', 'hidden').attr('name', name).attr('value', button.attr('value')).appendTo(form);
      }

      form.submit();
    };

    if (window.grecaptcha) {
      // check if recaptcha was loaded
      var captcha_key = $(form).data('ams-form-captcha-key');
      grecaptcha.execute(captcha_key, {
        action: 'form_submit'
      }).then(function (token) {
        $('.state-error', form).removeClass('state-error');
        $('input[name="g-recaptcha-response"]', form).val(token);
        doSubmit(form);
      });
    } else {
      doSubmit(form);
    }
  }
};
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (PyAMS_form);

/***/ })

}]);
//# sourceMappingURL=src_pyams_content_skin_resources_src__form_js.pyams-dev.js.map