var currentTabs = {};

function showTab(n, formId) {
  // This function will display the specified tab of the form ...
  var form = document.getElementById(formId);
  var x = form.getElementsByClassName("tab");
  x[n].style.display = "block";
  // ... and fix the Previous/Next buttons:
  if (n == 0) {
    document.getElementById("prevBtn"+formId).style.display = "none";
  } else {
    document.getElementById("prevBtn"+formId).style.display = "inline";
  }
  if (n == (x.length - 1)) {
    document.getElementById("nextBtn"+formId).innerHTML = "Submit";
  } else {
    document.getElementById("nextBtn"+formId).innerHTML = "Next";
  }
  // ... and run a function that displays the correct step indicator:
  fixStepIndicator(n, formId);
}

function nextPrev(n, formId) {
  var currentTab = currentTabs[formId];
  // This function will figure out which tab to display
  var form = document.getElementById(formId);
  var x = form.getElementsByClassName("tab");
  // Exit the function if any field in the current tab is invalid:
  if (n == 1 && !validateForm(formId)) {
    var btn = document.getElementById("nextBtn"+formId);
    btn.classList.add("shake-on-error");
    setTimeout(function(){btn.classList.remove("shake-on-error");}, 200);
    return false;
  }
  // Hide the current tab:
  if (n === -1 && currentTab ===0) return false;
  x[currentTab].style.display = "none";
  // Increase or decrease the current tab by 1:
  currentTab = currentTab + n;
  // if you have reached the end of the form... :
  if (currentTab >= x.length) {
    //...the form gets submitted:
    form.submit();
    return false;
  }
  // Otherwise, display the correct tab:
  currentTabs[formId] = currentTab;
  showTab(currentTab, formId);
//  document.getElementById(formId).scrollIntoView();
}

function validateForm(formId) {
  // This function deals with validation of the form fields
  var currentTab = currentTabs[formId];
  var x, y, i, valid = true;
  var form = document.getElementById(formId);
  x = form.getElementsByClassName("tab");
  y = x[currentTab].getElementsByTagName("input");
  textAreas = x[currentTab].getElementsByTagName("textarea");
  // A loop that checks every input field in the current tab:
  for (i = 0; i < y.length; i++) {
    // If a field is empty...
    if (y[i].required === true && y[i].value == "") {
      // add an "invalid" class to the field:
      y[i].className += " invalid";
      // and set the current valid status to false:
      valid = false;
    }
  }
  for (i = 0; i < textAreas.length; i++) {
    // If a field is empty...
    if (textAreas[i].required === true && textAreas[i].value == "") {
      // add an "invalid" class to the field:
      textAreas[i].className += " invalid";
      // and set the current valid status to false:
      valid = false;
    }
  }
  // If the valid status is true, mark the step as finished and valid:
  if (valid) {
    form.getElementsByClassName("step")[currentTab].className += " finish";
  }
  return valid; // return the valid status
}

function fixStepIndicator(n, formId) {
  // This function removes the "active" class of all steps...
  var form = document.getElementById(formId);
  var i, x = form.getElementsByClassName("step");
  for (i = 0; i < x.length; i++) {
    x[i].className = x[i].className.replace(" active", "");
  }
  //... and adds the "active" class to the current step:
  x[n].className += " active";
}

function appendDiv(source, target, dividerText='Achievement', counter='number_of_achievements') {
    sourceElement = document.getElementById(source).cloneNode(true);
    targetElement = document.getElementById(target);
    var number = parseInt(document.getElementById(counter).value);
    for (i = 0; i < sourceElement.children.length; i++) {
        var formElement = sourceElement.children[i];
        var textArea = formElement.getElementsByTagName('textarea');
        var Input = formElement.getElementsByTagName('input');
        var Select = formElement.getElementsByTagName('select');
        if (Input.length > 0) {
            Input[0].id += number;
            Input[0].name += number;
        }
        if (textArea.length > 0) {
            textArea[0].id += number;
            textArea[0].name += number;
        }
        if (Select.length > 0) {
            Select[0].id += number;
            Select[0].name += number;
        }
    }
    sourceElement.id += number + 1;
    targetElement.innerHTML += '<hr class="hr hr-blurry" /><h5>'+ dividerText +'</h5>' + sourceElement.innerHTML;
    document.getElementById(counter).value = number + 1;
}