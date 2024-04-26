from nxt_vapp_handler import NXTVAppHandler
from nxt_rest_connection import NXTRestConnection


class NXTVAppClassifierChild(NXTVAppHandler):
    """Demonstration class how inheritance from NXTVAppHandler would work for the individual VisionApps
    (in this case for the Classifier App) with regard to code structure.

    Provides App specific functions such as show_attention_map.

    Requires established NxtRestConnection and name of the VisionApp"""
    def __init__(self, rest_connection: NXTRestConnection):
        super().__init__(rest_connection, "classifier")

    def show_attention_map(self, value: bool):
        self.configurable_int_double_string_enum_set("enable_attentionmap", value)

    def save_result_image(self, file_name: str):
        self.save_custom_result_image("default", file_name)

    def save_attention_map(self, file_name: str):
        self.save_custom_result_image("attentionmap", file_name)

    def get_available_cnns(self) -> [str]:
        return self.configurable_int_double_string_enum_range("cnns")
