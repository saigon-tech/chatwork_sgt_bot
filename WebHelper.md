# WebHelper Class Documentation

The `WebHelper` class provides utilities for fetching web content and interacting with an AI model. It is designed to
simplify web scraping tasks and integrate AI-powered text generation.

## Class Initialization

```python
from src.utils.web_utils import WebHelper

web_helper = WebHelper()
```

When initialized, the `WebHelper` class creates an instance of `OpenAIHelper` for AI-related operations.

## Methods

### `fetch_url_html(url: str) -> str`

Fetches the full HTML content from a given URL.

**Parameters:**

- `url` (str): The URL to fetch content from

**Returns:**

- str: Raw HTML content of the webpage

**Usage Example:**

```python
web_helper = WebHelper()
url = "https://example.com"
html_content = web_helper.fetch_url_html(url)
print(f"HTML content length: {len(html_content)} characters")
```

**Note:** This method is useful when you need to process the raw HTML yourself or pass it to another function for
further parsing.

### `fetch_url_text(url: str, max_chars: int = None) -> str`

Fetches and extracts text content from a given URL, removing HTML tags and scripts.

**Parameters:**

- `url` (str): The URL to fetch content from
- `max_chars` (int, optional): Maximum number of characters to extract. If None, returns all extracted text.

**Returns:**

- str: Extracted text content

**Usage Example:**

```python
web_helper = WebHelper()
url = "https://en.wikipedia.org/wiki/Python_(programming_language)"
full_text = web_helper.fetch_url_text(url)
print(f"Full text length: {len(full_text)} characters")

limited_text = web_helper.fetch_url_text(url, max_chars=1000)
print(f"Limited text: {limited_text[:100]}...")
```

**Note:** This method is particularly useful when you want to extract readable content from a webpage without HTML
markup.

### `query_ai(prompt: str, system_message: str = "You are a helpful assistant.", max_tokens: int = 500) -> str`

Queries an AI model to generate text based on a prompt.

**Parameters:**

- `prompt` (str): The prompt to generate text from
- `system_message` (str, optional): The system message to set the context (default: "You are a helpful assistant.")
- `max_tokens` (int, optional): Maximum number of tokens to generate (default: 500)

**Returns:**

- str: Generated text

**Usage Example:**

```python
web_helper = WebHelper()

# Simple query
response = web_helper.query_ai("What are the main features of Python?")
print(f"AI response: {response}")

# Custom system message and longer response
custom_response = web_helper.query_ai(
    prompt="Explain the concept of machine learning",
    system_message="You are an AI expert specializing in machine learning.",
    max_tokens=1000
)
print(f"Custom AI response: {custom_response}")
```

**Note:** This method allows you to leverage AI capabilities for various tasks such as summarization,
question-answering, or content generation based on web-scraped data.

## Error Handling

All methods in the `WebHelper` class use error logging. If an exception occurs, it will be logged using the `logger`
object before being raised. This helps in debugging and tracking issues.

## Examples of Use Cases

1. **Web Content Summarization:**
   Combine `fetch_url_text()` and `query_ai()` to create summaries of web pages.

   ```python
   url = "https://en.wikipedia.org/wiki/Artificial_intelligence"
   content = web_helper.fetch_url_text(url, max_chars=5000)
   summary = web_helper.query_ai(f"Summarize the following text:\n\n{content}", max_tokens=200)
   print(f"Summary of {url}:\n{summary}")
   ```

2. **Question Answering from Web Content:**
   Use `fetch_url_text()` to get information and `query_ai()` to answer questions based on that information.

   ```python
   url = "https://en.wikipedia.org/wiki/Climate_change"
   content = web_helper.fetch_url_text(url)
   question = "What are the main causes of climate change?"
   answer = web_helper.query_ai(f"Based on the following text, {question}\n\nText: {content}")
   print(f"Q: {question}\nA: {answer}")
   ```

3. **Content Comparison:**
   Fetch content from multiple URLs and use AI to compare them.

   ```python
   url1 = "https://en.wikipedia.org/wiki/Python_(programming_language)"
   url2 = "https://en.wikipedia.org/wiki/JavaScript"
   content1 = web_helper.fetch_url_text(url1, max_chars=3000)
   content2 = web_helper.fetch_url_text(url2, max_chars=3000)
   comparison = web_helper.query_ai(f"Compare and contrast the following two programming languages:\n\nPython:\n{content1}\n\nJavaScript:\n{content2}")
   print(f"Comparison:\n{comparison}")
   ```