import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Router, RouterModule } from '@angular/router';
import {
  PizzariaApiService,
  OrderItemPayload,
} from '../../core/services/pizzaria-api.service';

@Component({
  selector: 'app-cart',
  standalone: true,
  templateUrl: './cart.component.html',
  styleUrls: ['./cart.component.scss'],
  imports: [CommonModule, RouterModule], // <<< IMPORTANTE
})
export class CartComponent implements OnInit {
  cart: any[] = [];
  orderId?: number;

  constructor(
    private api: PizzariaApiService,
    private router: Router,
  ) {}

  ngOnInit(): void {
    const stored = localStorage.getItem('cart');
    this.cart = stored ? JSON.parse(stored) : [];
  }

  get subtotal(): number {
    return this.cart.reduce(
      (acc, item) => acc + item.pizza.preco * item.quantidade,
      0,
    );
  }

  finalizarPedido(): void {
    const itens: OrderItemPayload[] = this.cart.map((item: any) => ({
      pizza_id: item.pizza.id,
      quantidade: item.quantidade,
    }));

    this.api
      .createOrder(itens, {
        tipo: 'percentual',
        percentual: 0.1,
      })
      .subscribe((order) => {
        this.orderId = order.id;
        localStorage.setItem('orderId', String(order.id));
        this.router.navigate(['/payment']);
      });
  }
}
