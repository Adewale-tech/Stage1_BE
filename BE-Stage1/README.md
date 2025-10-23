# Stage 1 - String Analyzer API

## Setup Instructions
1. Clone the repo
2. Create a virtual environment
3. Install dependencies:


# 🚀 Stage 1 Backend Task — FastAPI String Analysis API

## 📘 Overview

This project is part of the **Backend Developer Internship Stage 1** task.  
The goal is to build and deploy a **FastAPI-based REST API** that performs **string analysis** operations and stores data persistently using a local JSON file.

---

## 🎯 Objectives

By completing this project, I achieved the following objectives:

- ✅ Designed and implemented a REST API using **FastAPI**  
- ✅ Created a `/strings` endpoint that analyzes input strings for different properties  
- ✅ Implemented **CRUD operations** to create, retrieve, list, and delete analyzed strings  
- ✅ Stored analyzed string data persistently in a local `data.json` file  
- ✅ Added query filters to search strings by attributes like palindrome, length, and characters  
- ✅ Deployed the project successfully to **Render** as a live backend API

---

## 🧠 Features

### 1. Analyze and Save Strings
- Accepts a string input
- Calculates multiple properties:
  - Length
  - Palindrome check
  - Unique character count
  - Word count
  - Character frequency map
  - SHA-256 hash
- Saves the result in `data.json`

### 2. Retrieve a String by Value
- Fetches a single analyzed string from the stored data by its value

### 3. List All Strings
- Returns all analyzed strings
- Supports **filtering** based on:
  - `is_palindrome`
  - `min_length`
  - `max_length`
  - `word_count`
  - `contains_character`

### 4. Delete a String
- Deletes a string record by its value

---

## ⚙️ Endpoints

| Method | Endpoint | Description |
|--------|-----------|-------------|
| **POST** | `/strings` | Analyze and store a string |
| **GET** | `/strings` | Retrieve all analyzed strings (with optional filters) |
| **GET** | `/strings/{string_value}` | Retrieve details of a specific string |
| **DELETE** | `/strings/{string_value}` | Delete a string from storage |

---

## 🧩 Example Requests

### 🔹 POST `/strings`
**Request:**
```bash
curl -X POST "https://be-stage1.onrender.com/strings" \
-H "Content-Type: application/json" \
-d "{\"value\": \"madam\"}"
