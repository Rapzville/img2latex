
let input = document.querySelector("input[type='file']");
input.onchange = function () {
   this.form.submit();
}