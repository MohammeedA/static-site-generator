from textnode import TextNode, TextType, BlockType
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

def split_nodes_image(old_nodes):
    """
    Splits a list of TextNodes into groups based on images.
    """
    result = []
    
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            result.append(old_node)
            continue
        
        text = old_node.text
        images = extract_markdown_images(text)
        
        if not images:
            result.append(old_node)
            continue
            
        remaining_text = text
        new_nodes = []
        
        for img_alt, img_url in images:
            img_text = f"![{img_alt}]({img_url})"
            start_index = remaining_text.find(img_text)
            
            if start_index > 0:
                new_nodes.append(TextNode(remaining_text[:start_index], TextType.TEXT))
                
            new_nodes.append(TextNode(img_alt, TextType.IMAGE, url=img_url))
            remaining_text = remaining_text[start_index + len(img_text):]
            
        if remaining_text:
            new_nodes.append(TextNode(remaining_text, TextType.TEXT))
            
        result.extend(new_nodes)
            
    return result

def split_nodes_link(old_nodes):
    """
    Splits a list of TextNodes into groups based on links.
    """
    result = []
    
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            result.append(old_node)
            continue
        
        text = old_node.text
        links = extract_markdown_links(text)
        
        if not links:
            result.append(old_node)
            continue
            
        remaining_text = text
        new_nodes = []
        
        for link_text, link_url in links:
            link_md = f"[{link_text}]({link_url})"
            start_index = remaining_text.find(link_md)
            
            if start_index > 0:
                new_nodes.append(TextNode(remaining_text[:start_index], TextType.TEXT))
                
            new_nodes.append(TextNode(link_text, TextType.LINK, url=link_url))
            remaining_text = remaining_text[start_index + len(link_md):]
            
        if remaining_text:
            new_nodes.append(TextNode(remaining_text, TextType.TEXT))
            
        result.extend(new_nodes)
            
    return result

def text_to_textnodes(text: str) -> list[TextNode]:
    """
    Converts markdown text to a list of TextNodes.
    """
    nodes = [TextNode(text, TextType.TEXT)]
    
    # Split nodes based on delimiters (e.g., * for bold)
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    
    # Split nodes based on images and links
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    
    return nodes

def markdown_to_blocks(markdown: str) -> list[str]:
    """
    Converts markdown text to a list of blocks.
    Each block is separated by one or more empty lines.
    Returns a list of non-empty blocks with whitespace stripped.
    """
    blocks = markdown.split("\n\n")
    filtered_blocks = []
    for block in blocks:
        if block == "":
            continue
        block = block.strip()
        filtered_blocks.append(block)
    return filtered_blocks

def block_to_block_type(block: str) -> BlockType:
    lines = block.split("\n")

    if block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return BlockType.HEADING
    if block.startswith("```") and block.rstrip().endswith("```"):
        return BlockType.CODE
    if block.startswith(">"):
        for line in lines:
            if not line.startswith(">"):
                return BlockType.PARAGRAPH
        return BlockType.QUOTE
    if block.startswith("- "):
        for line in lines:
            if not line.startswith("- "):
                return BlockType.PARAGRAPH
        return BlockType.UNORDERED_LIST
    if block.startswith("1. "):
        i = 1
        for line in lines:
            if not line.startswith(f"{i}. "):
                return BlockType.PARAGRAPH
            i += 1
        return BlockType.ORDERED_LIST
    return BlockType.PARAGRAPH