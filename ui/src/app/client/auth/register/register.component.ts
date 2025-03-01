import {ChangeDetectionStrategy, Component, inject, signal} from '@angular/core';
import { FormBuilder, Validators } from '@angular/forms';
import { RegisterAccount } from '../interface/account';
@Component({
  selector: 'app-register',
  templateUrl: './register.component.html',
  styleUrl: './register.component.scss',
  standalone:false,
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class RegisterComponent {
  formBuilder = inject(FormBuilder)
  registrationAccountForm = this.formBuilder.group({
    username: ['', [Validators.required,Validators.minLength(6),Validators.maxLength(255)]],
    password: ['',[Validators.required,Validators.minLength(6),Validators.maxLength(255)]],
    confirm_password: ['',[Validators.required,Validators.minLength(6),Validators.maxLength(255)]],
  });

  onSave(){
    console.log(this.registrationAccountForm.value)
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
