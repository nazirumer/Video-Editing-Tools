

/* start progress bar */

const one = document.querySelector(".one");

const two = document.querySelector(".two");

const three = document.querySelector(".three");

const four = document.querySelector(".four");

const five = document.querySelector(".five");



one.onclick = function() {

    one.classList.add("active");

    two.classList.remove("active");

    three.classList.remove("active");

    four.classList.remove("active");

    five.classList.remove("active");

}


two.onclick = function() {

    one.classList.add("active");

    two.classList.add("active");

    three.classList.remove("active");

    four.classList.remove("active");

    five.classList.remove("active");

}

three.onclick = function() {

    one.classList.add("active");

    two.classList.add("active");

    three.classList.add("active");

    four.classList.remove("active");

    five.classList.remove("active");

}

four.onclick = function() {

    one.classList.add("active");

    two.classList.add("active");

    three.classList.add("active");

    four.classList.add("active");

    five.classList.remove("active");

}

five.onclick = function() {

    one.classList.add("active");

    two.classList.add("active");

    three.classList.add("active");

    four.classList.add("active");

    five.classList.add("active");

}
/* index */



/* end progress bar */

/* start preview */

function cut_o() {
    var x = document.getElementById('cut_o');
    if (x.style.display === 'none') {
      x.style.display = 'block';
    } 
    else {
      x.style.display = 'none';
    }
  }
  
  function cut_m() {
    var x = document.getElementById('cut_m');
    if (x.style.display === 'none') {
      x.style.display = 'block';
    } 
    else {
      x.style.display = 'none';
    }
  }

/* end preview */

/* start templates */


function select_template(){
    var x = document.getElementById('all-templates');
    var y = document.getElementById('create-template');
    if (x.style.display === 'none') {
      y.style.display = 'none'
      x.style.display = 'block';
    } 
    else {
      x.style.display = 'none';
    }
  }
  
  function create_template(){
    var x = document.getElementById('create-template');
    var y = document.getElementById('all-templates');
    if (x.style.display === 'none') {
      x.style.display = 'block';
      y.style.display ='none'
    }
    else {
      x.style.display = 'none';
    }
  }
  
  function temp_1_1(){
    var x = document.getElementById('size-input');
    var input_w = document.getElementById('width');
    var input_h = document.getElementById('height');
    if (x.style.display === 'none') {
      x.style.display = 'block';
      input_w.value = "720";
      input_h.value = '720';
    }
    else {
      x.style.display = 'none';
    }
  }
  
 
/*     var original = document.getElementById('inputState1');
    var merged = document.getElementById('inputState2');
    //var input_w = document.getElementById('width');
    //var input_h = document.getElementById('height');
    
    if (original.sele === 'top') {
      //x.style.display = 'block';
      //input_w.value = "720";
      //input_h.value = '1280';
      document.write('yes')
    }
    else {
      x.style.display = 'none';
    }
 */
  

/*   function set(){
    var x = document.getElementById('setting')
    if (x.style.display === 'none'){
      x.style.display = 'block'
    }
    else{
      x.style.display = 'none'
    }
  } */

  /* end templates */

