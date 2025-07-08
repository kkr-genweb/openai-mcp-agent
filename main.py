"""
pricing_agent_demo.py

This script partially replicates the example:
https://cookbook.openai.com/examples/mcp/mcp_tool_guide

- Uses MCP to fetch Alo Yoga prices
- Uses Web Search for Uniqlo prices
- Uses Code Interpreter to analyze price differences

Requirements:
- Set OPENAI_API_KEY as an environment variable.
"""

import os
from openai import OpenAI

# -------------------------------------------------------
# CONFIGURATION
# -------------------------------------------------------

# Load API key from environment variable
client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

# System prompt (same as your provided multi-step instructions)
instructions = """You are a pricing analyst for my clothing company. Please use the MCP tool 
to fetch prices from the Alo Yoga MCP server for the categories of women's 
shorts, yoga pants, and tank tops. Use only the MCP server for Alo yoga data, don't search the web. 

Next, use the web search tool to search for Uniqlo prices for women's shorts, yoga pants, and tank tops. 

In each case for Alo Yoga and Uniqlo, extract the
price for the top result in each category. Also provide the full URLs
 
Using products where the price difference exceeds 20%. 
Create and output a short report including the findings.

# Steps

1. **Fetch Alo Yoga Prices:**
   - Use the Alo Yoga MCP server to fetch prices for the following products:
High-Waist Airlift Legging
Sway Bra Tank
 5" Airlift Energy Short

- Ensure you find prices for each. 
- Extract the price of the top result for each category.
- include  URL links 


2. **Query Uniqlo Prices:**
   - Use the Web-Search tool to search non-sale prices for the following Uniqlo products: 
Women's AIRism Soft Biker Shorts
Women's AIRism Soft Leggings
Women's AIRism Bra Sleeveless Top
- Ensure you find non-sale prices for each. 
- Extract the price for the top result in each category.
- include  URL links 

3. **Sales Data Analysis:**
   - For each SKU, use the python code interpreter to compute the percentage price gap between the Uniqlo and Alo Yoga prices.
   - Flag products priced 20% or more apart

4. **Report:**
   - Compile and output a report including the flagging results

# Output Format
- A short text report explaining:
  - Any products that are priced ≥ 20% apart with specific details.
"""

# -------------------------------------------------------
# TOOL CONFIGURATION
# -------------------------------------------------------

TOOLS = [
    {
        "type": "web_search_preview",
        "user_location": {
            "type": "approximate",
            "country": "US"
        },
        "search_context_size": "medium"
    },
    {"type": "code_interpreter",
    "container": {"type": "auto"}},
    {
        "type": "mcp",
        "server_url": "https://www.aloyoga.com/api/mcp",
        "server_label": "aloyoga",
        "allowed_tools": [
            "search_shop_catalog",
            "get_product_details"
        ],
        "require_approval": "never"
    }
]

# -------------------------------------------------------
# RUN AGENT
# -------------------------------------------------------

response = client.responses.create(
    model="gpt-4o",
    input=[{"role": "user", "content": "Please execute the analysis and share the final report."}],
    tools=TOOLS,
    instructions = instructions
)

# -------------------------------------------------------
# PRINT OUTPUT
# -------------------------------------------------------

print("\n=== PRICING GAP ANALYSIS REPORT ===\n")
print(response.output_text)