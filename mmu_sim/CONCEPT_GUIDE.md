# 🧠 MMU for Beginners: The Library Guide

If you are new to Operating Systems, don't worry! This simulation is just a game of "Moving Books."

### 1. What is an "Address"?
Think of an address like a **Coordinate**. 
- `12345` is just a way of saying: "Go to Book #48 and look at Sentence #57."

### 2. Why do we need a "Page Table"?
Your computer has a lot of "stuff" (on the Hard Drive) but very little "active space" (RAM). 
The **Page Table** is just a map. It's like a GPS that tells the computer: "That file you wanted is currently sitting in RAM slot #4."

### 3. What is a "TLB"?
The TLB is just a **Shortcut**. It remembers the last 16 things you did so you don't have to look them up in the big map every single time.

### 4. What are "FIFO" and "LRU"?
These are just "Cleaning Rules" for when your memory gets full:
- **FIFO (First-In-First-Out)**: Like a grocery store line. The oldest person (data) leaves first.
- **LRU (Least Recently Used)**: Like a messy desk. You throw away the papers you haven't touched in the longest time.

### 5. Why do we see "Page Faults"?
A Page Fault isn't an "Error"—it's just a **Wait Timer**. It means: "I don't have that data in my fast memory yet, give me a second to go get it from the slow disk."
