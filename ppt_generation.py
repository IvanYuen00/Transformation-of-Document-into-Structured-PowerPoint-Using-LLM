from langchain.llms import TextGen

normal_llm = TextGen(
    model_url="http://<LLM_SERVER_IP>:<PORT>/",  # Masked
    max_new_tokens=2048,
    seed=42,
    verbose=False
)

system = """
Write a presentation text. You only answer with finished presentation.
You must follow these:
- You write the texts no longer than 250 characters!
- You make very short titles!
- You make the presentation easy to understand.
- The presentation has a table of contents which matches the slide/content count.
- The presentation has a summary.
- You are not allowed to insert links/images.
- At least 5 pages.
- Use bullet point wisely.

Follow the format closely. Enclose your response in triple backquotes.
---
title: Example Slide
author: John Doe
---

# Example Title Slide

# Example Section Slide 1
- Bullet point 1
- Bullet point 2
- Bullet point 3

# Example Section Slide 2 containing two columns

:::::::::::::: {.columns}
::: {.column width="50%"}

## Column 1

This is the content of the first column.

:::
::: {.column width="50%"}

## Column 2

This is the content of the second column.

:::
::::::::::::::

# Example Ending Slide
"""

def ppt_md_generation(list_pinned):
    final_ans = normal_llm(f'''[INST] <<SYS>>
    {system}
    <</SYS>>
    List of text:
    {list_pinned}
[/INST]
''')
    return final_ans
