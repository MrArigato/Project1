Accio TCP Client Project
Introduction
This README documents the challenges faced and solutions found during the development of the Accio TCP client, a simple application for connecting to a TCP server and transferring files.

Challenges and Solutions
1. Understanding TCP Sockets
Problem: Initially, I had a basic understanding of TCP sockets and their operations. Implementing the connect, send, and receive functionalities was challenging.
Solution: I spent time reviewing the Python socket module documentation and experimenting with sample codes. This hands-on approach helped me grasp the concepts better.

2. Implementing the Protocol Correctly
Problem: Ensuring that the client correctly followed the specified protocol (sending and receiving specific commands) was tricky. I struggled to correctly implement the logic to wait for the accio command before sending confirmations.
Solution: After several trial and error attempts, I used a while loop to continuously receive data until the expected command was complete. This approach proved effective in handling partial data receptions.

Acknowledgements
While developing this project, I referred to several online resources to strengthen my understanding of Python's socket programming and TCP/IP concepts. Some of the key resources include:
Python Socket Programming Tutorial
GeeksforGeeks Python Socket Programming
These tutorials were instrumental in helping me understand the basics and provided code snippets that I adapted for my project.
Conclusion
This project was a valuable learning experience in network programming. Although there were challenges along the way, each problem presented an opportunity to learn and improve my coding skills.