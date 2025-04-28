import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { HttpClient } from '@angular/common/http';

@Injectable({
  providedIn: 'root'
})
export class ChatbotServiceService {
  constructor(protected http: HttpClient) {}

  postMessage(
    userMessage: string,
    chat_id: number,
    api_response: string,
    session_id: number
  ): Observable<any> {
    return this.http.post<any>('/api/chatbot/chat', {
      chat_id: chat_id,
      user_prompt: userMessage,
      api_response: api_response,
      session_id: session_id
    });
  }
}
