function makeRegistration(form) {
    console.log(form)
    if (form.email.value != null && form.password.value != null) {
        let data = {
            'email':form.email.value,
            'password':form.password.value,
            'name':form.name.value
        }
        postCall('http://127.0.0.1:5000/registerRequest', data, 'register')
    } else {
        alert("Error Password or Username")
    }
}
