import { Component, ElementRef, ViewChild } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { ChatbotServiceService } from './chatbot-service.service';

@Component({
  selector: 'app-chatbot',
  templateUrl: './chatbot.component.html',
  styleUrl: './chatbot.component.css'
})
export class ChatbotComponent {
  @ViewChild('messagesContainer') private messagesContainer!: ElementRef;

  userName: string = '';
  isChatbotVisible: boolean = false;
  newMessage: string = '';
  messages = [
    { sender: 'bot', text: 'Good evening, how can I help you today?' }
  ];

  constructor(private chatbotSVC: ChatbotServiceService) {}

  ngOnInit() {
    this.chatbotSVC.getUserName().subscribe((name: string) => {
      this.userName = name;
      this.messages[0].text = `Good evening ${this.userName}, how can I help you today?`;
    });
  }

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
      this.chatbotSVC
        .postMessage(userMessage, chat_id, api_response, 0)
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
