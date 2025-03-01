import { HttpInterceptorFn } from '@angular/common/http';

export const InterceptorInterceptor: HttpInterceptorFn = (req, next) => {
  console.log(req)
  req = req.clone({
    headers: req.headers.set('Authorization', 'Bearer your_token')
  });
  return next(req);
};
