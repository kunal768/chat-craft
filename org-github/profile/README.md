# Chat-Craft: Domain Knowledge Based Internal Q&A Chatbot

Empower your enterprise with a customizable chatbot service that leverages your internal knowledge base to provide accurate, context-aware answers.

---

## Overview

**Chat-Craft** is a chatbot-as-a-service RAG platform built for enterprises seeking to break down knowledge silos and streamline internal information retrieval. By leveraging your organization's documents and data, Chat-Craft delivers reliable, context-aware answers using advanced Retrieval Augmented Generation (RAG) techniques.

---

## Key Features

- **Document ingestion & vectorization:** Seamlessly upload and process internal documents for instant Q&A capabilities.
- **Vector search for relevant context:** Retrieve the most pertinent information from your knowledge base for every query.
- **Structured responses via LLMs:** Ensure consistent, accurate answers with large language models fine-tuned for your data.
- **Microservices architecture:** Robust, scalable, and maintainable system design.
- **Secure & private deployment:** Keep your data safe with enterprise-grade security and deployment options.
- **Customizable UI components:** Tailor the chatbot experience to your brand and workflow.
- **Exportable iFrame Widget:** Easily embed your chatbot in any internal tool or website.

---

## System Architecture

Chat-Craft employs a modern microservices architecture, orchestrated by a central service that manages document processing, vector storage, and AI-powered responses.

**Core Services:**
- [Entities Service (Orchestrator)](https://github.com/Chat-craft/entities)
- [File AI Service](https://github.com/Chat-craft/file-ai)
- [Cron Job Service](https://github.com/Chat-craft/Cron-job)
- [UI Frontend](https://github.com/Chat-craft/ui)

**Technology Stack:**
- Next.js, Tailwind CSS, Interactive UI Components
- FastAPI for backend services
- MongoDB with Atlas Vector Search
- Ollama (local LLMs), Nomic Embed Text (embeddings), Llama 2 (response generation)

  <img src = "https://github.com/Chat-craft/.github/blob/main/system-architecture-diagram.svg" />

---

## How It Works

### Document Processing Workflow

1. **User uploads documents**
2. **File AI Service** processes and splits documents into chunks
3. **Nomic Embed Text** converts chunks into vector embeddings
4. **Embeddings stored in MongoDB** with user metadata

### Query Processing Workflow

1. **User submits a query** via the chat interface
2. Query is embedded into a vector
3. **MongoDB Atlas Vector Search** retrieves relevant document chunks
4. Chunks are sent to **Llama 2** with a structured prompt
5. **Llama 2** generates a context-aware, structured response
6. Response is displayed in the chat interface

 <img src = "https://github.com/Chat-craft/.github/blob/main/workflow.png" />

 ---


## Product Interface

- **Dashboard:** Manage your chatbot, analyze performance, and train with your documents.
- **Chatbot UI:** Interactive, user-friendly chat interface for seamless Q&A.
- **Configuration & Analytics:** Customize the system and gain insights into usage and knowledge gaps.
- **Exportable Widget:** Integrate the chatbot in your internal tools with a simple iFrame.


### Dashboard 
<img src = "https://github.com/Chat-craft/.github/blob/main/file-upload-view-dashboard.png"/>

---

## Example Use Cases

- **Internal IT or HR support**
- **Onboarding and training assistance**
- **Technical documentation Q&A**
- **Customer support knowledge base**

---

## Why Chat-Craft?

- **Empower your teams:** Fast, accurate answers reduce time spent searching for information.
- **Break down silos:** Centralize knowledge and make it accessible to everyone.
- **Customizable & secure:** Tailor the chatbot to your needs and keep your data private.

---

## Get Started

Deploy Chat-Craft in your organization and transform how your teams access knowledge!

---

