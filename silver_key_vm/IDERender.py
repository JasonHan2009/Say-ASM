# Render Module
# Im Lazy Written it in IDE GUI Module
# Dev JasonHan2009
# IdeaSphere

class RenderModule:

    def __init__(self, type: str, color: str, msg: str = ""):
        self.type = type
        self.color = color
        self.msg = msg
    
    def render(self):
        return {
            "type" : self.type,
            "color" : self.color,
            "msg" : self.msg
        }

class Popup:

    def __init__(self, popup_type: str, text_color : str, type: str, text:str):
        """
        Popup Moudle
        popup_type:
            - "top"
            - "under"
            - "bottom_right"
        text_color:
            - any
        type:
            - any
        text:
            - any
        """
        self.popup_type = popup_type
        self.text_color = text_color
        self.type = type
        self.text = text
    
    def render(self):
        match self.popup_type:
            case "top":
                return {
                    "popup_type" : self.popup_type,
                    "text_color" : self.text_color,
                    "type" : self.type,
                    "text" : self.text
                }
            case "under":
                return {
                    "popup_type" : self.popup_type,
                    "text_color" : self.text_color,
                    "type" : self.type,
                    "text" : self.text
                }
            case "bottom_right":
                return {
                    "popup_type" : self.popup_type,
                    "text_color" : self.text_color,
                    "type" : self.type,
                    "text" : self.text
                }
            case _:
                return {"popup_type" : "error"}
      