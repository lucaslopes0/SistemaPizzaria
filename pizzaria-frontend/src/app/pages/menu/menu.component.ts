import { Component, OnInit } from '@angular/core';
import { PizzariaApiService, MenuItem } from '../../core/services/pizzaria-api.service';
import { Router } from '@angular/router';

interface CartItem {
  pizza: MenuItem;
  quantidade: number;
}

@Component({
  selector: 'app-menu',
  templateUrl: './menu.component.html',
  styleUrls: ['./menu.component.scss'],
})
export class MenuComponent implements OnInit {
  menu: MenuItem[] = [];
  cart: CartItem[] = [];

  constructor(
    private api: PizzariaApiService,
    private router: Router
  ) {}

  ngOnInit(): void {
    this.api.getMenu().subscribe((data) => {
      this.menu = data;
    });
  }

  addToCart(item: MenuItem): void {
    const existing = this.cart.find(c => c.pizza.id === item.id);
    if (existing) {
      existing.quantidade++;
    } else {
      this.cart.push({ pizza: item, quantidade: 1 });
    }
  }

  goToCart(): void {
    // em versão simples, você pode guardar o carrinho no localStorage
    localStorage.setItem('cart', JSON.stringify(this.cart));
    this.router.navigate(['/cart']);
  }
}
