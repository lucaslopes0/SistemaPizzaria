import { Component, OnInit } from '@angular/core';
import { Router, ActivatedRoute } from '@angular/router';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';
import {
  PizzariaApiService,
  OrderResponse,
} from '../../core/services/pizzaria-api.service';

@Component({
  selector: 'app-order-tracking',
  standalone: true,
  templateUrl: './order-tracking.component.html',
  styleUrls: ['./order-tracking.component.scss'],
  imports: [CommonModule, RouterModule], // <-- IMPORTANTE
})
export class OrderTrackingComponent implements OnInit {
  orderId?: number;
  order?: OrderResponse;
  loading = false;
  error?: string;

  constructor(
    private api: PizzariaApiService,
    private router: Router,
    private route: ActivatedRoute,
  ) {}

  ngOnInit(): void {
    const routeId = this.route.snapshot.paramMap.get('id');
    if (routeId) {
      this.orderId = Number(routeId);
    } else {
      const storedId = localStorage.getItem('orderId');
      if (storedId) {
        this.orderId = Number(storedId);
      }
    }

    if (!this.orderId) {
      this.error = 'Nenhum pedido encontrado. Crie um pedido primeiro.';
      return;
    }

    this.loadOrder();
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
        this.error = 'Erro ao carregar pedido. Tente novamente.';
        this.loading = false;
      },
    });
  }

  goToPayment(): void {
    this.router.navigate(['/payment']);
  }
}
