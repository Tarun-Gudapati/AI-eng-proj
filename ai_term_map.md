# AI term map (one page)

## How the terms connect

```text
Basic call: prompt --> tokens --> LLM --> answer
RAG:        question --> embedding --> vector database --> best chunks --> added to prompt --> LLM
Agent:      LLM --> asks for a tool --> your code runs the tool --> result --> LLM --> repeat
MCP:        a standard plug that gives an agent its tools
LangChain:  a library that connects all these parts in code
```

## 1. Basics

| Term | Plain explanation | Example |
|---|---|---|
| AI | Software that does tasks that usually need a person: read, write, decide. | Cursor writes C# code for you. |
| Machine learning (ML) | The computer learns rules from data. A person does not write the rules. | A model learns to find fraud from old transactions. |
| Model | The file of learned numbers that makes the predictions. | Claude Sonnet is a model. |
| Parameters (weights) | The learned numbers inside a model. More parameters usually means more skill and more cost. | "A 70-billion-parameter model." |
| Training | The process that sets the weights from a very large amount of data. It is slow and expensive. | Anthropic trains Claude on text and code. |
| Inference | One use of a trained model. You send input. The model returns output. | Each Claude API call in the AI assessment is one inference. |
| Transformer | The type of neural network inside all modern LLMs. | The "T" in GPT means Transformer. |

## 2. LLM

| Term | Plain explanation | Example |
|---|---|---|
| LLM | Large language model. It predicts the next token again and again to write text. | Claude, GPT, Gemini. |
| Token | A small piece of text, about 4 characters of English. Price and limits use tokens, not words. | 1,000 tokens is about 750 words. |
| Context window | The maximum number of tokens in one call: prompt, documents, and answer together. | 200,000 tokens is about a 500-page book. |
| Prompt | The text you send to the model. | "Write 5 questions about this bank statement." |
| System prompt | Fixed instructions that set the role and the rules for each call. | "You are an underwriter. Return JSON only." |
| Temperature | A setting for randomness. Low gives the same answer each time. High gives more variety. | Use 0 to extract data from a CSV. |
| Hallucination | The model states a false fact with confidence. | The model invents a transaction that is not in the statement. |
| Reasoning model | A model that "thinks" in hidden steps before it answers. It is slower but better at hard problems. | Claude with extended thinking. |
| Multimodal | The model accepts more than text, for example images or PDFs. | You send a PDF bank statement directly. |
| Structured output | The model returns data in a fixed shape, for example JSON that matches a schema. | `{"questions": [...]}` that your C# code deserializes. |
| Prompt caching | The provider stores the repeated start of a prompt. Later calls are cheaper and faster. | Cache the long system prompt of the AI assessment. |
| Fine-tuning | Extra training on your own examples to change how the model behaves. | Train a model on 1,000 past underwriter notes. |

## 3. Knowledge: embeddings and RAG

| Term | Plain explanation | Example |
|---|---|---|
| Embedding | A list of numbers that holds the meaning of a text. Similar meanings get close numbers. | "salary" and "wages" get close embeddings. |
| Vector | The list of numbers itself. | `[0.12, -0.80, 0.33, ...]` (often 1,536 numbers) |
| Vector database | A database that finds the nearest vectors fast. | pgvector in Supabase, Pinecone, Azure AI Search. |
| Semantic search | Search by meaning, not by exact words. | "rent payments" finds "Landlord Ltd transfer". |
| Chunking | You cut long documents into small parts before you make embeddings. | Split a 40-page policy into 500-token chunks. |
| RAG | Retrieval-augmented generation. Find the relevant chunks first. Then put them in the prompt. The model answers from your data. | A chatbot that answers from a lender's loan policy. |

## 4. Action: tools and agents

| Term | Plain explanation | Example |
|---|---|---|
| Tool use (function calling) | You describe functions to the model. The model returns a request to call one. Your code runs it. | The model asks for `get_application(123)`. Your code runs the SQL query. |
| Agent | An LLM in a loop: decide, call a tool, read the result, repeat until the task is done. | Cursor Agent reads files, runs `dotnet build`, and fixes errors. |
| MCP | Model Context Protocol. A standard way to plug tools and data into any AI app, like USB for AI tools. | The GitHub or Figma MCP server in Cursor. |
| Subagent | An agent that a main agent starts for one smaller job. | Cursor starts an "explore" subagent to search the code. |
| Guardrails | Checks that stop bad input or bad output. | Block an answer that contains a full card number. |

## 5. Frameworks and operations

| Term | Plain explanation | Example |
|---|---|---|
| SDK | A client library for one provider's API. | The Anthropic Python SDK: `client.messages.create(...)`. |
| LangChain | A Python and JavaScript library with ready parts for prompts, RAG, tools, and agents. | A few lines of code make a RAG bot over PDFs. |
| LangGraph | The LangChain library for agents as a graph of steps that share state. | Loan review: extract, check, ask a person, decide. |
| LlamaIndex | A library that focuses on RAG over your documents. | Index a folder of statements, then ask questions. |
| Evals | Tests for AI output. You score answers against expected results. | 50 sample statements with the correct expected flags. |
| Rate limit | The maximum calls or tokens per minute that the provider allows. | HTTP 429 from the Claude API. |
| Latency and cost | Time and money for each call. Both increase with more tokens. | A 10,000-token prompt costs about 10 times a 1,000-token prompt. |
