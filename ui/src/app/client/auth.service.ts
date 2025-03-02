import { HttpClient } from '@angular/common/http';
import { inject, Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root'
})
export class AuthService {
  private readonly apiUrl: string = 'localhost:8000';
  http = inject(HttpClient)

  login(credentials: {username: string, password: string}) {
    return this.http.post(this.apiUrl+'/v1/account/token', credentials)
  }
  register(account: {username: string, password: string,confirm_password:string}) {
    return this.http.post(this.apiUrl+'/v1/account', account)
  }
}
