

class HTMLNode:
    def __init__(self, tag=None, value=None, children:list = None, props:dict = None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError

    def props_to_html(self):
        if self.props is None or self.props == {}:
            return ""
        return " " + ' '.join([f'{k}="{v}"' for k, v in self.props.items()])

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"


class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag=tag, value=value, props=props, children=None)

    def to_html(self):
        if self.value is None:
            raise ValueError
        elif self.tag is None:
            return self.value

        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"

    def __repr__(self):
        return f"LeafNode({self.tag}, {self.value}, {self.props})"


class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag=tag, children=children, props=props)

    def to_html(self):
        if self.tag is None:
            raise ValueError("Tag is missing")
        elif self.children is None:
            raise ValueError("Class Parent Node needs to have children")
        output = ""
        for child in self.children:
            output += child.to_html()

        return f'<{self.tag}{self.props_to_html()}>{output}</{self.tag}>'
