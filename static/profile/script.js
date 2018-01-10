function chClassNameByIdName(idnm, classnm) {
  document.getElementById(idnm).className = classnm;
}
function chClassNameByClassName(base_class, classnm) {
  var items = document.getElementsByClassName(base_class)
  for(i=0; i<items.length; i++) {
    items[i].className = classnm;
  }
}
function show(idnm) {
  chClassNameByClassName('profile-items', 'profile-items hidden animated fadeOut');
  chClassNameByIdName(idnm, 'profile-items shown animated fadeIn');
}
function toggle(idnm) {
  chClassNameByClassName('menu-items', 'menu-items idle');
  chClassNameByIdName(idnm, 'menu-items active');
}
