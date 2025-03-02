import {ChangeDetectionStrategy, Component, inject, signal} from '@angular/core';
import { FormBuilder, Validators } from '@angular/forms';
import { RegisterAccount } from '../interface/account';
import { AuthService } from '../../auth.service';
@Component({
  selector: 'app-register',
  templateUrl: './register.component.html',
  styleUrl: './register.component.scss',
  standalone:false,
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class RegisterComponent {
  formBuilder = inject(FormBuilder)
  authService = inject(AuthService)
  registrationAccountForm = this.formBuilder.group({
    username: ['', [Validators.required,Validators.minLength(6),Validators.maxLength(255)]],
    password: ['',[Validators.required,Validators.minLength(6),Validators.maxLength(255)]],
    confirm_password: ['',[Validators.required,Validators.minLength(6),Validators.maxLength(255)]],
  });

  onRegister(){
    console.log(this.registrationAccountForm.value)
    const { username, password,confirm_password } = this.registrationAccountForm.value as { username:string, password:string, confirm_password:string}
    if(password === confirm_password){
     this.authService.register({username, password,confirm_password}).subscribe((response) => {
       console.log(response);
     })
    } else {
      alert('Passwords do not match')
    }
  }


  hide = signal(true);
  confirmPasswordHide = signal(true);  
  clickEvent(event: MouseEvent,type: 'password' | 'confirmPassword') {
    if (type === 'confirmPassword') {
      this.confirmPasswordHide.set(!this.confirmPasswordHide());
    }  else {
      this.hide.set(!this.hide());
    }
    event.stopPropagation();
  }

}
