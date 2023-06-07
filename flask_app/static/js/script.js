
// smiley face hover change image + dropdown
const smiley_face = "/static/images/smiley_face.png"
const smiley_face_fill = "/static/images/smiley_face_fill.png"
dropdown_menu.addEventListener('mouseover', () => {
    hover_smiley.src = smiley_face_fill
    smile_dropdown.classList.remove('hidden')
    black_backdrop.classList.remove('hidden')
})
dropdown_menu.addEventListener('mouseout', () => {
    hover_smiley.src = smiley_face
    smile_dropdown.classList.add('hidden')
    black_backdrop.classList.add('hidden')
})


// login button clicked
function login_form(element) {

    login_reg_backdrop.classList.remove('hidden')
    login_reg_form_div.classList.remove('hidden')
    if(element.innerText == 'Log In') {
        user_login.classList.remove('hidden')
    } else {
        user_register.classList.remove('hidden')
    }
}

function exit_login_reg() {
    login_reg_backdrop.classList.add('hidden')
    login_reg_form_div.classList.add('hidden')
    user_login.classList.add('hidden')
    user_register.classList.add('hidden')
}

// swaps from login to registration form
function change_login_reg() {
    user_login.classList.toggle('hidden')
    user_register.classList.toggle('hidden')
}