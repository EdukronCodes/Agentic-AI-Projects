# Customer Support Agent — Architecture and Frontend Integration

## 1. Project summary

This subproject implements a multi-agent customer support RAG system with a FastAPI backend and two new frontend integrations:
- `frontend/vue-app`: Vue 3 + Vite app
- `frontend/next-app`: Next.js (App Router) app

The backend is provided in `app/api/api.py` and orchestrated in `app/graph/orchestrator.py`.

## 2. Backend architecture

### 2.1 API
- `GET /health` -> health check
- `POST /chat` -> accepts JSON `{ "query": "..." }` and returns:
  - `query` (string)
  - `agent` (resolved agent key)
  - `answer` (generated text)
  - `confidence` (float)
  - `metadata` (router, context, history)

### 2.2 Orchestrator (`app.graph.orchestrator.LangGraphOrchestrator`)

- `self.agents` map: agent name -> specialized agent instance (FAQ, billing, returns, etc.)
- `self.router = RouterAgent(self.agents)` decides which domain agent to call
- falling back to `escalation_agent` for unknown or exceptions
- `self.rag` loads `RAGPipeline` to enrich context with embedded knowledge from `data/*.json`
- stores up to 50 history entries in `self.history`

### 2.3 Specialized agents
- in `app/agents/specialized_agents.py` (domain-specific business rules)
- all implement `handle(query, context_data)` and return:
  - `answer`, `confidence`, `agent`, `reason`

### 2.4 Data
- `data/faqs.json`, `data/orders.json`, `data/policies.json`
- FAISS index under `data/faiss_index/index.faiss`

## 3. New frontend integration

### 3.1 Shared design pattern

Both frontends use exactly the same endpoint through CORS/proxy:
- internal request: `POST /api/chat` -> backend `POST /chat`

The backend already allows CORS from any origin (`allow_origins=["*"]`) in `app/api/api.py`.

### 3.2 Vue frontend
- path: `customer_support_agent/frontend/vue-app`
- main files:
  - `src/App.vue`: UI, query input, fetch logic
  - `vite.config.js`: `/api` proxy to backend at `http://localhost:8000`

#### Usage
1. `cd customer_support_agent/frontend/vue-app`
2. `npm install`
3. `npm run dev` (port `5173`)
4. Type question, click `Send`

### 3.3 Next.js frontend
- path: `customer_support_agent/frontend/next-app`
- main files:
  - `app/page.js`: client component with state and `fetch('/api/chat')`
  - `next.config.js`: rewrites `/api/:path*` -> `http://localhost:8000/:path*`

#### Usage
1. `cd customer_support_agent/frontend/next-app`
2. `npm install`
3. `npm run dev` (port `3000`)
4. Type question, click `Send`

## 4. End-to-end run steps

1. Start backend:
   ```bash
   cd customer_support_agent
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   export OPENAI_API_KEY=...  # or config/.env
   python main.py
   ```

2. In another terminal, run one frontend:
   - Vue:
     ```bash
     cd customer_support_agent/frontend/vue-app
     npm install
     npm run dev
     ```
   - Next:
     ```bash
     cd customer_support_agent/frontend/next-app
     npm install
     npm run dev
     ```

3. Confirm health:
   ```bash
   curl http://localhost:8000/health
   ```

4. Confirm chat pipeline:
   ```bash
   curl -X POST 'http://localhost:8000/chat' -H 'Content-Type: application/json' -d '{"query":"What is your return policy?"}'
   ```

## 5. System flow diagram

```mermaid
flowchart TD
  A(User) -->|input text| B(Vue or Next frontend)
  B -->|POST /api/chat| C[Frontend proxy (Vite/Next)]
  C -->|POST /chat| D[FastAPI backend]
  D -->|orchestrator.run(query)| E[RouterAgent -> Selected Agent]
  E -->|calls| F[Specialized Agent(s)]
  F -->|response| D
  D -->|ChatResponse| C
  C -->|output| B
  B --> A

  subgraph BackEnd[Backend Components]
    D
    E
    F
  end

  subgraph Data[Knowledge Base]
    G[data/faqs.json]
    H[data/orders.json]
    I[data/policies.json]
    J[data/faiss_index/index.faiss]
  end

  D --> G
  D --> H
  D --> I
  D --> J
```

## 6. Detailed connection map

- `frontend/*` -> `POST /api/chat` (same shape as backend `/chat`)
- `app/api/api.py` -> orchestrator.run -> `app/graph/orchestrator.py`
- orchestrator loads `RAGPipeline` from `app/rag/rag_pipeline.py` to fetch context and agent router result
- router chooses one of `app/agents/specialized_agents.py`
- specialized agent returns structured response, set enforcement (`answer`, `confidence`)

## 7. Validation checklist

- [x] Backend health endpoint returns `status: ok`
- [x] Chat endpoint responds for sample query
- [x] Vue app runs at http://localhost:5173 and shows response
- [x] Next app runs at http://localhost:3000 and shows response

## 8. Notes and next improvements

- Add authentication between frontend and backend (JWT / OAuth)
- Add WebSocket for streaming and multi-turn behavior
- Add test scripts for UI end-to-end (Cypress / Playwright)
- Add `docker-compose` with backend + both frontends
