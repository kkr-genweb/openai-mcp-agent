# Supply‑Chain Copilot Demo
Derived from [Building a Supply-Chain Copilot with OpenAI Agent SDK and Databricks MCP Servers, July 8, 2025](https://cookbook.openai.com/examples/mcp/mcp_tool_guide)
This repo demonstrates using the **Model Context Protocol (MCP)** tool via the OpenAI Responses API to build an agent that fetches external data, combines it with model reasoning and analysis tools, and produces insights.

## 💡 Overview
Traditional function calling requires multiple back‑and‑forth trips between model → backend → external API, which adds latency and complexity. With the **hosted MCP tool**, the model communicates directly with remote MCP servers, dramatically simplifying workflows and reducing token & network overhead  .

In this demo, we:
1. **Fetch competitor pricing** from remote MCP servers.
2. **Web‑search alternative vendor prices**.
3. **Analyze internal sales data** using Code Interpreter.
4. **Generate a consolidated pricing gap report**.

## Use Cases Enabled
|**Domain**|**Example Workflow**|
|---|---|
|E‑commerce|Add to cart + generate Stripe checkout in one turn|
|Dev‑ops|Fetch Sentry error → open GitHub issue|
|Notifications|Retrieve headlines → send Twilio text|

These were formerly multi-step glue code processes. With MCP, it’s streamlined.


## 🔧 How MCP Works
1. **Declare MCP server** in your tools array. The Responses runtime auto-detects transport (HTTP/HTTP‑SSE).
2. **Import tool list** from tools/list. Controlled via allowed_tools, caching the list to avoid repeated retrievals  .
3. **Model invokes tools** via mcp_tool_call. By default, calls pause for approval—can disable with "require_approval": "never".

Remote tool access is now _first-class_, eliminating backend orchestration.

## 🚀 Best Practices
1. **Filter with allowed_tools** to limit tool payload and reduce context bloat  .
2. **Cache tool listings** via mcp_list_tools or by including previous_response_id for follow-ups.
3. **Reserve reasoning models** for complex tasks to avoid excessive token use; use lighter models for tool calls  .
4. **Combine MCP** with tools like web_search_preview and code_interpreter for rich, end‑to‑end pipelines.

## 🧵 Demo Flow

### **1. Setup Tools Block**
```
"tools": [
  {
    "type": "mcp",
    "server_url": "https://www.aloyoga.com/api/mcp",
    "server_label": "aloyoga",
    "allowed_tools": ["search_shop_catalog","get_product_details"],
    "require_approval": "never"
  },
  {
    "type": "web_search_preview",
    "user_location": { "type":"approximate","country":"US" },
    "search_context_size": "medium"
  },
  {
    "type": "code_interpreter",
    "container": { "type":"auto", "file_ids": ["<uploaded‑sales‑CSV‑ID>"] }
  }
]
```
### **2. System Prompt**
Describe tasks:
- Use MCP server for Alo Yoga pricing.
- Use web search for Uniqlo pricing.
- Analyze sales CSV via code interpreter.
- Report pricing gaps ≥15%.

### **3. Sample MCP & Search Flow**
```
assistant → model:
{"name":"aloyoga.search_shop_catalog","arguments":{...}}
{"name":"web_search_preview.fetch","arguments":{...}}
```

### **4. Analysis & Reporting**
- Code Interpreter ingests CSV → calculates pricing gaps.
- Model compiles price‑gap report, flags outliers.

### **5. Typical Output**
```
#### Pricing Comparison Report

Revenue:
- Shorts: $6,060
- Tank tops: $6,150
- Yoga pants: $12,210

Flags (≥15% gap):
- Shorts: ‑31.8% vs Alo, +100.7% vs Uniqlo
- Tank tops: … etc.
```

## **✅ Usage Tips**
- 📌 **Limit search results** — instruct model to return 4 items max before asking for extension.
- 🎯 **Clarify missing params** (e.g. size/color) before invoking MCP.
- 📚 **Few-shot examples** in system prompt help model pick right tools & stop early  .

E.g.:
```
If user: “Tree Runner, blue, size 10”
Assistant:
{"name":"allbirds.search_shop_catalog", "arguments":{"query":"Tree Runner","context":"blue size 10"}}
```

## **✅ Summary**
Using the hosted MCP tool transforms complex multi‑step pipelines into succinct, agentic workflows:
1. Direct remote tool invocation
2. Token & latency savings via cached tool definitions
3. Composable with web search, interpreter, and custom tools
4. Outcome: clean, fully‑automated, multi‑service agents 