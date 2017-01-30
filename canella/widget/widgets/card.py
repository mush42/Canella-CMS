from .. import Widget, WidgetWidth, WidgetLocation

class CardWidget(Widget):
    template = 'canella/admin/widgets/card.html'
    width = WidgetWidth.third

    def __init__(self, color, icon, main_heading, sub_heading, details_link):
        self.color = color
        self.icon = icon
        self.main_heading = main_heading
        self.sub_heading = sub_heading
        self.details_link = details_link
