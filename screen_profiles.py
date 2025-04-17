from config import rel_path

class ScreenProfile:
    def __init__(
        self,
        name,
        hamster_template_path,
        footer_template_path,
        regions,
        rom_rlt_template_path,
        page_templates,
        rlt_offsets  # tuple: (top_offset, bottom_offset, left_offset, right_offset)
    ):
        self.name = name
        self.hamster_template_path = hamster_template_path
        self.footer_template_path = footer_template_path
        self.regions = regions
        self.rom_rlt_template_path = rom_rlt_template_path
        self.page_templates = page_templates
        self.rlt_offsets = rlt_offsets

    def activate(self):
        import ocr.regions as regions_module
        regions_module.REGIONS = self.regions


class Profile1080p(ScreenProfile):
    def __init__(self):
        super().__init__(
            name="1080p",
            hamster_template_path=rel_path("ocr", "templates", "hamster_icon_1080p.png"),
            regions={
                "name": (10, 28, 450, 34),          # x, y, width, height
                "power_bonus": (10, 63, 400, 27),
                "price": (340, 73, 150, 23),
            },
            footer_template_path=rel_path("ocr", "templates", "footer_about_us_1080p.png"),
            rom_rlt_template_path=rel_path("ocr", "templates", "rom_rlt_1080p.png"),
            page_templates={
                "2": rel_path("ocr", "templates", "page_2_1080p.png"),
                "3": rel_path("ocr", "templates", "page_3_1080p.png"),
                "4": rel_path("ocr", "templates", "page_4_1080p.png"),
                "5": rel_path("ocr", "templates", "page_5_1080p.png"),
                "6": rel_path("ocr", "templates", "page_6_1080p.png"),
            },
            rlt_offsets=(
                50,   # top_offset
                95,  # bottom_offset
                490,  # left_offset
                55    # right_offset
            )
        )


class Profile4K(ScreenProfile):
    def __init__(self):
        super().__init__(
            name="4K",
            hamster_template_path=rel_path("ocr", "templates", "hamster_icon_4k.png"),
            regions={
                "name": (23, 46, 535, 34),          # x, y, width, height
                "power_bonus": (20, 85, 400, 27),
                "price": (450, 97, 150, 23),
            },
            footer_template_path=rel_path("ocr", "templates", "footer_about_us_4k.png"),
            rom_rlt_template_path=rel_path("ocr", "templates", "rom_rlt_4k.png"),
            page_templates={
                "2": rel_path("ocr", "templates", "page_2_4k.png"),
                "3": rel_path("ocr", "templates", "page_3_4k.png"),
                "4": rel_path("ocr", "templates", "page_4_4k.png"),
                "5": rel_path("ocr", "templates", "page_5_4k.png"),
                "6": rel_path("ocr", "templates", "page_6_4k.png"),
            },
            rlt_offsets=(
                68,  # top_offset
                122,  # bottom_offset
                595, # left_offset
                75   # right_offset
            )
        )


class DebugProfile(Profile1080p):
    def __init__(self):
        super().__init__()
        self.name = "debug"

    def get_debug_image_path(self):
        return rel_path("debug", "market_screen.png")

    def get_debug_crop_output_path(self, region_key):
        return rel_path("debug", f"crop_{region_key}.png")


def detect_and_activate_profile():
    import pyautogui
    width, height = pyautogui.size()
    if False:        #Debug
        profile = DebugProfile()
    elif width >= 3840:
        profile = Profile4K()
    else:
        profile = Profile1080p()
    profile.activate()
    return profile
