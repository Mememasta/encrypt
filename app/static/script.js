document.addEventListener("DOMContentLoaded", function(event) {
    
    document.getElementById("btn_des_encrypt").addEventListener("click",
        function(e){
            form = document.getElementById('form_des_encrypt')
            key = form.key.value
            message = form.message.value
            padding = form.padding.checked
            data = {key: key, message: message, padding: padding}
            url = "/api/v1/utils/des/encrypt"
            block_error = "error_des_encrypt"
            block_resp = "resp_des_encrypt"
            sendAjax(data, url, block_error, block_resp);
        }
    );

    document.getElementById("btn_des_decrypt").addEventListener("click",
        function(e){
            form = document.getElementById('form_des_decrypt')
            key = form.key.value
            encrypted_message = form.message.value
            padding = form.padding.checked
            data = {key: key, encrypted_message: encrypted_message, padding: padding}
            url = "/api/v1/utils/des/decrypt"
            block_error = "error_des_decrypt"
            block_resp = "resp_des_decrypt"
            sendAjax(data, url, block_error, block_resp);
        }
    );

    document.getElementById("btn_wgnr_encrypt").addEventListener("click",
        function(e){
            form = document.getElementById('form_wgnr_encrypt')
            key = form.key.value
            message = form.message.value
            data = {key: key, message: message}
            url = "/api/v1/utils/wiegener/encrypt"
            block_error = "error_wgnr_encrypt"
            block_resp = "resp_wgnr_encrypt"
            sendAjax(data, url, block_error, block_resp);
        }
    );

    document.getElementById("btn_wgnr_decrypt").addEventListener("click",
        function(e){
            form = document.getElementById('form_wgnr_decrypt')
            key = form.key.value
            encrypted_message = form.message.value
            data = {key: key, encrypted_message: encrypted_message}
            url = "/api/v1/utils/wiegener/decrypt"
            block_error = "error_wgnr_decrypt"
            block_resp = "resp_wgnr_decrypt"
            sendAjax(data, url, block_error, block_resp);
        }
    );
});


function sendAjax(data, url, block_error, block_resp) {
    // var form = {key: key, message: message}
    var data_obj = JSON.stringify(data)
    var request = new XMLHttpRequest();
    
    request.open('POST', url, true);
    request.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded; charset=UTF-8');
    request.onload = function() {
        if (this.status >= 200 && this.status < 400) {
          // Success!
          document.getElementById(block_error).innerHTML = ''
          var resp = this.response;
          resp_obj = JSON.parse(resp)
          block = document.getElementById(block_resp)
          block.style.display = 'inline'
          if (resp_obj.encrypted_message)
            block.children['resp'].value = resp_obj.encrypted_message
          else
            block.children['resp'].value = resp_obj.message
            
        } else {
            document.getElementById(block_resp).style.display = 'none'
            var err = this.response;
            err = JSON.parse(err)
            document.getElementById(block_error).innerHTML = err.detail
        }
      };
      
      request.onerror = function() {
          //ERROR
          document.getElementById(block_resp).style.display = 'none'
          document.getElementById(block_error).innerHTML = ''
          var err = this.response;
          document.getElementById(block_error).innerHTML = err
      };
    request.send(data_obj);
}
    
    
