import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { ChatMessageResponse } from '../models.module';

@Injectable({
  providedIn: 'root'
})
export class frontendChatbotService {
  constructor(private http: HttpClient) {}

  getAllMessages(id: number): Observable<ChatMessageResponse[]> {
    return this.http.get<ChatMessageResponse[]>(
      `/api/chatbot/admin/session/${id}`
    );
  }

  getAllSessions(): Observable<number[]> {
    return this.http.get<number[]>(`/api/chatbot/admin/sessions/`);
  }
}
