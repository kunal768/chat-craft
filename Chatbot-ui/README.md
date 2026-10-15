# Chat‑Craft UI – Chatbot Front‑End

![Chat‑Craft](https://img.shields.io/badge/Chat--Craft-CaaS-blue?style=flat-square)  ![License](https://img.shields.io/badge/license-MIT-green?style=flat-square)

> **Chat‑Craft** is a *Chatbot‑as‑a‑Service (CaaS)* platform that bridges the information gap inside organisations by delivering secure, scalable and intelligent Retrieval‑Augmented Generation (RAG) over internal knowledge bases. This repository hosts the **front‑end chatbot UI** and the **iframe export** that lets you embed a fully‑featured conversational assistant into any page with a single HTML tag.

---

## ✨ Key Features

| Feature                            | Description                                                                                                    |
| ---------------------------------- | -------------------------------------------------------------------------------------------------------------- |
| **Conversational UI**              | React‑based chat experience with rich‑text, code and markdown rendering.                                       |
| **Retrieval‑Augmented Generation** | Combines semantic search with LLMs to provide context‑aware answers from your documents.                       |
| **Secure, Org‑Scoped Data Access** | All queries are scoped to your company’s index; no data leaves your tenancy.                                   |
| **Plug‑and‑Play Embed**            | Drop an `<iframe>` tag anywhere (Confluence, Notion, intranet, external site) to bring Chat‑Craft to the user. |                                              

---

## 🛠 Tech Stack

* **React 18** with **TypeScript**
* **Vite** build tooling
* **Tailwind CSS** for utility‑first styling
* **Headless UI** + **Radix Primitives** for accessibility

> *This repo focuses solely on the client. The backend (vector storage, LLM orchestration, auth) lives in `Chat‑Craft/server`.*

---

## 🚀 Getting Started

### Prerequisites

|  Tool       | Version                        |
| ----------- | ------------------------------ |
| **Node.js** | ≥ 18 .x                        |
| **npm**     | ≥ 9 .x (or **pnpm**/ **yarn**) |

### Installation

```bash
# 1 — Clone the repo
$ git clone https://github.com/your‑org/chat‑craft‑ui.git
$ cd chat‑craft‑ui

# 2 — Install dependencies
$ npm install

# 3 — Configure env variables
$ cp .env.example .env
$ $EDITOR .env  # fill VITE_API_URL, VITE_AUTH_TOKEN, etc.

# 4 — Run locally
$ npm run dev

# 5 — Build for production
$ npm run build && npm run preview
```

---

## 📦 Embedding the Chatbot

The build pipeline produces a **zero‑dependency iframe bundle** located in `dist/embed`. To drop the chatbot into any web page, copy‑paste the snippet below:

```html
<!-- Chat‑Craft Embed -->
<iframe
  src="https://cdn.your‑org.com/chat‑craft/embed.html?orgId=ACME&theme=dark"
  title="Chat‑Craft Assistant"
  style="width:100%; height:680px; border:none; border-radius:12px; overflow:hidden;"
  loading="lazy"
  referrerpolicy="no-referrer"
></iframe>
```

| Query Param | Purpose                                                 |
| ----------- | ------------------------------------------------------- |
| `orgId`     | Matches the tenant in the backend (required)            |
| `userId`    | Pre‑fills the session with SSO identity (optional)      |
| `theme`     | `light`, `dark` or a custom CSS‑vars palette (optional) |
| `lang`      | UI locale (e.g. `en`, `fr`, `ja`)                       |

> Need fine‑grained control? Import `@chat‑craft/sdk` instead and mount the `<ChatCraftProvider>` directly in your SPA.

---


## 🧑‍💻 Contributing

1. Fork the project
2. Create your feature branch (`git checkout -b feat/amazing‑feature`)
3. Commit your changes (`git commit -am 'feat: add amazing feature'`)
4. Push to the branch (`git push origin feat/amazing‑feature`)
5. Open a Pull Request

All PRs require at least one approval and a passing CI.

---

## 📣 Acknowledgements

* [OpenAI API](https://openai.com)
* [LangChain](https://github.com/langchain-ai)
* \[Vector DB of your choice] – Pinecone, Weaviate, Qdrant…
* [Vercel](https://vercel.com) for CDN‑edge hosting

> Have questions or feedback? Reach us at **support\@chat‑craft.io** or open an issue.


