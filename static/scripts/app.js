/**
 * Created by 0404070c on 17/03/2017.
 */

// Feedback for the register form
jQuery(function () {
  $("#register-form-submit").click(function () {
    $(".alert-danger").hide();
    var hasError = false;
    var passwordVal = $("#id_password").val();
    var checkVal = $("#password-check").val();
    if (passwordVal == '') {
      $("#id_password").after('<div class="alert alert-danger" role="alert">Please enter a password.</div>');
      hasError = true;
    } else if (checkVal == '') {
      $("#password-check").after('<div class="alert alert-danger" role="alert">Please comfirm your password.</div>');
      hasError = true;
    } else if (passwordVal != checkVal) {
      $("#password-check").after('<div class="alert alert-danger" role="alert">Your passwords do not match.</div>');
      hasError = true;
    }
    if (hasError == true) {
      return false;
    }
  });
});


jQuery(function () {
  $("#login-form-submit").click(function () {
    $(".alert-danger").hide();
    var hasError = false;
    var usernameVal = $("#login-username").val();
    var passwordVal = $("#login-password").val();
    if (usernameVal == '') {
      $("#login-username").after('<div class="alert alert-danger" role="alert">Please enter a username.</div>');
      hasError = true;
    }
    if (passwordVal == '') {
      $("#login-password").after('<div class="alert alert-danger" role="alert">Please enter a password.</div>');
      hasError = true;
    }
    if (hasError == true) {
      return false;
    }
  })
});