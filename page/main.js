setTimeout(() => {
  var elements = document.getElementsByClassName("afterOpen");
  console.log(elements);

  for(var i = 0; i < elements.length; i++) {
    elements[i].classList.add("display");
  }

}, 1200);
/*
var features = document.getElementById("features");
  document.onscroll = () => {
    if(document.documentElement.scrollTop > (features.offsetHeight - features.scrollHeight / 3)) {
      console.log("abc");
    }
}
*/
