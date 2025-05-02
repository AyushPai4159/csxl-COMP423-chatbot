import { Component, ViewChild, ElementRef, Input } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { ChatMessageResponse } from '../models.module';
import { Observable } from 'rxjs';
import { ChatbotServiceService } from './chatbot-service.service';

@Component({
  selector: 'app-chatbot',
  templateUrl: './chatbot.component.html',
  styleUrl: './chatbot.component.css'
})
export class ChatbotComponent {
  @ViewChild('messagesContainer') private messagesContainer!: ElementRef;
  @ViewChild('tempDiv') private target!: ElementRef;

  constructor(
    private http: HttpClient,
    private chatbotSVC: ChatbotServiceService
  ) {}

  isChatbotVisible = false; //main session toggle
  isSessionView = false; //sessions view toggle
  selectedSession: number = -1; // null means no session selected yet

  userName: string = '';
  newMessage: string = '';
  messages = [
    { sender: 'bot', text: 'Good evening, how can I help you today?' }
  ];

  ngOnInit() {
    this.chatbotSVC.getUserName().subscribe((name: string) => {
      this.userName = name;
      this.messages[0].text = `Good evening ${this.userName}, how can I help you today?`;
    });
    this.fetchSession();
  }

  sessions: number[] = [1];

  //toggles chatbot between on and off
  toggleChatbot() {
    this.isChatbotVisible = !this.isChatbotVisible;
    if (!this.isChatbotVisible) {
      this.isSessionView = false;
      this.selectedSession = -1;
    }
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
        .postMessage(userMessage, chat_id, api_response, this.selectedSession)
        .subscribe(
          (response: string) => {
            this.messages.push({ sender: 'bot', text: response });
            this.newMessage = '';
            this.scrollToBottom();
            this.scrollToBottom();
          },
          (error) => {
            if (error.status === 403) {
              this.messages.push({
                sender: 'bot',
                text: 'Sorry, you need to be logged in to use this feature.'
              });
            } else {
              this.messages.push({
                sender: 'bot',
                text: "Sorry, I couldn't process your request."
              });
            }
            this.scrollToBottom();
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

  //on init, fetches all sessions and messages
  fetchSession() {
    this.sessions = []; //clears sessions list
    // Fetch session IDs
    this.chatbotSVC.getAllSessions().subscribe({
      next: (response) => {
        // Populate session list (IDs only)
        this.sessions = response.map(
          (session: any, index: number) => index + 1
        );
        this.selectedSession = this.sessions[this.sessions.length - 1];
        this.chatbotSVC
          .getAllMessages(this.selectedSession)
          .subscribe((responses) => {
            responses.forEach((message) => {
              this.messages.push({ sender: 'user', text: message.user_prompt });
              this.messages.push({ sender: 'bot', text: message.api_response });
            });
          });
      },
      error: (err) => {
        console.error('Failed to fetch sessions:', err);
      }
    });
  }
  showSessions() {
    this.isSessionView = !this.isSessionView;
    this.selectedSession = -1;
    let num = Number(this.target.nativeElement.value);
    let newMessages: ChatMessageResponse[] = [];
    this.messages = [
      { sender: 'bot', text: 'Good evening [name], how can I help you today?' }
    ];

    this.chatbotSVC.getAllMessages(num).subscribe((responses) => {
      responses.forEach((message) => {
        this.messages.push({ sender: 'user', text: message.user_prompt });
        this.messages.push({ sender: 'bot', text: message.api_response });
      });
    });

    console.log(newMessages);

    console.log(this.messages);
  }

  showSessionsList() {
    // Toggle to session list view
    this.isSessionView = !this.isSessionView;
    //this.selectedSession = -1;

    // Fetch session IDs
    this.chatbotSVC.getAllSessions().subscribe({
      next: (response) => {
        // Populate session list (IDs only)
        this.sessions = response.map(
          (session: any, index: number) => index + 1
        );
      },
      error: (err) => {
        console.error('Failed to fetch sessions:', err);
      }
    });
  }

  openSession(sessionId: any) {
    this.selectedSession = sessionId;
    this.messages = [{ sender: 'bot', text: `Opening Session ${sessionId}` }];

    this.chatbotSVC.getAllMessages(sessionId).subscribe({
      next: (responses) => {
        responses.forEach((message) => {
          this.messages.push({ sender: 'user', text: message.user_prompt });
          this.messages.push({ sender: 'bot', text: message.api_response });
        });
        this.scrollToBottom();
      },
      error: (err) => {
        console.error(`Failed to load messages for session ${sessionId}:`, err);
      }
    });
    this.showHome();
  }

  backToSessionList() {
    this.selectedSession = -1;
  }

  backToChat() {
    this.isSessionView = false;
    this.selectedSession = -1;
  }

  resetSession() {
    //saves current session and resets chat window
    //implement saving later
    this.messages = [
      { sender: 'bot', text: 'Good evening [name], how can I help you today?' }
    ];

    this.http
      .delete<any>(`/api/chatbot/admin/session/${this.selectedSession}`)
      .subscribe(
        (response: string) => {
          console.log('Session reset:', response);
        },
        (error) => {
          console.error('Error:', error);
        }
      );
  }

  toggleSessionView() {
    this.isSessionView = !this.isSessionView;
  }

  showHome() {
    this.isChatbotVisible = true;
    this.isSessionView = false;
    console.log(this.messages);
  }
}
