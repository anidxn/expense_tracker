
/*	
 *  custom js file with common js functions
 *	Prasenjit Das, Sc-B
 *
 */
            function valdateDate(inputText){
                //var inputText = document.getElementById('txtDate').value;
                
                var dateformat = /^(0?[1-9]|[12][0-9]|3[01])[\/\-](0?[1-9]|1[012])[\/\-]\d{4}$/;
                // Match the date format through regular expression
                if(inputText.match(dateformat)) {
                   
                    //Test which seperator is used '/' or '-'
                    var opera1 = inputText.split('/');
                    var opera2 = inputText.split('-');
                    var lopera1 = opera1.length;
                    var lopera2 = opera2.length;
                    // Extract the string into month, date and year
                            if (lopera1 > 1) {
                                var pdate = inputText.split('/');
                            } else if (lopera2 > 1) {
                                var pdate = inputText.split('-');
                            }
                           
                            var dd = parseInt(pdate[0]);
                            var mm = parseInt(pdate[1]);
                            var yy = parseInt(pdate[2]);
                            // Create list of days of a month [assume there is no leap year by default]
                            var ListofDays = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31];
                            if (mm == 1 || mm > 2)
                            {
                                if (dd > ListofDays[mm - 1])
                                {
                                    // alert('Invalid date format!');
                                    return false;
                                }
                            }
                            if (mm == 2) {
                                var lyear = false;
                                if ((!(yy % 4) && yy % 100) || !(yy % 400)) {
                                    lyear = true;
                                }
                                if ((lyear == false) && (dd >= 29)) {
                                    // alert('Invalid date format!');
                                    return false;
                                } else if ((lyear == true) && (dd > 29)) {
                                    //alert('Invalid date format!');
                                    return false;
                                }
                            }
                            return true;
                } else {
                    // alert("Invalid date format!");
                    return false;
                }
            }
        
        //allow only alphabets & space
                    var mikExp2 = /^[a-zA-Z-,]+(\s{0,1}[a-zA-Z-, ])*$/;
                    function doTextOnlyWithSpace(txtctrl) {
                        var txtval = txtctrl.value;
                        if (!txtval.match(mikExp2)) {
                            txtctrl.value = txtval.substring(0, (txtval.length) - 1);
                        }
                    }
        
        //make the text uppercase
                    function makeuppercase(param) {
                        document.getElementById(param).value = document.getElementById(param).value.toUpperCase();
                    }
          
        //allow only numbers
                    function numbersonly(e) {
                        var unicode = e.charCode ? e.charCode : e.keyCode
                        if (unicode != 8 && unicode != 9) { //if the key isn't the backspace / tab key (which we should allow)
                            if (unicode < 48 || unicode > 57) //if not a number
                            return false //disable key press
                        }
                    }
                    
            //username pattern - only alphabets & digits
                    var usrnExp = /^[a-zA-Z0-9]*$/;
                    function isValidUname(txtuname) {
                        if (!txtuname.match(usrnExp)) {
                            return false;
                        }
                        return true;
                    }
                    
                    var passExp = /((?=.*\\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[@#$%]).{6,20})/;
                    function isValidPass(txtpass) {
                        if (!txtpass.match(passExp)) {
                            return false;
                        }
                        return true;
                    }
            
            //only alphabets
                    var alExp = /[$\\@\\\#%\^\&\*\(\)\[\]\+\_\{\}\`\~\!\ \-\=\|]/;
                    function doTextOnly(val) {
                        var strPass = val.value;
                        var strLength = strPass.length;
                        var lchar = val.value.charAt((strLength) - 1);
                        var re = /[^a-zA-Z]/;
                        if (lchar.search(alExp) != -1 || re.test(strPass)) {
                            var tst = val.value.substring(0, (strLength) - 1);
                            val.value = tst;
                        }
                    }
                    
    function isValidEmail(txtMail) {
        var  mailformat = /^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/;
        if (txtMail.match(mailformat)) {
            return true;
        }
            
        return false;
    }
    
    /* HTML decode functions */
    
    var decodeEntities = (function() {
        var element = document.createElement('div');
        
        function decodeHTMLEntities(str){
            if(str && typeof str === 'string') {
                //strip script/html tags
                str = str.replace(/<script[^>*]([\S\s]*?)<\/script>/gmi, '');
                str = str.replace(/<\/?\w(?:[^"'>]|"[^"]*"|'[^']*')*>/gmi, '');
                element.innerHTML = str;
                str = element.textContent;
                element.textContent = '';
            }
            
            return str;
        }
        return decodeHTMLEntities;
    })();
            
            