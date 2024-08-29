import subprocess
import sys
import random
import json
import os
import re

def install_and_import(package):
    try:
        __import__(package)
    except ImportError:
        print(f"Package {package} not found. Installing...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
    finally:
        globals()[package] = __import__(package)

# Load JSON files
def load_json_file(file_name):
    file_path = os.path.join(os.path.dirname(__file__), "data", file_name)
    with open(file_path, "r", encoding='utf-8') as file:
        data = json.load(file)
    return data

def create_display_data(data):
    zh_list = [item["zh"] for item in data]
    en_list = [item["en"] for item in data]
    en_mapping = {item["zh"]: item["en"] for item in data}
    return zh_list, en_list, en_mapping

# Load JSON data and create display mappings
ARTFORM_ZH, ARTFORM_EN, ARTFORM_MAPPING = create_display_data(load_json_file("artform.json"))
PHOTO_TYPE_ZH, PHOTO_TYPE_EN, PHOTO_TYPE_MAPPING = create_display_data(load_json_file("photo_type.json"))
BODY_TYPES_ZH, BODY_TYPES_EN, BODY_TYPES_MAPPING = create_display_data(load_json_file("body_types.json"))
DEFAULT_TAGS_ZH, DEFAULT_TAGS_EN, DEFAULT_TAGS_MAPPING = create_display_data(load_json_file("default_tags.json"))
ROLES_ZH, ROLES_EN, ROLES_MAPPING = create_display_data(load_json_file("roles.json"))
HAIRSTYLES_ZH, HAIRSTYLES_EN, HAIRSTYLES_MAPPING = create_display_data(load_json_file("hairstyles.json"))
ADDITIONAL_DETAILS_ZH, ADDITIONAL_DETAILS_EN, ADDITIONAL_DETAILS_MAPPING = create_display_data(load_json_file("additional_details.json"))
PHOTOGRAPHY_STYLES_ZH, PHOTOGRAPHY_STYLES_EN, PHOTOGRAPHY_STYLES_MAPPING = create_display_data(load_json_file("photography_styles.json"))
DEVICE_ZH, DEVICE_EN, DEVICE_MAPPING = create_display_data(load_json_file("device.json"))
PHOTOGRAPHER_ZH, PHOTOGRAPHER_EN, PHOTOGRAPHER_MAPPING = create_display_data(load_json_file("photographer.json"))
ARTIST_ZH, ARTIST_EN, ARTIST_MAPPING = create_display_data(load_json_file("artist.json"))
DIGITAL_ARTFORM_ZH, DIGITAL_ARTFORM_EN, DIGITAL_ARTFORM_MAPPING = create_display_data(load_json_file("digital_artform.json"))
PLACE_ZH, PLACE_EN, PLACE_MAPPING = create_display_data(load_json_file("place.json"))
LIGHTING_ZH, LIGHTING_EN, LIGHTING_MAPPING = create_display_data(load_json_file("lighting.json"))
CLOTHING_ZH, CLOTHING_EN, CLOTHING_MAPPING = create_display_data(load_json_file("clothing.json"))
COMPOSITION_ZH, COMPOSITION_EN, COMPOSITION_MAPPING = create_display_data(load_json_file("composition.json"))
POSE_ZH, POSE_EN, POSE_MAPPING = create_display_data(load_json_file("pose.json"))
BACKGROUND_ZH, BACKGROUND_EN, BACKGROUND_MAPPING = create_display_data(load_json_file("background.json"))
FACE_FEATURES_ZH, FACE_FEATURES_EN, FACE_FEATURES_MAPPING = create_display_data(load_json_file("face_features.json"))
EYE_COLORS_ZH, EYE_COLORS_EN, EYE_COLORS_MAPPING = create_display_data(load_json_file("eye_colors.json"))
FACIAL_HAIR_ZH, FACIAL_HAIR_EN, FACIAL_HAIR_MAPPING = create_display_data(load_json_file("facial_hair.json"))
SKIN_TONE_ZH, SKIN_TONE_EN, SKIN_TONE_MAPPING = create_display_data(load_json_file("skin_tone.json"))
AGE_GROUP_ZH, AGE_GROUP_EN, AGE_GROUP_MAPPING = create_display_data(load_json_file("age_group.json"))
ETHNICITY_ZH, ETHNICITY_EN, ETHNICITY_MAPPING = create_display_data(load_json_file("ethnicity.json"))
ACCESSORIES_ZH, ACCESSORIES_EN, ACCESSORIES_MAPPING = create_display_data(load_json_file("accessories.json"))
EXPRESSION_ZH, EXPRESSION_EN, EXPRESSION_MAPPING = create_display_data(load_json_file("expression.json"))
TATTOOS_SCARS_ZH, TATTOOS_SCARS_EN, TATTOOS_SCARS_MAPPING = create_display_data(load_json_file("tattoos_scars.json"))
MAKEUP_STYLES_ZH, MAKEUP_STYLES_EN, MAKEUP_STYLES_MAPPING = create_display_data(load_json_file("makeup_styles.json"))
HAIR_COLOR_ZH, HAIR_COLOR_EN, HAIR_COLOR_MAPPING = create_display_data(load_json_file("hair_color.json"))
BODY_MARKINGS_ZH, BODY_MARKINGS_EN, BODY_MARKINGS_MAPPING = create_display_data(load_json_file("body_markings.json"))
PHOTO_FRAMING_ZH, PHOTO_FRAMING_EN, PHOTO_FRAMING_MAPPING = create_display_data(load_json_file("photo_framing.json"))

class PromptGenerator:
    def __init__(self):
        pass

    def split_and_choose(self, input_str):
        choices = [choice.strip() for choice in input_str.split(",")]
        return random.choice(choices)

    def get_choice(self, input_str, zh_choices, en_choices, mapping):
        if input_str == "禁用":
            return None  # 禁用选项不会返回任何内容
        elif input_str == "随机":
            return random.choice(en_choices)  # 随机选项返回英文内容
        elif "," in input_str:
            return self.split_and_choose(input_str)
        else:
            result = mapping.get(input_str)
            if result:
                return result
            return input_str  # 如果没有映射，则返回原始输入

    def clean_consecutive_commas(self, input_string):
        cleaned_string = re.sub(r',\s*,', ',', input_string)
        return cleaned_string

    def process_string(self, replaced):
        replaced = re.sub(r'\s*,\s*', ',', replaced)
        replaced = re.sub(r',+', ',', replaced)
        return replaced

    def generate_prompt(self, custom, subject, artform, photo_type, body_types, default_tags, roles, hairstyles,
                        additional_details, photography_styles, device, photographer, artist, digital_artform,
                        place, lighting, clothing, composition, pose, background, face_features, eye_colors,
                        facial_hair, skin_tone, age_group, ethnicity, accessories, expression, tattoos_scars,
                        makeup_styles, hair_color, body_markings, photo_framing):
        components = []
        if custom:
            components.append(custom)
        is_photographer = artform.lower() == "photography" or (
                artform.lower() == "随机" and random.choice([True, False])
        )

        if is_photographer:
            selected_photo_style = self.get_choice(photography_styles, PHOTOGRAPHY_STYLES_ZH,
                                                   PHOTOGRAPHY_STYLES_EN, PHOTOGRAPHY_STYLES_MAPPING)
            if selected_photo_style:
                components.append(selected_photo_style)
            if selected_photo_style and (default_tags != "禁用" or subject):
                components.append("of")

        if not subject:
            if default_tags == "随机":
                if body_types and body_types != "禁用":
                    selected_subject = self.get_choice(default_tags, DEFAULT_TAGS_ZH, DEFAULT_TAGS_EN,
                                                       DEFAULT_TAGS_MAPPING)
                    if selected_subject:
                        components.append("a")
                        body_type_choice = self.get_choice(body_types, BODY_TYPES_ZH, BODY_TYPES_EN, BODY_TYPES_MAPPING)
                        if body_type_choice:
                            components.append(body_type_choice)
                        components.append(selected_subject)
                elif body_types == "禁用":
                    selected_subject = self.get_choice(default_tags, DEFAULT_TAGS_ZH, DEFAULT_TAGS_EN,
                                                       DEFAULT_TAGS_MAPPING)
                    if selected_subject:
                        components.append(selected_subject)
                else:
                    body_type_en = self.get_choice(body_types, BODY_TYPES_ZH, BODY_TYPES_EN, BODY_TYPES_MAPPING)
                    if body_type_en:
                        components.append("a")
                        components.append(body_type_en)
                        selected_subject = self.get_choice(default_tags, DEFAULT_TAGS_ZH,
                                                           DEFAULT_TAGS_EN, DEFAULT_TAGS_MAPPING)
                        if selected_subject:
                            components.append(selected_subject)
            elif default_tags != "禁用":
                selected_subject = self.get_choice(default_tags, DEFAULT_TAGS_ZH, DEFAULT_TAGS_EN, DEFAULT_TAGS_MAPPING)
                if selected_subject:
                    components.append(selected_subject)
        else:
            if body_types != "禁用" and body_types != "随机":
                components.append("a")
                body_type_choice = self.get_choice(body_types, BODY_TYPES_ZH, BODY_TYPES_EN, BODY_TYPES_MAPPING)
                if body_type_choice:
                    components.append(body_type_choice)
            elif body_types != "禁用":
                body_type_en = self.get_choice(body_types, BODY_TYPES_ZH, BODY_TYPES_EN, BODY_TYPES_MAPPING)
                if body_type_en:
                    components.append("a")
                    components.append(body_type_en)
            components.append(subject)






        # 确保每个参数的禁用逻辑
        def add_if_not_disabled(param_name, zh_choices, en_choices, mapping):
            choice = self.get_choice(param_name, zh_choices, en_choices, mapping)
            if choice:
                components.append(choice)

        add_if_not_disabled(accessories, ACCESSORIES_ZH, ACCESSORIES_EN, ACCESSORIES_MAPPING)
        add_if_not_disabled(additional_details, ADDITIONAL_DETAILS_ZH, ADDITIONAL_DETAILS_EN,
                            ADDITIONAL_DETAILS_MAPPING)
        add_if_not_disabled(age_group, AGE_GROUP_ZH, AGE_GROUP_EN, AGE_GROUP_MAPPING)
        add_if_not_disabled(artform, ARTFORM_ZH, ARTFORM_EN, ARTFORM_MAPPING)
        add_if_not_disabled(artist, ARTIST_ZH, ARTIST_EN, ARTIST_MAPPING)
        add_if_not_disabled(background, BACKGROUND_ZH, BACKGROUND_EN, BACKGROUND_MAPPING)
        add_if_not_disabled(body_markings, BODY_MARKINGS_ZH, BODY_MARKINGS_EN, BODY_MARKINGS_MAPPING)
        add_if_not_disabled(body_types, BODY_TYPES_ZH, BODY_TYPES_EN, BODY_TYPES_MAPPING)
        add_if_not_disabled(clothing, CLOTHING_ZH, CLOTHING_EN, CLOTHING_MAPPING)
        add_if_not_disabled(composition, COMPOSITION_ZH, COMPOSITION_EN, COMPOSITION_MAPPING)
        add_if_not_disabled(default_tags, DEFAULT_TAGS_ZH, DEFAULT_TAGS_EN, DEFAULT_TAGS_MAPPING)
        add_if_not_disabled(device, DEVICE_ZH, DEVICE_EN, DEVICE_MAPPING)
        add_if_not_disabled(digital_artform, DIGITAL_ARTFORM_ZH, DIGITAL_ARTFORM_EN, DIGITAL_ARTFORM_MAPPING)
        add_if_not_disabled(ethnicity, ETHNICITY_ZH, ETHNICITY_EN, ETHNICITY_MAPPING)
        add_if_not_disabled(expression, EXPRESSION_ZH, EXPRESSION_EN, EXPRESSION_MAPPING)
        add_if_not_disabled(eye_colors, EYE_COLORS_ZH, EYE_COLORS_EN, EYE_COLORS_MAPPING)
        add_if_not_disabled(face_features, FACE_FEATURES_ZH, FACE_FEATURES_EN, FACE_FEATURES_MAPPING)
        add_if_not_disabled(facial_hair, FACIAL_HAIR_ZH, FACIAL_HAIR_EN, FACIAL_HAIR_MAPPING)
        add_if_not_disabled(hairstyles, HAIRSTYLES_ZH, HAIRSTYLES_EN, HAIRSTYLES_MAPPING)
        add_if_not_disabled(hair_color, HAIR_COLOR_ZH, HAIR_COLOR_EN, HAIR_COLOR_MAPPING)
        add_if_not_disabled(lighting, LIGHTING_ZH, LIGHTING_EN, LIGHTING_MAPPING)
        add_if_not_disabled(makeup_styles, MAKEUP_STYLES_ZH, MAKEUP_STYLES_EN, MAKEUP_STYLES_MAPPING)
        add_if_not_disabled(photographer, PHOTOGRAPHER_ZH, PHOTOGRAPHER_EN, PHOTOGRAPHER_MAPPING)
        add_if_not_disabled(photography_styles, PHOTOGRAPHY_STYLES_ZH, PHOTOGRAPHY_STYLES_EN,
                            PHOTOGRAPHY_STYLES_MAPPING)
        add_if_not_disabled(photo_framing, PHOTO_FRAMING_ZH, PHOTO_FRAMING_EN, PHOTO_FRAMING_MAPPING)
        add_if_not_disabled(photo_type, PHOTO_TYPE_ZH, PHOTO_TYPE_EN, PHOTO_TYPE_MAPPING)
        add_if_not_disabled(place, PLACE_ZH, PLACE_EN, PLACE_MAPPING)
        add_if_not_disabled(pose, POSE_ZH, POSE_EN, POSE_MAPPING)
        add_if_not_disabled(roles, ROLES_ZH, ROLES_EN, ROLES_MAPPING)
        add_if_not_disabled(skin_tone, SKIN_TONE_ZH, SKIN_TONE_EN, SKIN_TONE_MAPPING)
        add_if_not_disabled(tattoos_scars, TATTOOS_SCARS_ZH, TATTOOS_SCARS_EN, TATTOOS_SCARS_MAPPING)

        if components:
            components.append("BREAK_CLIPL")

        prompt = " ".join(components)
        prompt = re.sub(" +", " ", prompt)
        replaced = self.clean_consecutive_commas(prompt)

        return self.process_string(replaced)

class FluxPromptGenerator:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "自定义": ("STRING", {"multiline": True, "default": ""}),
                "主题": ("STRING", {"multiline": True, "default": ""}),
                "艺术形式": (["禁用", "随机"] + ARTFORM_ZH, {"default": "禁用"}),
                "照片类型": (["禁用", "随机"] + PHOTO_TYPE_ZH, {"default": "禁用"}),
                "身体类型": (["禁用", "随机"] + BODY_TYPES_ZH, {"default": "禁用"}),
                "默认标签": (["禁用", "随机"] + DEFAULT_TAGS_ZH, {"default": "禁用"}),
                "角色": (["禁用", "随机"] + ROLES_ZH, {"default": "禁用"}),
                "发型": (["禁用", "随机"] + HAIRSTYLES_ZH, {"default": "禁用"}),
                "额外细节": (["禁用", "随机"] + ADDITIONAL_DETAILS_ZH, {"default": "禁用"}),
                "摄影风格": (["禁用", "随机"] + PHOTOGRAPHY_STYLES_ZH, {"default": "禁用"}),
                "设备": (["禁用", "随机"] + DEVICE_ZH, {"default": "禁用"}),
                "摄影师": (["禁用", "随机"] + PHOTOGRAPHER_ZH, {"default": "禁用"}),
                "艺术家": (["禁用", "随机"] + ARTIST_ZH, {"default": "禁用"}),
                "数字艺术形式": (["禁用", "随机"] + DIGITAL_ARTFORM_ZH, {"default": "禁用"}),
                "地点": (["禁用", "随机"] + PLACE_ZH, {"default": "禁用"}),
                "照明": (["禁用", "随机"] + LIGHTING_ZH, {"default": "禁用"}),
                "服装": (["禁用", "随机"] + CLOTHING_ZH, {"default": "禁用"}),
                "构图": (["禁用", "随机"] + COMPOSITION_ZH, {"default": "禁用"}),
                "姿势": (["禁用", "随机"] + POSE_ZH, {"default": "禁用"}),
                "背景": (["禁用", "随机"] + BACKGROUND_ZH, {"default": "禁用"}),
                "面部特征": (["禁用", "随机"] + FACE_FEATURES_ZH, {"default": "禁用"}),
                "眼睛颜色": (["禁用", "随机"] + EYE_COLORS_ZH, {"default": "禁用"}),
                "面部毛发": (["禁用", "随机"] + FACIAL_HAIR_ZH, {"default": "禁用"}),
                "肤色": (["禁用", "随机"] + SKIN_TONE_ZH, {"default": "禁用"}),
                "年龄段": (["禁用", "随机"] + AGE_GROUP_ZH, {"default": "禁用"}),
                "种族": (["禁用", "随机"] + ETHNICITY_ZH, {"default": "禁用"}),
                "配饰": (["禁用", "随机"] + ACCESSORIES_ZH, {"default": "禁用"}),
                "表情": (["禁用", "随机"] + EXPRESSION_ZH, {"default": "禁用"}),
                "纹身_疤痕": (["禁用", "随机"] + TATTOOS_SCARS_ZH, {"default": "禁用"}),
                "化妆风格": (["禁用", "随机"] + MAKEUP_STYLES_ZH, {"default": "禁用"}),
                "发色": (["禁用", "随机"] + HAIR_COLOR_ZH, {"default": "禁用"}),
                "身体标记": (["禁用", "随机"] + BODY_MARKINGS_ZH, {"default": "禁用"}),
                "照片构图": (["禁用", "随机"] + PHOTO_FRAMING_ZH, {"default": "禁用"}),
            },
        }

    RETURN_TYPES = ("STRING",)
    FUNCTION = "execute"
    CATEGORY = "Prompt"

    def execute(self, 自定义, 主题, 艺术形式, 照片类型, 身体类型, 默认标签, 角色, 发型,
                额外细节, 摄影风格, 设备, 摄影师, 艺术家, 数字艺术形式, 地点, 照明,
                服装, 构图, 姿势, 背景, 面部特征, 眼睛颜色, 面部毛发, 肤色, 年龄段,
                种族, 配饰, 表情, 纹身_疤痕, 化妆风格, 发色, 身体标记, 照片构图):
        # 确保所有参数之间用逗号分隔，且没有多余的符号
        prompt_generator = PromptGenerator()
        prompt = prompt_generator.generate_prompt(
            自定义, 主题, 艺术形式, 照片类型, 身体类型, 默认标签, 角色, 发型,
            额外细节, 摄影风格, 设备, 摄影师, 艺术家, 数字艺术形式, 地点, 照明,
            服装, 构图, 姿势, 背景, 面部特征, 眼睛颜色, 面部毛发, 肤色, 年龄段,
            种族, 配饰, 表情, 纹身_疤痕, 化妆风格, 发色, 身体标记, 照片构图
        )
        return (prompt,)

    @classmethod
    def IS_CHANGED(cls, *args):
        return True

# Node export details
NODE_CLASS_MAPPINGS = {
    "FluxPromptGenerator": FluxPromptGenerator
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "FluxPromptGenerator": "Flux Prompt Generator"
}
