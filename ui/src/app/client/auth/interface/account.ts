import { FormControl } from "@angular/forms";

export interface Account {
    username:FormControl<string>;
    password: FormControl<string>;
}
export interface RegisterAccount extends Account {
    confirm_password: FormControl<string>;
}