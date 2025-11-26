// small helper - hide flash messages after timeout
document.addEventListener('DOMContentLoaded', function(){
  const flashes = document.querySelectorAll('.flash');
  if(flashes.length){
    setTimeout(()=> {
      flashes.forEach(el => el.style.display = 'none');
    }, 3500);
  }
});
