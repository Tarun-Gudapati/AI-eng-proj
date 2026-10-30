# AI engineer interview: questions and answers

How to use this: cover the answer, say yours out loud, then compare.
Short answers first; interviewers ask the follow-up, so learn that too.

---

## Basics

**1. What is a token, and why should you care?**
A token is a piece of text, often part of a word. In English, 1,000 tokens is about 750 words,
so there are **more tokens than words**. You pay per token (input and output), the context window
is counted in tokens, and more tokens means slower responses.
*Follow-up: why does a CSV of numbers cost more than you expect?* Digits, commas and dates split into many small tokens.

**2. What is the context window?**
The maximum number of tokens the model can handle in one request: your input plus its output.
Bigger isn't free. Cost and latency grow, and models can miss details buried in the middle of a very long prompt.

**3. What does temperature do?**
It controls randomness. Use low for classification and extraction, where you want the same answer every time.
Use higher for creative writing.

**4. What is a hallucination, and how do you reduce it?**
A confident answer that is wrong or made up. To reduce it:
- give the model the facts in the prompt (RAG, or the documents directly)
- ask for citations
- allow "I don't know"
- check the output with code
- measure it with evals

---

## Prompts and outputs

**5. How do you get reliable JSON out of a model?**
- Give it a clear schema.
- Use the provider's structured-output or tool feature if there is one.
- **Validate** the result in code (Pydantic, or a C# model).
- If it fails, retry once with the error, or fall back gracefully.

Never trust the JSON blindly.
*Your work example:* the answer comes between markers, each line is parsed as JSON, and a line that
doesn't parse becomes a plain-text question instead of crashing the run.

**6. What is prompt caching?**
The provider stores a repeated **start** of the prompt (system prompt, policy text). Later calls
that start the same way reuse it, so they're cheaper and faster. Put stable content first and the per-request data last.
*Your work example:* the system prompt and the credit policy are cached; each application's data goes in the user message.

**7. Why would you send a whole document instead of using RAG?**
If it's small enough to fit and doesn't change often, sending it whole is simpler, and there is
**no retrieval step that can miss the right section**. Caching makes the repeated cost small.
Switch to RAG when the documents get too big, change often, or you need to search many of them.

---

## RAG

**8. What is RAG? Walk me through it.**
Retrieval-augmented generation: find the relevant parts of your documents, put them in the prompt,
and have the model answer from them.
- **Offline:** load the documents, split them into chunks, make an embedding for each chunk, store them in a vector database.
- **Per question:** embed the question, search for the closest chunks (top-k), optionally rerank them,
  build the prompt with those chunks, and answer with citations.

It's a **one-pass pipeline**: retrieve once, answer once.

**9. What is an embedding?**
A list of numbers that represents the meaning of a piece of text. Texts with similar meanings get
vectors that are close together, measured with cosine similarity. That's what makes "search by meaning" possible.

**10. How do you choose a chunk size?**
Too small and a chunk loses its context. Too big and the relevant sentence gets diluted, and you waste tokens.
Start by splitting on the document's structure (sections, headings) with a little overlap.
Then **measure** retrieval hit rate on test questions and adjust.

**11. Keyword, semantic or hybrid search?**
- **Keyword search** finds exact terms: IDs, product codes, names.
- **Semantic search** finds meaning: "income" matches "salary".
- **Hybrid** combines both. It's often the best choice for finance documents full of codes and jargon.

**12. RAG or fine-tuning?**
- Use **RAG** for knowledge that changes, or when you need citations.
- Use **fine-tuning** to change behaviour, style or format. It doesn't add up-to-date facts.
- Most apps should try prompting, then RAG, before fine-tuning.

---

## Agents and tools

**13. What's the difference between an agent and a pipeline?**
- A **pipeline** is fixed steps that your code decides, run in one pass.
- An **agent** is a **loop**: the model decides the next step, calls a tool, looks at the result, and repeats until it's done.

Use a pipeline when the steps are known: it's cheaper, faster and predictable.
Use an agent when the path depends on what it finds.
*Your work example:* the AI assessment is a pipeline, not an agent.

**14. How does tool calling work?**
You describe functions to the model (name, description, parameter schema). The model replies with
"call this tool with these arguments". **Your code** runs the function and sends the result back,
and the model continues. The model never runs code itself.

**15. What is MCP?**
Model Context Protocol, an open standard for connecting AI apps to tools and data.
- An **MCP server** offers tools, resources and prompts.
- A **host** (Cursor, Claude Desktop, your app) connects to it through an MCP **client**.

Write the server once, and any MCP host can use it. Think of it as a USB-C port for tools.

**16. How do you stop an agent from running forever or doing damage?**
- a maximum number of steps, and timeouts
- tools with the fewest permissions they need
- human approval before any important action (payments, writes)
- a log line for every step, so you can see what it did

---

## Evals and quality

**17. How do you know your LLM feature works?**
Build a **labelled test set** (a golden set), run the feature on it, and measure it:
- accuracy, for classification
- retrieval hit rate and faithfulness, for RAG

Re-run it every time you change the prompt or the model. In production, use real signals such as
user or assessor corrections. "It looked fine on 3 examples" is not an eval.

**18. What is LLM-as-a-judge, and what's the risk?**
Using a model to grade another model's output, for open-ended answers. The judge can be biased
(it likes longer answers, or its own style), so give it a clear rubric with yes/no criteria,
and check it against human labels on a sample.

---

## Safety and production

**19. What is prompt injection, and how do you defend against it?**
Untrusted text in the prompt that contains instructions, such as "ignore your rules and...".
It can come from user input, documents or transaction descriptions. To defend:
- mark data clearly as data, separate from instructions
- give tools the fewest permissions they need
- validate outputs in code
- never let model output trigger writes without checks or a human

**20. What are guardrails?**
Deterministic checks around the model:
- input filters
- output schema validation
- business rules that **override** the model
- fallbacks when it fails

*Your work example:* code rules in the categoriser always win over what the model proposed.

**21. How do you handle rate limits and outages from the AI provider?**
- Retry 429 (rate limited), 529 (overloaded) and 5xx errors with **exponential backoff plus jitter**, with a cap on retries.
- Respect `retry-after`.
- Never retry a 400, because your request is wrong and will fail again.
- For heavy load, put the work on a queue. Consider a fallback model.

**22. How do you reduce cost and latency?**
- route easy tasks to a smaller model
- use prompt caching
- send compact input (CSV instead of verbose JSON)
- cap the output tokens
- run calls in parallel, with a limit
- stream the output, so the user sees progress
- cache results you've already computed

**23. Why run LLM calls in the background, and what's the catch?**
They're slow and can fail, so the user's request shouldn't wait for them, and a failure shouldn't
break the main feature. The catch with a plain `Task.Run` is that the work lives only in memory.
If the app restarts, it's lost, and there's no automatic retry. A **queue** (database table plus worker,
or Service Bus) survives restarts and gives you retries and visibility.

---

## About your own work

**24. "What would you do better?" (have this ready)**
- Add **evals**, so quality is measured rather than guessed.
- Move secrets into Key Vault.
- Run the AI work from a **durable queue** instead of in-memory background tasks.
- Track **cost per run**.
- Harden against prompt injection, because client answers and transaction text are untrusted input.

**25. Tell me about the AI feature you built (2 minutes)**
Use this shape:
1. **Problem:** what hurt before.
2. **What I built:** one sentence.
3. **One hard decision and why:** the trade-off.
4. **Result:** a number.
5. **What I'd do better.**
