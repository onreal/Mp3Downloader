function makeLogin(form) {
    console.log(form)
    if (form.email.value != null && form.password.value != null) {
        let data = {
            'email':form.email.value,
            'password':form.password.value
        }
        postCall('http://127.0.0.1:5000/loginRequest', data, 'login')
    } else {
        alert("Error Password or Username")/*displays error message*/
    }
}