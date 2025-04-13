import { Component } from '@angular/core';

@Component({
  selector: 'app-chatbot',
  //standalone: true,
  //imports: [],
  templateUrl: './chatbot.component.html',
  styleUrl: './chatbot.component.css'
})
export class ChatbotComponent {
  
  isChatbotVisible = false;
  
  messages = [
    { sender: 'bot', text: "Good evening [name], how can I help you today?" },
    { sender: 'user', text: "What events are happening this week?" },
    { sender: 'bot', text: "We’ve got a Hackathon on Friday! 🎉" }
  ];

  newMessage: string = '';



  //toggles chatbot between on and off
  toggleChatbot() {
    this.isChatbotVisible = !this.isChatbotVisible;
  }

  sendMessage(){
    //
  }

}
