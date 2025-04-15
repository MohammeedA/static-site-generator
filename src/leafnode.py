from htmlnode import HTMLNode

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(value, None, props, tag)
    
    def to_html(self):
        if self.value is None:
            raise ValueError("LeafNode value cannot be None")
        if self.tag is None:
            return self.value
        props_str = self.props_to_html()
        return f"<{self.tag}{props_str}>{self.value}</{self.tag}>"