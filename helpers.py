import asyncio
import json
from typing import List, Dict, Any
from openai import AsyncOpenAI

client = AsyncOpenAI()


async def call_function_async(name, args):
    """Async version of call_function that can be run concurrently."""
    if name == "get_apartment_dataset_schema":
        return get_apartment_dataset_schema(**args)
    if name == "get_apartment_values":
        return get_apartment_values(**args)
    if name == "ask_user":
        return await ask_user(**args)
    if name == "search_keywords_in_values":
        return search_keywords_in_values(**args)
    if name == "search_by_field":
        return search_by_field(**args)
    if name == "web_search":
        return await web_search(**args)
    if name == "analyze_image":
        return await analyze_image(**args)

    return {"error": f"Function '{name}' not found"}


def call_function(name, args):
    """Synchronous wrapper for backward compatibility."""
    return asyncio.run(call_function_async(name, args))


async def search_single_question(
    question: str,
    system_prompt: str = "You are a real estate agent in New York City, searching for information about apartments in the city.",
) -> tuple[str, str]:
    """Search for a single question and return (question, answer) tuple."""
    try:
        messages = [
            {
                "role": "system",
                "content": system_prompt,
            },
            {"role": "user", "content": question},
        ]

        response = await client.chat.completions.create(
            model="gpt-4o-search-preview",
            web_search_options={},
            messages=messages,
        )

        # Extract the answer
        answer = response.choices[0].message.content
        return (question, answer)

    except Exception as e:
        return (question, "Error retrieving information: " + str(e))


async def web_search(questions: list[str]) -> dict[str, str]:
    """Web Search for any generalquestions.

    Args:
            questions: List of questions to search for

    Returns:
            Dictionary mapping questions to their answers

    """

    # Run all searches concurrently
    results_list = await asyncio.gather(*[search_single_question(q) for q in questions])

    # Convert list of tuples to dictionary
    results = dict(results_list)

    return results


def get_apartment_dataset_schema(
    filepath: str = "data/streeteasy.json",
) -> Dict[str, Any]:
    """Get the schema of the apartment dataset and an example.

    Args:
        filepath: Path to the JSON file containing apartment listings

    Returns:
        Dictionary containing the schema fields and an example apartment
    """
    with open(filepath, "r") as f:
        apartments = json.load(f)

    if not apartments:
        return {"error": "No apartments found in dataset"}

    # Get first apartment as example
    example = apartments[0]

    # Extract schema from example
    schema = {}
    for key, value in example.items():
        schema[key] = type(value).__name__

    return {"schema": schema, "example": example, "total_apartments": len(apartments)}


def get_apartment_values(filepath: str, fields: List[str]) -> Dict[str, List[Any]]:
    """Get all possible values of a list of fields for all available apartments.

    Args:
        filepath: Path to the JSON file containing apartment listings
        fields: List of field names to get values for

    Returns:
        Dictionary mapping field names to lists of unique values
    """
    with open(filepath, "r") as f:
        apartments = json.load(f)

    values = {field: set() for field in fields}

    for apartment in apartments:
        for field in fields:
            if field in apartment:
                value = apartment[field]
                # Handle nested fields
                if isinstance(value, dict):
                    values[field].add(json.dumps(value))
                elif value is not None:
                    values[field].add(value)

    # Convert sets to sorted lists
    return {field: sorted(list(vals)) for field, vals in values.items()}


async def ask_user(
    question: str,
) -> str:
    """Ask the user for more information about what they are looking for.

    Args:
        question: The question to ask the user

    Returns:
        String prompt to be used with an LLM or user interface
    """
    try:
        result = await search_single_question(question)
        return result[1]
    except Exception as e:
        return "Hmmmm i'm not sure can you decide for me?"


def search_keywords_in_values(
    filepath: str, keywords: List[str]
) -> List[Dict[str, Any]]:
    """Search for keywords in the values of the apartments list.

    Args:
        filepath: Path to the JSON file containing apartment listings
        keywords: List of keywords to search for in the values

    Returns:
        List of apartments that contain any of the keywords in their values
    """
    with open(filepath, "r") as f:
        apartments = json.load(f)

    # Convert keywords to lowercase for case-insensitive search
    keywords_lower = [kw.lower() for kw in keywords]

    results = []

    for apartment in apartments:
        # Check each value in the apartment
        for value in apartment.values():
            # Convert value to string and lowercase
            value_str = str(value).lower()

            # Check if any keyword is in this value
            if any(keyword in value_str for keyword in keywords_lower):
                results.append(apartment)
                break  # Stop checking this apartment once a match is found

    return results


def search_by_field(
    filepath: str, keywords: List[str], fields: List[str]
) -> List[Dict[str, Any]]:
    """Search for keywords in specific fields of the apartments list.

    Args:
        filepath: Path to the JSON file containing apartment listings
        keywords: List of keywords to search for
        fields: List of field names to search in

    Returns:
        List of apartments that match any of the keywords in the specified fields
    """
    with open(filepath, "r") as f:
        apartments = json.load(f)

    # Convert keywords to lowercase for case-insensitive search
    keywords_lower = [kw.lower() for kw in keywords]

    results = []

    for apartment in apartments:
        found = False

        # Search only in specified fields
        for field in fields:
            if field in apartment:
                field_value = str(apartment[field]).lower()
                if any(keyword in field_value for keyword in keywords_lower):
                    found = True
                    break

        if found:
            results.append(apartment)

    return results


async def analyze_image(
    image_url: str,
    prompt: str = "Analyze this image and describe what you see. Focus on architectural features, room layouts, lighting, and any notable characteristics that would be relevant for someone looking for an apartment.",
) -> Dict[str, Any]:
    """Analyze an image using OpenAI's vision capabilities.

    Args:
        image_url: URL of the image to analyze
        prompt: Custom prompt for image analysis (optional)

    Returns:
        Dictionary containing the analysis results and metadata
    """
    try:
        response = await client.chat.completions.create(
            model="gpt-4.1",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {"type": "image_url", "image_url": {"url": image_url}},
                    ],
                }
            ],
            max_tokens=500,
        )

        analysis = response.choices[0].message.content

        return {"analysis": analysis}

    except Exception as e:
        return {"analysis": None}
