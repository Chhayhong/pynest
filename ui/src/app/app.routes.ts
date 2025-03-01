import { Routes } from '@angular/router';

export const routes: Routes = [
  {
    path: 'auth',
    loadChildren: () =>
      import('./client/auth/auth.module').then((m) => m.AuthModule),
  },
  {
    path: 'home',
    loadChildren: () =>
      import('./server/home/home.module').then((m) => m.HomeModule),
  },
  {
    path: 'auth',
    redirectTo: 'login',
    pathMatch: 'full'
  }
];
