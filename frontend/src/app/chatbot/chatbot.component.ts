import { Component } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Component({
  selector: 'app-chatbot',
  //standalone: true,
  //imports: [],
  templateUrl: './chatbot.component.html',
  styleUrl: './chatbot.component.css'
})
export class ChatbotComponent {
  constructor(private http: HttpClient) {}

  isChatbotVisible = false;

  messages = [
    { sender: 'bot', text: 'Good evening [name], how can I help you today?' },
    { sender: 'user', text: 'What events are happening this week?' },
    { sender: 'bot', text: 'We’ve got a Hackathon on Friday! 🎉' }
  ];

  newMessage: string = '';

  //toggles chatbot between on and off
  toggleChatbot() {
    this.isChatbotVisible = !this.isChatbotVisible;
  }

  sendMessage() {
    const userMessage = this.newMessage.trim();
    const chat_id = 0;
    const api_response = '';
    // If user message is empty, do not send
    if (userMessage.length > 0) {
      this.messages.push({ sender: 'user', text: userMessage });
      this.http
        .post<any>('http://localhost:1560/api/chatbot/admin/chat', {
          chat_id: 0,
          user_prompt: userMessage,
          api_response: ''
        })
        .subscribe(
          (response: string) => {
            this.messages.push({ sender: 'bot', text: response });
            this.newMessage = '';
          },
          (error) => {
            console.error('Error:', error);
            this.messages.push({
              sender: 'bot',
              text: "Sorry, I couldn't process your request."
            });
          }
        );
    }
  }
}
