import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { HttpClient } from '@angular/common/http';
import { map } from 'rxjs/operators';
import { ChatMessageResponse } from '../models.module';

@Injectable({
  providedIn: 'root'
})
export class ChatbotServiceService {
  constructor(protected http: HttpClient) {}

  // Post the user's message to the OpenAI API
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

  // Get the user's name from the profile service
  getUserName(): Observable<string> {
    return this.http
      .get<any>('/api/profile')
      .pipe(map((profile) => profile.first_name));
  }

  getAllMessages(id: number): Observable<ChatMessageResponse[]> {
    return this.http.get<ChatMessageResponse[]>(
      `/api/chatbot/admin/session/${id}`
    );
  }

  getAllSessions(): Observable<number[]> {
    return this.http.get<number[]>(`/api/chatbot/admin/sessions/`);
  }
}
