import { ApplicationConfig } from '@angular/core';
import { provideRouter } from '@angular/router';
import { serverRoutes } from './app.routes.server';

export const appConfig: ApplicationConfig = {
  providers: [
    provideRouter(serverRoutes),
  ],
};
