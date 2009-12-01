from gui_interface import GuiInterface
from process_interface import ProcessInterface


class BaseGenerator(GuiInterface, ProcessInterface):
    pass


# TODO: move data from generator factory to here

def get_diagrams():
    return ["standard", "houses", "paper", "shiny"]
