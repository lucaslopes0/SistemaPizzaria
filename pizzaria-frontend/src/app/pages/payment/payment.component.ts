import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';
import {
  PizzariaApiService,
  OrderResponse,
} from '../../core/services/pizzaria-api.service';

type MetodoPagamento = 'PIX' | 'CARTAO' | 'DINHEIRO';

@Component({
  selector: 'app-payment',
  standalone: true,
  templateUrl: './payment.component.html',
  styleUrls: ['./payment.component.scss'],
  imports: [CommonModule, RouterModule], // <-- IMPORTANTE
})
export class PaymentComponent implements OnInit {
  orderId?: number;
  order?: OrderResponse;
  loading = false;
  paying = false;
  error?: string;
  successMessage?: string;

  metodo: MetodoPagamento = 'PIX';

  constructor(
    private api: PizzariaApiService,
    private router: Router,
  ) {}

  ngOnInit(): void {
    const storedId = localStorage.getItem('orderId');
    if (storedId) {
      this.orderId = Number(storedId);
      this.loadOrder();
    } else {
      this.error = 'Nenhum pedido encontrado. Crie um pedido primeiro.';
    }
  }

  loadOrder(): void {
    if (!this.orderId) return;

    this.loading = true;
    this.error = undefined;

    this.api.getOrder(this.orderId).subscribe({
      next: (order) => {
        this.order = order;
        this.loading = false;
      },
      error: () => {
        this.error = 'Erro ao carregar pedido.';
        this.loading = false;
      },
    });
  }

  selectMetodo(m: MetodoPagamento): void {
    this.metodo = m;
    this.successMessage = undefined;
  }

  pagar(): void {
    if (!this.orderId) return;

    this.paying = true;
    this.error = undefined;
    this.successMessage = undefined;

    this.api.payOrder(this.orderId, this.metodo).subscribe({
      next: (res) => {
        this.successMessage = res?.message ?? 'Pagamento realizado com sucesso!';
        this.paying = false;
      },
      error: () => {
        this.error = 'Erro ao processar pagamento. Tente novamente.';
        this.paying = false;
      },
    });
  }

  goToTracking(): void {
    this.router.navigate(['/tracking']);
  }
}
