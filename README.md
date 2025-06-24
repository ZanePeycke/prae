# prae
Production Ready Agent Engineering

## W1
## Task: Personalized broker to find apartments in New York City
- Agent has access to tools and personal details to find the best apartment for each person.
- Agent can parse listing and go beyond StreetEasy filters, better understand the renter through large amounts of text, images, etc. (eventually could proactively reach out to schedule viewings)
- Reward function is if the person want's to schedule a viewing (determined by LLM as a judge with personal info for the time being)


## Details
- Chat completions API with 4.1 or sonnet for the main model
    - 4o for parsing images, openai web search 
- Tools:
    - Apartment Text search
    - Analyze apartment images
    - Explore neighborhood
    - Map directions
- Outcomes:
    - Recommend apartment(s)
    - Do nothing


## What I would like to improve on
- Better file search: Should gather more data and consider organizing it by neighborhood, provide more context on the schema
- Better search by keywords (a budget of 4000 should include listings less than 4k but now fails because i'im comparing on ints)
- Larger apartment dataset for testing
- Analyze tool usage
- Re add [Open Street Map MCP](https://github.com/jagan-shanmugam/open-streetmap-mcp) for better directions and explorations
- Error handling on context window limits for Claude
- Larger Test Set + Cl