import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

const API_BASE = 'http://127.0.0.1:5000';

export interface MenuItem {
  id: string;
  nome: string;
  preco: number;
}

export interface OrderItemPayload {
  pizza_id: string;
  quantidade: number;
}

export interface DescontoPayload {
  tipo: 'percentual' | 'valor_minimo';
  percentual?: number;
  minimo?: number;
  desconto_fixo?: number;
}

export interface OrderResponse {
  id: number;
  status: string;
  itens: {
    pizza: { nome: string; preco: number };
    quantidade: number;
    total: number;
  }[];
  subtotal: number;
  desconto: number;
  total_final: number;
}

@Injectable({ providedIn: 'root' })
export class PizzariaApiService {
  constructor(private http: HttpClient) {}

  getConfig(): Observable<any> {
    return this.http.get(`${API_BASE}/config`);
  }

  getMenu(): Observable<MenuItem[]> {
    return this.http.get<MenuItem[]>(`${API_BASE}/menu`);
  }

  createOrder(
    itens: OrderItemPayload[],
    desconto?: DescontoPayload
  ): Observable<OrderResponse> {
    const body: any = { itens };
    if (desconto) {
      body.desconto = desconto;
    }
    return this.http.post<OrderResponse>(`${API_BASE}/orders`, body);
  }

  getOrder(id: number): Observable<OrderResponse> {
    return this.http.get<OrderResponse>(`${API_BASE}/orders/${id}`);
  }

  updateOrderStatus(id: number, status: string): Observable<OrderResponse> {
    return this.http.patch<OrderResponse>(
      `${API_BASE}/orders/${id}/status`,
      { status }
    );
  }

  payOrder(id: number, metodo: 'PIX' | 'CARTAO' | 'DINHEIRO'): Observable<any> {
    return this.http.post(`${API_BASE}/orders/${id}/pay`, { metodo });
  }
}
