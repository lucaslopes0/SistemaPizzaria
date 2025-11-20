import { Component } from '@angular/core';
import { RouterOutlet } from '@angular/router';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [RouterOutlet],
  template: `
    <!-- Componente raiz: apenas o roteador -->
    <router-outlet></router-outlet>
  `,
})
export class AppComponent {}
