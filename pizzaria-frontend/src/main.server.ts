import { bootstrapApplication, BootstrapContext } from '@angular/platform-browser';
import { provideRouter } from '@angular/router';
import { provideHttpClient, withFetch } from '@angular/common/http'; // <-- withFetch aqui

import { AppComponent } from './app/app.component';
import { routes } from './app/app.routes';

export default function bootstrap(context: BootstrapContext) {
  return bootstrapApplication(AppComponent, {
    providers: [
      provideRouter(routes),
      provideHttpClient(withFetch()), // <-- IMPORTANTE: usar fetch no SSR
    ],
  }, context);
}
