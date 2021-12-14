//password and mail-id validation
function validate(){
    var mail = document.getElementById("mail").value;
    var regx = /^([a-z]+)@gmail.com$/;
    var pass = document.getElementById("pass").value;
    var repass = document.getElementById("repass").value;
    var n = pass.length;
    var cap=0,small=0,num=0,misc=0;
    for( var i=0;i<n;i++){
        var temp = pass.charCodeAt(i);
        if(temp >=65 && temp<=90){
            cap++;
        }else if(temp>=97 && temp <= 122){
            small++;
        }else if(temp>=48 && temp <= 57){
            num++;
        }else if( (temp>=33 && temp <= 47) || (temp>=58 && temp <= 64) ){
            misc++;
        }
    }
    if (regx.test(mail) && num && misc && cap && small && n >= 8 && (pass == repass)) {
        //alert("Valid!")
        return true;
    } else {
        if(pass !== repass){
            alert("Passwords must match!");
        }else{
            if(!(num && cap && misc && small)){
                alert("Password should have atleast a small letter, capital letter, misc value, a  number and a minimum length of 8");
            }else{
                alert("Invalid mail-id");
            }
        }
        return false;
    }
}