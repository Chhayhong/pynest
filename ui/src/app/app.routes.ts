import { Routes } from '@angular/router';

export const routes: Routes = [
  {
    path: '',
    loadChildren: () =>
      import('./client/auth/auth.module').then((m) => m.AuthModule),
  },
  {
    path: '',
    loadChildren: () =>
      import('./server/home/home.module').then((m) => m.HomeModule),
  },
];
