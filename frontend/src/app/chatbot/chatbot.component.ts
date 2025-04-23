import { Component, ElementRef, ViewChild } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Component({
  selector: 'app-chatbot',
  //standalone: true,
  //imports: [],
  templateUrl: './chatbot.component.html',
  styleUrl: './chatbot.component.css'
})
export class ChatbotComponent {
  @ViewChild('messagesContainer') private messagesContainer!: ElementRef;
  constructor(private http: HttpClient) {}

  isChatbotVisible = false;

  messages = [
    { sender: 'bot', text: 'Good evening [name], how can I help you today?' }
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
      this.newMessage = ''; //clears the input field
      this.http
        .post<any>('/api/chatbot/admin/chat', {
          chat_id: 0,
          user_prompt: userMessage,
          api_response: '',
          session_id: 0
        })
        .subscribe(
          (response: string) => {
            this.messages.push({ sender: 'bot', text: response });
            this.newMessage = '';
            this.scrollToBottom();
          },
          (error) => {
            console.error('Error:', error);
            this.messages.push({
              sender: 'bot',
              text: "Sorry, I couldn't process your request."
            });
            this.scrollToBottom();
          }
        );
      setTimeout(() => this.scrollToBottom(), 1000);
    }
  }

  scrollToBottom() {
    try {
      this.messagesContainer.nativeElement.scrollTop =
        this.messagesContainer.nativeElement.scrollHeight;
    } catch (err) {
      console.warn('Could not scroll to bottom:', err);
    }
  }

  resetSession() {
    //saves current session and resets chat window
  }

  showSessions() {
    //shows previous user sessions with the bot
  }
}
