import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Router, RouterModule } from '@angular/router';
import {
  PizzariaApiService,
  MenuItem,
} from '../../core/services/pizzaria-api.service';

interface CartItem {
  pizza: MenuItem;
  quantidade: number;
}

@Component({
  selector: 'app-menu',
  standalone: true,
  templateUrl: './menu.component.html',
  styleUrls: ['./menu.component.scss'],
  imports: [CommonModule, RouterModule], // <<< IMPORTANTE
})
export class MenuComponent implements OnInit {
  menu: MenuItem[] = [];
  cart: CartItem[] = [];

  constructor(
    private api: PizzariaApiService,
    private router: Router,
  ) {}

  ngOnInit(): void {
    this.api.getMenu().subscribe((data) => {
      this.menu = data;
    });
  }

  addToCart(item: MenuItem): void {
    const existing = this.cart.find((c) => c.pizza.id === item.id);
    if (existing) {
      existing.quantidade++;
    } else {
      this.cart.push({ pizza: item, quantidade: 1 });
    }
  }

  goToCart(): void {
    localStorage.setItem('cart', JSON.stringify(this.cart));
    this.router.navigate(['/cart']);
  }
}
