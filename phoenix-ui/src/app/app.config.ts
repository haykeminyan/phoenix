import { ApplicationConfig } from '@angular/core';
import { provideRouter } from '@angular/router';

import { routes } from './app.routes';
import {HTTP_INTERCEPTORS, provideHttpClient, withInterceptors, withInterceptorsFromDi} from "@angular/common/http";
import {AuthComponent} from "./components/auth/auth.component";
import {provideAnimations} from "@angular/platform-browser/animations";
import {provideClientHydration} from "@angular/platform-browser";
import { provideAnimationsAsync } from '@angular/platform-browser/animations/async';
import {CarouselModule} from "ngx-bootstrap/carousel";

interface AppConfig extends ApplicationConfig {
  imports: any[]; // Define the 'imports' property
}

export const appConfig: AppConfig = {
  imports: [CarouselModule.forRoot(),],
  providers: [
    provideRouter(routes),
    provideClientHydration(),
    provideHttpClient(withInterceptorsFromDi()),
    provideAnimations(),
    {
      provide:HTTP_INTERCEPTORS,
      useClass:AuthComponent,
      multi:true
    }, provideAnimationsAsync()
  ],

};
