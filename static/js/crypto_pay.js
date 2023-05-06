window.addEventListener('load', async () => {
      if (window.ethereum) {
        window.web3 = new Web3(ethereum);
        try {
          await ethereum.enable();
          initPayButton()
        } catch (err) {
            alert("Usuario denegó acceso!")
            //$('#status').html('User denied account access', err)
        }
      } else if (window.web3) {
        window.web3 = new Web3(web3.currentProvider)
        initPayButton()
      } else {
          alert("Metamask no se encuentra instalado en el navegador!")
          //$('#status').html('No Metamask (or other Web3 Provider) installed')
      }
    })

    const initPayButton = () => {
      $('#btn-pago').click(() => {
        // paymentAddress is where funds will be sent to
        const paymentAddress = '0x094e6DFb93885127ed28942093Dd95DAFeB2aBAb'
        var amountEth = document.getElementById("pagar_eth").innerHTML

        web3.eth.sendTransaction({
          to: paymentAddress,
          value: web3.toWei(amountEth, 'ether')
        }, (err, transactionId) => {
          if  (err) {
            console.log('Payment failed', err)
            //$('#status').html('Payment failed')
              alert("Pago fallido! Intente nuevamente")
          } else {
            console.log('Payment successful', transactionId)
            //$('#status').html('Payment successful')
              alert("Pago exitoso! Muchas gracias")
          }
        })
      })
    }