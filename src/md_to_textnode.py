from textnode import TextNode, TextType
import re

def split_nodes_delimiter(
    old_nodes: list[TextNode], delimiter: str, text_type: TextType
) -> list[TextNode]:
    """
    Splits a list of TextNodes into groups based on a delimiter.
    """

    result = []
    
    for old_node in old_nodes:
        # If not a text node, add it unchanged
        if old_node.text_type != TextType.TEXT:
            result.append(old_node)
            continue
        
        # Process text node
        text = old_node.text
        remaining_text = text
        new_nodes = []
        
        # Look for delimiter pairs
        while delimiter in remaining_text:
            # Find the first delimiter
            start_index = remaining_text.find(delimiter)
            
            # Add text before delimiter as normal text (if any)
            if start_index > 0:
                new_nodes.append(TextNode(remaining_text[:start_index], TextType.TEXT))
            
            # Find the closing delimiter
            end_index = remaining_text.find(delimiter, start_index + len(delimiter))
            if end_index == -1:
                raise ValueError(f"Closing delimiter not found: {delimiter}")
            
            # Extract the content between delimiters
            content = remaining_text[start_index + len(delimiter):end_index]
            new_nodes.append(TextNode(content, text_type))
            
            # Continue with the remaining text
            remaining_text = remaining_text[end_index + len(delimiter):]
        
        # Add any remaining text as normal text
        if remaining_text:
            new_nodes.append(TextNode(remaining_text, TextType.TEXT))
        
        # Add the new nodes to the result
        result.extend(new_nodes)
    
    return result

def extract_markdown_images(text: str) -> list[tuple[str, str]]:
    """
    Extracts images from markdown text.
    """
    re_image = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
    # This regex matches the markdown image syntax: ![alt text](url)
    return re.findall(re_image, text)

def extract_markdown_links(text: str) -> list[tuple[str, str]]:
    """
    Extracts links from markdown text.
    Returns a list of tuples containing (anchor_text, url).
    Example: For "[link](url)" returns [("link", "url")]
    """
    re_link = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
    # This regex matches markdown link syntax: [anchor text](url)
    return re.findall(re_link, text)