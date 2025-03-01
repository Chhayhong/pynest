import { RenderMode, ServerRoute } from '@angular/ssr';

export const serverRoutes: ServerRoute[] = [
  { path: 'login', renderMode: RenderMode.Client },
  { path: 'register', renderMode: RenderMode.Client },
  
  // {
  //   path: 'error',
  //   renderMode: RenderMode.Server,
  //   status: 404,
  //   headers: {
  //     'Cache-Control': 'no-cache',
  //   },
    
  // },
  { path: '**', renderMode: RenderMode.Server },
];
