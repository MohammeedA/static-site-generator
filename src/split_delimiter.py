from textnode import TextNode, TextType

def split_nodes_delimiter(
    nodes: list[TextNode], delimiter: str, text_type: TextType
) -> list[TextNode]:
    """
    Splits a list of TextNodes into groups based on a delimiter.
    """
    #result = []
    #current_group = []

    result = []
    for node in nodes:
        if node.text_type != TextType.TEXT or delimiter not in node.text:
            # If the node is not TEXT or doesn't contain the delimiter,
            result.append(node)
            continue
        # Split the text by the delimiter
        splits = node.text.split(delimiter)
        if len(splits) == 1:
            # If the delimiter is not found, just append the node
            result.append(node)
            continue
        # Check for correct Markdown syntax
        if len(splits) % 2 == 0:
            raise ValueError("invalid Markdown syntax")
        for i in range(len(splits)):
            if i % 2 == 0 and splits[i] != "":
                result.append(TextNode(splits[i], TextType.TEXT))
            else:
                result.append(TextNode(splits[i], text_type))
        print(result)
    return result

"""    for node in nodes:
        if node.text_type != TextType.TEXT:
            result.append(node)
        elif delimiter in node.text:
            # Split the text by the delimiter
            md_text = node.text.split(delimiter)
            # Check for correct Markdown syntax
            if len(md_text) % 2 == 0:
                raise Exception("invalid Markdown syntax")
            for text in md_text:
                # Check if current group is empty
                if not current_group:
                    current_group.append(TextNode(text, TextType.TEXT))
                else:
                    if len(current_group) == 2:
                        current_group.append(TextNode(text,TextType.TEXT))
                        result.extend(current_group)
                        current_group = []
                    else:
                        current_group.append(TextNode(text, text_type))
        else:
            current_group.append(node)
    # Append any remaining nodes in the current group
    # to the result
    if current_group:
        result.extend(current_group)"""

    #return result
