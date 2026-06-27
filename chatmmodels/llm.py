from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_mistralai import ChatMistralAI

load_dotenv()

prompt = ChatPromptTemplate.from_template("""
You are an expert AI Study Assistant.

Your task is to analyze the given study material (paragraph, notes, article, chapter, or PDF text) and generate a well-structured study guide.

Instructions:
- Read the entire content carefully.
- Extract only information explicitly mentioned in the text.
- Never hallucinate or add outside knowledge.
- If information is unavailable, write "Not Mentioned."
- Use clear headings and bullet points.
- Keep explanations concise and easy to understand.
- Highlight exam-relevant information.

Generate the following:

# 📌 Overview
- Title (if available)
- Subject
- Main Topic
- Content Type

# 📖 Summary
Provide a concise summary of the content.

# 🎯 Main Concepts
List all major concepts discussed.

# ⭐ Important Topics
Rank the most important topics from highest to lowest priority.

# 🔥 Exam Priority
For every important topic mention:
- High Priority
- Medium Priority
- Low Priority

Also explain why you assigned that priority.

# 🧠 Key Points
Extract all important facts, concepts, definitions, rules, formulas, and principles.

# 📚 Important Terminology
List important terms with short explanations.

# 📅 Dates, Numbers & Statistics
Extract important dates, numerical values, formulas, percentages, or statistics.

# 👤 Important People / Organizations
Mention important people or organizations if present.

# ❓ Possible Exam Questions

Generate:

• 5 MCQs with answers

• 5 Short Answer Questions

• 5 Long Answer Questions

# 📝 Revision Notes
Create concise revision notes in bullet points.

# ⚡ One-Minute Revision Sheet
Create a quick revision sheet containing only the highest-yield points.

# 🔑 Keywords
List 15-20 important keywords.

# 📌 Final Summary
Summarize the complete document in 100 words or less.

Text:
{text}
""")

model = ChatMistralAI(
    model="mistral-small-latest",
    temperature=0
)

chain = prompt | model


def analyze_text(text):
    response = chain.invoke({"text": text})
    return response.content
