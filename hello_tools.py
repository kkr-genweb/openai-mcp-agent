from openai import OpenAI

client = OpenAI()

tools = [{
    "type": "function",
    "name": "get_weather",
    "description": "Get current temperature for a given location.",
    "parameters": {
        "type": "object",
        "properties": {
            "location": {
                "type": "string",
                "description": "City and country e.g. Bogotá, Colombia"
            }
        },
        "required": [
            "location"
        ],
        "additionalProperties": False
    }
},
{"type": "web_search_preview"},
{"type": "code_interpreter",
 "container": {"type": "auto"}}
]

instructions = """
    You are a versatile researcher. When asked a math question, 
    write and run code using the python tool to answer the question. 
    If asked about the weather use the get_weather function with the right params.
    If any other question execute a web search and use the tools if needed.
    """
response = client.responses.create(
    model="gpt-4o",
    #input=[{"role": "user", "content": "What is the weather like in Deerfiled Illinois today?"}],
    #input=[{"role": "user", "content": "solve the equation 3x + 11 = 14"}],
    input=[{"role": "user", "content": "how many tennis balls fit in a gallon jug?"}],
    tools=tools,
    instructions = instructions
)

print(response.output)


