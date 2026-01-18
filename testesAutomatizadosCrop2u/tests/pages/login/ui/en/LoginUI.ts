import { EMAIL_CLIENT, SENHA_CLIENT } from "@src/constants/constants";


export const loginPageServices = {
    login: EMAIL_CLIENT,
    senha: SENHA_CLIENT,
    btn: ""
} as const;

export const toastrLogin = {
    localElementoToastr: ".ngx-toastr",
    text: "",
    sucesso: " Login Successful!  Welcome to Crop2U ",
    error: " Login Error! Invalid email or password ",
    logout:  " Exiting the System  Exit successful! ",
    emailInvalido: " Invalid email, please enter a valid email. "
} as const;
