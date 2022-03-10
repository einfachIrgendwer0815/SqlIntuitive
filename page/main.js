setTimeout(() => {
  var elements = document.getElementsByTagName("section");
  console.log(elements);

  for(var i = 0; i < elements.length; i++) {
    elements[i].classList.add("visible");
  }

}, 1200);
