LLMs are better at focused, more specific tasks

they have the tendency to lose context and drift away over time
For example, if there is a specific service we are trying to provide to the user, and we task the one agent with gathering all of the info and callling of the tools, after 10 or so turns, the agent starts to lose context, drift away, and cannot effectively "finish" the flow

The modern solution to this is using multiple agents, each focused on a specific task, and connecting them into a graph. Then, depending on the service we're trying to provide to the customer, we can build the graph in such a way to reflect this.

In this case, the service would be:

Our goal is to build a chatbot that can help with lead generation and cold email outreach. For example, job hunting or sales

1. look through public databases of companies and find ones that best mach user's criteria
2. use the context about the company + info form the user to draft a perfect cold email

Hence, in this proposed architechture, we use several different agents via langgraph

1. Main Assistant
   -> talks to user in the beggining, asks for their criteria, and call the retriever (RAG) tool
2. Evaluator Assistant
   -> talks to user to see if the user is happy with the

Main assistant, after making the retriever (RAG) tool call, passes the conversation down to the evaluator assistant. Evaluator assistant makes sure the user is happy with the choice, and if they are, can then make the call to the generate_cold_opener tool, which is an LLM in its own as well.

Meanwhile, we use a state graph, and in our state, besides messages, we also store which assistant (agent) user was talking to last, and when a new messages comes in from the user, we drop them right into the conversation with the right bot

As this project evolves, I will be splitting each task even further down into more agents, so that each agent can be great at their specific task. More importantly, this setup avoids

It is important to understand that one full run of the graph represents one message from the user (one HumanMessage). So the graph should always go from HumanMessage -> End. Alternative design pattern would be to pause the execution of the graph midway through when we need user's input, insert that into the graph, adn resume.

However, I do not like this design pattern as it makes it really difficult to understant where you are in the graph at any point of time. Hence, in this design, we're never pausing exeuction, but instead, design the graph such that 1 human mesage = 1 full run of the graph, with the last message usually being an AI message. An important consequence of this is that ToolMessage (from a tool) or a AIMessage with a tool all will NEVER be the last message.

To get this to run, dont forget to export your openai and anthropic keys into the env
