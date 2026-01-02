from rich.markup import render
from rich.text import Text

def convert_rich_to_markdown(markup: str) -> str:
    """
    Converts Rich markup strings to Markdown.
    Mapping:
    - [green] -> Stripped (plain text)
    - [yellow] -> **bold**
    - All other Rich tags are stripped.
    """
    if not markup:
        return ""
        
    text = render(markup)
    plain = text.plain
    
    markers = []
    for span in text.spans:
        style_str = str(span.style)
        
        if "yellow" in style_str:
            markers.append((span.start, "**"))
            markers.append((span.end, "**"))
            
    # Sort markers by position (descending) to avoid offset shifting issues
    # If positions are same, order doesn't matter much for our use case,
    # but let's be consistent.
    markers.sort(key=lambda x: (x[0], x[1]), reverse=True)
    
    # Apply markers
    result = list(plain)
    for pos, marker in markers:
        # Check if the marker is already there to avoid duplicates if multiple 
        # green/yellow styles applied to same span (unlikely)
        # However, list.insert is fine.
        result.insert(pos, marker)
        
    return "".join(result)

