import json
import random
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

__all__ = ("create_photo", "save_draw", "class_data", "draw_base")


def draw_base(res_file_load: Path) -> Image:
    """基础框架

    Args:
        res_file_load (Path): 资源文件路径

    Returns:
        img: 图片对象
    """
    # TODO: 画布 && 画笔
    base_img = Image.new(mode="RGBA", size=(2000, 1000), color="white")
    draw = ImageDraw.Draw(base_img, "RGBA")

    # TODO: 画格子
    draw.line(xy=(250, 0, 250, 1000), fill="black")  # 最左的竖线
    for i in range(500, 1751, 250):
        draw.line(xy=(i, 0, i, 890), fill="black")  # 竖线
    for i in [100, 235, 375, 515, 655, 750, 890]:
        draw.line(xy=(0, i, 2000, i), fill="black")  # 横线

    # TODO: 备注
    font = ImageFont.truetype(
        f"{res_file_load.joinpath('source')}/Deng.ttf",
        size=30
    )
    draw.text(xy=(95, 930), text="备注", font=font, fill=(47, 79, 79, 255))
    draw.text(xy=(95, 690), text="晚上", font=font, fill="black")  # 晚上

    # TODO: 节次
    font = ImageFont.truetype(
        f"{res_file_load.joinpath('source')}/Deng.ttf",
        size=25
    )
    draw.text(xy=(70, 140), text="第 1-2 节",
              font=font, fill="black")
    draw.text(xy=(70, 275), text="第 3-4 节",
              font=font, fill="black")
    draw.text(xy=(70, 415), text="第 5-6 节",
              font=font, fill="black")
    draw.text(xy=(70, 555), text="第 7-8 节",
              font=font, fill="black")
    draw.text(xy=(55, 790), text="第 9-10-11 节",
              font=font, fill="black")

    # TODO: 时间
    draw.text(xy=(50, 180), text="08:40—10:00", font=font, fill="black")
    draw.text(xy=(50, 315), text="10:20—11:40", font=font, fill="black")
    draw.text(xy=(50, 455), text="14:00—15:20", font=font, fill="black")
    draw.text(xy=(50, 595), text="15:30—17:00", font=font, fill="black")
    draw.text(xy=(60, 830), text="19:00—21:10", font=font, fill="black")

    # TODO: 星期
    days = ["星期一", "星期二", "星期三", "星期四", "星期五", "星期六", "星期天"]
    date_num = [330, 580, 830, 1080, 1330, 1580, 1830]
    font = ImageFont.truetype(
        f"{res_file_load.joinpath('source')}/Deng.ttf",
        size=30
    )
    # 星期
    for local, text in zip(date_num, days):
        draw.text(
            xy=(local, 40),
            text=text, font=font, fill="black"
        )
    return base_img


def save_draw(img_class: Image, save_load: Path):
    """存储基础图片

    Args:
        img_class (Image): 图片对象
        save_load (Path): 存储路径
    """
    p_load = save_load.parent
    if not Path.exists(p_load):
        Path.mkdir(p_load)
    img_class.save(save_load)


def class_data(class_info: dict = None):
    """处理课表数据"""
    data_class = {
        "bool": True,
        "data": {}
    }
    if class_info is None:
        data_load = str(
            Path(__file__).parent.parent / "res"
            / "2022级学前教育12班.json"
        )
        with open(data_load, mode="r", encoding="utf-8") as f:
            class_info = json.loads(f.read())
    data_class['data'] = class_info
    return data_class


def create_photo(cname=None, data=None) -> None or (Image and str):
    """
    绘制课表
    :param cname: 班级名
    :param data: 数据来源
    :param week: 周期
    :return: QQ_API(Send Message)
    """
    # 资源路径
    photo_path = Path(__file__).parent.parent / "source"
    if data is None:
        return None, photo_path / "img" / "init_photo.png"
    # 星期位置
    w_place_data = [250, 500, 750, 1000, 1250, 1500, 1750]
    # 时间位置
    h_place_data = {'first': 100, 'second': 235,
                    'third': 375, 'fourth': 515, 'fifth': 750}
    # 颜色列表
    color_list = [
        (251, 255, 242, 200), (192, 192, 192, 200), (255, 255, 0, 200),
        (244, 164, 95, 200), (127, 255, 0, 200), (218, 112, 214, 200),
        (156, 147, 133, 200), (186, 164, 48, 200), (15, 56, 154, 200),
        (49, 65, 196, 200), (153, 51, 250, 200), (34, 139, 34, 200),
        (255, 192, 203, 200), (255, 127, 80, 200), (237, 145, 33, 200)
    ]
    # 读取模板
    img = Image.open(f'{photo_path / "img" / "init_photo.png"}', 'r')
    # 字体|画笔
    font = ImageFont.truetype(f'{photo_path / "font" / "萝莉体.ttf"}', 20)
    img.convert("RGBA")
    draw = ImageDraw.Draw(img, "RGBA")
    # 颜色数据
    color_data = {}
    # 课表数据处理
    data_class = class_data(data)

    for week_day in range(0, 7):  # 取出一周中的 每一天
        try:
            class_ = data_class["data"][week_day + 1]
            for seq_info in class_:  # 每一周[节次]
                i = class_[seq_info]
                if i["lesson_name"] != '':
                    # 从课表中获取 课程名 i["lesson_name"]
                    if i["lesson_name"] in color_data.keys():
                        color = color_data[i["lesson_name"]]
                    else:
                        color = random.choice(
                            list(set(color_list) - set(color_data.values())))
                        color_data[i["lesson_name"]] = color

                    draw.rectangle((w_place_data[week_day], h_place_data[i["rank"]], w_place_data[week_day] + 249,
                                    h_place_data[i["rank"]] + 140), fill=color, outline=color)

                    draw.text((w_place_data[week_day] + 5, h_place_data[i["rank"]] + 15), text=i["lesson_name"],
                              font=font, fill=(0, 0, 0, 255))
                    draw.text((w_place_data[week_day] + 5, h_place_data[i["rank"]] + 40), text=i["teacher"], font=font,
                              fill=(0, 0, 0, 255))
                    draw.text((w_place_data[week_day] + 10, h_place_data[i["rank"]] + 65), text=i["week"], font=font,
                              fill=(0, 0, 0, 255))
                    draw.text((w_place_data[week_day] + 10, h_place_data[i["rank"]] + 90), text=i["place"], font=font,
                              fill=(0, 0, 0, 255))
        except [Exception, IndexError] as exc:
            print(f"绘制异常: {exc}")

    draw.text(
        (10, 35),  # 表头数据
        cname,  # 文本信息
        font=font,  # 采用字体
        fill=(0, 0, 0, 255)  # 头部数据绘制
    )

    save_path = str(photo_path.parent / "img" / f"{cname}.png")
    img.save(save_path)

    return img, save_path


if __name__ == "__main__":
    file = Path(__file__).parent

    img = draw_base(file)
    img.show()

    save_draw(
        img,
        file.parent / "source" / "img" / "init_photo.png"
    )
    print("Img Saved!")
