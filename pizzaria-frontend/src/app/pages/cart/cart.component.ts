import { Component, OnInit } from '@angular/core';
import { PizzariaApiService, OrderItemPayload } from '../../core/services/pizzaria-api.service';
import { Router } from '@angular/router';

@Component({
  selector: 'app-cart',
  templateUrl: './cart.component.html',
})
export class CartComponent implements OnInit {
  cart: any[] = [];
  orderId?: number;

  constructor(
    private api: PizzariaApiService,
    private router: Router
  ) {}

  ngOnInit(): void {
    const stored = localStorage.getItem('cart');
    this.cart = stored ? JSON.parse(stored) : [];
  }

  get subtotal(): number {
    return this.cart.reduce((acc, item) => acc + item.pizza.preco * item.quantidade, 0);
  }

  finalizarPedido(): void {
    const itens: OrderItemPayload[] = this.cart.map((item: any) => ({
      pizza_id: item.pizza.id,
      quantidade: item.quantidade,
    }));

    // Exemplo com 10% de desconto (Strategy CupomPercentual)
    this.api.createOrder(itens, {
      tipo: 'percentual',
      percentual: 0.1,
    }).subscribe(order => {
      this.orderId = order.id;
      localStorage.setItem('orderId', String(order.id));
      // poderia redirecionar direto para pagamento ou tracking
      this.router.navigate(['/payment']);
    });
  }
}
