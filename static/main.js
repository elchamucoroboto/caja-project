var formatter = new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency: 'USD',

    // These options are needed to round to whole numbers if that's what you want.
    //minimumFractionDigits: 0,
    //maximumFractionDigits: 0,
  });

  var amounts = document.getElementsByClassName("op-amount");
  for (var i = 0; i < amounts.length; i++) {

       amounts[i].innerHTML = formatter.format(parseFloat(amounts[i].innerHTML));
  }

  //CAMBIA COLOR SEGUN METODO DE PAGO

  var colores = ["list-group-item-success","list-group-item-danger","list-group-item-warning"]

  
  var classColor = document.getElementsByClassName("list-group-item");
  for (var i = 0; i < classColor.length; i++){
    if (classColor[i].innerHTML.indexOf('ZELLE') > -1 || classColor[i].innerHTML.indexOf('DOLARES') > -1){
      classColor[i].className += " " +colores[0]

    }
    if (classColor[i].innerHTML.indexOf('PUNTO') > -1 || classColor[i].innerHTML.indexOf('BOLIVARES') > -1){
      classColor[i].className += " " +colores[2]

    }
    if (classColor[i].innerHTML.indexOf('DEVOLUCION') > -1) {
      classColor[i].className += " " +colores[1]

    }
  } 

