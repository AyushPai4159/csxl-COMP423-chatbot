import { Component, ViewChild, ElementRef, Input } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { frontendChatbotService } from './chatbot-services';
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
    private service: frontendChatbotService
  ) {}

  isChatbotVisible = false; //main session toggle
  isSessionView = false; //sessions view toggle
  selectedSession: number = -1; // null means no session selected yet

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

  sessions: number[] = [1];

  public ngOnInit(): void {
    this.fetchSession();
  }

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
            console.error('Error:', error);
            this.messages.push({
              sender: 'bot',
              text: "Sorry, I couldn't process your request."
            });
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
    this.service.getAllSessions().subscribe({
      next: (response) => {
        // Populate session list (IDs only)
        this.sessions = response.map(
          (session: any, index: number) => index + 1
        );
        this.selectedSession = this.sessions[this.sessions.length - 1];
        this.service
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

    this.service.getAllMessages(num).subscribe((responses) => {
      responses.forEach((message) => {
        this.messages.push({ sender: 'user', text: message.user_prompt });
        this.messages.push({ sender: 'bot', text: message.api_response });
      });
    });

    console.log(newMessages);

    console.log(this.messages);
  }

  // showAndGetSessions() {
  //   let temp = 0;
  //   try {
  //     this.service.getAllSessions().subscribe((response) => {
  //       this.sessions = response;
  //       temp = this.sessions[this.sessions.length - 1];
  //       console.log(temp);
  //       this.service.getAllMessages(temp).subscribe((responses) => {
  //         responses.forEach((message) => {
  //           this.messages.push({ sender: 'user', text: message.user_prompt });
  //           this.messages.push({ sender: 'bot', text: message.api_response });
  //         });
  //       });
  //     });

  //     console.log(this.messages);
  //   } catch (Error) {}
  // }

  showSessionsList() {
    // Toggle to session list view
    this.isSessionView = !this.isSessionView;
    //this.selectedSession = -1;

    // Fetch session IDs
    this.service.getAllSessions().subscribe({
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

    this.service.getAllMessages(sessionId).subscribe({
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

  // Hardcoded past sessions
  // sessions = [
  //   {
  //     id: 1,
  //     title: 'Session with Support Bot',
  //     conversation: [
  //       { sender: 'bot', text: 'Hello! How can I assist you today?' },
  //       { sender: 'user', text: 'I need help with my order.' },
  //       { sender: 'bot', text: 'Sure, can you provide your order ID?' }
  //     ]
  //   },
  //   {
  //     id: 2,
  //     title: 'Technical Help',
  //     conversation: [
  //       { sender: 'bot', text: 'Welcome to tech support!' },
  //       { sender: 'user', text: 'My app keeps crashing.' },
  //     ]
  //   }
  // ];

  showHome() {
    this.isChatbotVisible = true;
    this.isSessionView = false;
    console.log(this.messages);
  }
}
