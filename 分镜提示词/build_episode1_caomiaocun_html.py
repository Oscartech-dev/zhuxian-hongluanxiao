from __future__ import annotations

import html
import importlib.util
import os
import shutil
from pathlib import Path
from urllib.parse import quote


HERE = Path(__file__).resolve().parent
PROJECT = HERE.parent
OUT = PROJECT / "制作脚本" / "第1集-草庙村" / "第1集-草庙村-制作脚本.html"
DOCS_OUT = PROJECT / "docs" / "ep1" / "index.html"
SOURCE = HERE / "build_episode1_caomiaocun_storyboard.py"
PUBLISH_ASSETS = OUT.parent / "assets"
LUXUEQI_PROFILE = PROJECT / "角色资产" / "陆雪琪" / "角色设定.md"
VIDEO_EXTS = {".mp4", ".mov", ".m4v", ".webm"}

ASSET_ALIASES = {
    "红鸾笑/场景资产/草庙村_木屋近景_绿色衣角风铃.jpg": "scene_wood_house_cloth.jpg",
    "红鸾笑/场景资产/草庙村_村内街巷全景.png": "scene_village_street.png",
    "红鸾笑/场景资产/草庙村_青云山脚全貌母场景.png": "scene_qingyun_village_wide.png",
    "红鸾笑/场景资产/草庙村_青云山云海御剑空镜.png": "scene_qingyun_clouds_swordflight_empty.png",
    "红鸾笑/场景资产/小竹峰_竹林溪桥仙门雅舍清晨残灯.png": "scene_xiaozhufeng_bamboo_bridge_lanterns.png",
    "红鸾笑/场景资产/小竹峰_居所室内圆窗清晨空镜.jpg": "scene_xiaozhufeng_interior_round_window.jpg",
    "红鸾笑/角色资产/陆雪琪/归档/archive_陆雪琪_四视图角色参考表_诛仙动画风_v2.png": "character_luxueqi_turnaround_v2.png",
    "红鸾笑/道具资产/天琊剑/归档/archive_天琊神剑_道具设定图_v1.png": "prop_tianya_sword_design_v1.png",
}


def load_luxueqi_character_prompt() -> str:
    if not LUXUEQI_PROFILE.is_file():
        return ""
    text = LUXUEQI_PROFILE.read_text(encoding="utf-8")
    marker = "### 00 · 四视图角色参考表"
    start = text.find(marker)
    if start == -1:
        return ""
    block = text[start:]
    fence_start = block.find("```text")
    if fence_start == -1:
        return ""
    prompt_start = fence_start + len("```text")
    fence_end = block.find("```", prompt_start)
    if fence_end == -1:
        return ""
    return block[prompt_start:fence_end].strip()


ASSET_PROMPT_OVERRIDES = {
    "红鸾笑/角色资产/陆雪琪/归档/archive_陆雪琪_四视图角色参考表_诛仙动画风_v2.png": load_luxueqi_character_prompt(),
    "红鸾笑/道具资产/天琊剑/归档/archive_天琊神剑_道具设定图_v1.png": """天琊神剑标准道具设定图，用于后续《红鸾笑》视频分镜中的道具一致性参考。主体是一柄清冷、修长、灵性极强的仙门神剑，属于陆雪琪的本命神兵。整体气质不是战斗化的凶器，而是清冷、圣洁、锋利、克制的仙剑。

剑身修长轻薄，比例优雅，剑体以银白色、冰蓝色、浅青蓝色为主。剑刃像寒冰与玉石结合，半透明质感，边缘锋利但不血腥。剑身中央有细长的冰蓝色灵纹或浅蓝透明槽线，内部仿佛有很淡的灵光流动。剑刃表面有冷玉、琉璃、寒冰、银金属混合质感，反光清透，不要厚重铁剑感。

剑柄与护手设计精致，有仙门神兵的华美感，但不能过度繁复。护手呈银白金属与冰蓝玉石结合的流线造型，带云纹、羽翼形、莲瓣形或水波形结构。剑柄处镶嵌青蓝宝石或碧色灵石，光芒克制。握柄修长，适合女性剑修单手持握，缠绕浅白或淡青色细纹材质，不要粗犷武器感。

剑鞘与剑身风格统一，银白、冰蓝、浅青蓝为主，表面有细密银丝纹、云纹、寒冰纹或青云门仙纹。剑鞘修长轻薄，末端精致，带少量玉石嵌件。后续视频中需保持剑身、剑鞘、护手、宝石、银蓝材质与该图一致。

风格参考腾讯《诛仙》动画剧集第二季 / 第三季 3D 国漫质感，玄机科技建模路线，仙侠古风，高级 3D CG 道具设定图。无文字、无水印、无 logo、无多余人物、无手持人物、无背景场景、无血迹、无破损、无现代科幻机械结构、不要西方骑士剑、不要武侠厚重大刀感、不要夸张火焰、不要爆炸剑气、不要大红大紫。""",
    "红鸾笑/场景资产/小竹峰_居所室内圆窗清晨空镜.jpg": """画面为 16:9 横版，小竹峰女子居所室内空镜，腾讯《诛仙》动画剧集 3D 国漫质感，黎明后的青蓝清晨。

机位采用平视略高机位，24mm 广角，三分之二侧后方观察视角；镜头位于房间内侧偏后位置，能同时看到室内陈设、圆形月洞门或圆窗、半开的窗棂，以及窗外竹林、晨雾和微弱天光。空间要宽广、干净、层次清晰。

室内为小竹峰仙门雅舍：竹木结构精致，墙面素雅，青灰色木柱，圆形月洞门、圆窗或圆形窗棂清晰可见。窗边有低矮木案、青瓷茶盏、卷轴、书册、素色屏风、淡色纱帘、竹帘，陈设清雅克制，不要奢华宫殿感。

窗外可见竹林、山雾、溪水或远处山壁的一小部分。清晨青蓝光从窗外进入，屋内残留少量暖色小灯或回廊灯光映入，形成克制冷暖对比。纱帘被微风轻轻吹起，空气中有少量尘埃和薄雾感。

画面重点：室内空间关系、圆形门窗、竹木雅舍、窗边坐席、木案卷轴、青瓷茶盏、素色屏风、纱帘、窗外竹林晨雾。整体气质清冷、安静、出尘，是小竹峰女弟子的修仙居所。

负面限制：不要人物，不要人物背影，不要人物剪影，不要动物，不要现代家具，不要电灯，不要沙发，不要床铺过于生活化，不要农舍，不要客栈，不要宫殿大殿，不要红色喜庆装饰，不要大红灯笼，不要奢华金色装饰，不要武器陈列过多，不要战斗氛围，不要夜晚，不要恐怖阴森，不要文字水印，不要 logo，不要鱼眼畸变，不要过度梦幻发光，不要把窗外完全虚化。""",
    "红鸾笑/场景资产/小竹峰_竹林溪桥仙门雅舍清晨残灯.png": """画面为 16:9 横版，小竹峰深处仙门女子居所外部主场景，国风仙侠动画电影质感，腾讯《诛仙》动画剧集 3D 国漫风格，黎明前后的青蓝清晨。

机位采用平视略高机位，24mm 广角，三分之二侧前方观察视角；镜头位于竹林溪岸外侧，隔着溪流与小桥看向中景居所。画面宽广、干净、层次清晰。

前景是高挑修长的青竹、竹叶、溪边石阶和薄雾。溪流清浅，水面有晨雾缓慢漂浮。溪上必须是一座小巧精致的弧形拱桥，不要直板桥；桥可以是竹木与青石结合，桥身略拱，栏杆细致，有东方园林感和仙门雅致感，尺度小而灵秀。

中景是一座小竹峰清雅居所：青瓦或深灰瓦屋顶，屋脊轻微上扬，飞檐克制，竹木结构精致，墙面素雅，门窗有圆形月洞门、圆窗或圆形窗棂元素。入口可以有小平台、回廊、细竹帘、素色纱帘，屋内透出极淡暖光。

房外回廊下挂着几盏小巧素雅的暖色灯笼，灯笼还微微亮着，像清晨天刚亮、多数人尚未醒来时残留的夜灯。灯笼颜色以淡米白、浅杏色、暖黄为主，不要大红灯笼，不要节庆感。

远景是小竹峰陡峭山壁、层叠竹林和云雾。山雾在林间、溪面和屋檐后方流动，形成前景竹林、中景居所、远景仙山的三层空间。整体色调以青蓝、墨绿、淡白晨雾为主，屋内暖光与回廊残灯作为小面积点缀。

负面限制：不要人物，不要人物背影，不要人物剪影，不要动物，不要农舍，不要草堆，不要茅草屋顶，不要柴火堆，不要农具，不要普通乡村木屋，不要直板桥，不要现代建筑，不要城市，不要大红灯笼，不要节庆装饰，不要喜庆氛围，不要大面积红色，不要欧式城堡，不要恐怖阴森，不要战斗场面，不要文字水印，不要 logo，不要强烈夜景，不要过度梦幻发光，不要鱼眼畸变，不要浅景深虚化大面积背景。""",
    "红鸾笑/场景资产/草庙村_青云山云海御剑空镜.png": """画面为 16:9 横版，清晨青云山上空的云海御剑建立镜头，腾讯《诛仙》动画剧集 3D 国漫质感，东方仙侠电影场景图。

机位采用高空航拍视角，24mm 超广角，从云层之间俯瞰青云山群峰与山脚方向。画面上半部分是层叠流动的青白云海，云层有明显前中后景关系；远处是巍峨连绵的青云山山脉，山腰被白色仙雾缠绕，峰顶在清晨暖金色日光边缘中若隐若现。

画面中下部可以看到山谷、林海和青云山脚下的一片荒村废墟轮廓。

整体氛围清冷、辽阔、安静，带一点即将抵达故地的命运感。色彩以青蓝云雾、墨青山脉、淡白晨雾为主，暖金日出边缘光作为小面积点缀。云层要有体积感，山脉和山谷要有空间纵深。""",
    "红鸾笑/场景资产/草庙村_青云山脚全貌母场景.png": """生成宏大的草庙村废墟全貌场景，清晨暖橙逆光，薄雾，废墟木石材质，木屋炊烟，东方仙侠动画电影风格。视角从村外高处或山坡上远眺，16:9 横版，extreme wide establishing shot，24mm 超广角，deep depth of field。

画面必须展示整个草庙村废墟坐落在青云山脚下。远景背景是巍峨连绵的青云山脉，高耸入云，山腰有云雾缭绕，带东方仙山气势；山脚下是一片荒废小村的全貌，可以看到几十处低矮残墙、倒塌房基、破屋架、断木梁、旧井、石磨、被野草覆盖的小路和零散院落遗迹。村落整体被荒草、藤蔓和薄雾包围，能看出这里曾经有人居住，如今只剩废墟。

画面中后景偏右或偏中位置，保留一间新立的简陋木屋，但木屋必须很小，占画面不超过 5%-8%，只是整个废村中的一个温暖小点。木屋烟囱冒出一缕细细炊烟，炊烟在晨雾中向上散开，成为观众发现“有人住在这里”的线索，而不是画面主体。

因为这是远景全貌，屋檐下的水绿色女子裙角残片可以非常小，只需要在木屋檐下有一点浅水绿色提示即可，不要做成旗子、布幡或完整飘带。它应是手掌大小的破碎衣角，被细绳系在檐角下，像珍藏多年的私人遗物。远景中不要让它变成大块装饰布。

整体氛围：青云山脚、荒村废墟、清晨薄雾、温柔而苍凉、久别重逢前一刻的命运感。腾讯《诛仙》动画剧集 3D 国漫质感，东方仙侠，3D animated cinematic environment, rich environmental storytelling, Qingyun mountain background, ruined village at the foot of the mountain, atmospheric fog, warm backlight, no characters.

负面限制：不要人物，不要狗，不要猴子，不要现代建筑，不要城市，不要电线杆，不要灯笼，不要金属风铃，不要旗子，不要布幡，不要长飘带，不要完整布条，不要大块布料，不要装饰挂旗，不要让木屋占满画面，不要近景构图，不要村内街巷近景，不要单一木屋特写，不要浅景深虚化背景，不要看不到青云山，不要只有小山丘，不要恐怖鬼屋感，不要夜晚，不要雪景，不要文字，不要水印。""",
    "红鸾笑/场景资产/草庙村_村内街巷全景.png": """画面为 16:9 横版，草庙村废墟村内街巷全景，腾讯《诛仙》动画剧集 3D 国漫质感，清晨暖橙逆光，薄雾轻笼。

机位保持 24mm-35mm 广角，视角位于荒废村路中段，沿旧村路向前看。画面要有清晰前景、中景、远景：前景是断裂木梁、碎瓦、荒草和半埋石块；中景是两侧低矮残墙、倒塌房基、旧院墙、青苔石磨或旧井；远景继续延伸出被晨雾吞没的残破村路和模糊山影。

整体必须能看出“曾经是村子，如今荒废多年”：旧路仍有走向，房基仍有轮廓，断木梁、碎瓦、荒草、藤蔓和湿润石墙交错。画面细节丰富，适合作为后续镜头裁切出断梁、石磨、半埋木柱、旧村路、残墙、荒草等局部。

光线保持温柔清晨，不要恐怖化。暖橙逆光从远处穿过薄雾，照亮草尖和破碎木结构边缘。画面苍凉但不阴森，有久别重返旧地的安静气息。

负面限制：不要人物，不要动物，不要现代物品，不要电线杆，不要城市元素，不要血迹，不要恐怖鬼屋，不要夜晚，不要新建筑，不要让木屋成为主体，不要文字水印，不要浅景深虚化大面积背景。""",
    "红鸾笑/场景资产/草庙村_木屋近景_绿色衣角风铃.jpg": """画面为 16:9 横版，草庙村废墟深处木屋近景，清晨暖光，薄雾，腾讯《诛仙》动画剧集 3D 国漫质感。

杂草与残墙之后，一间新立但简陋的木屋赫然立着。木屋木板粗糙朴素，结构简洁，歪斜烟囱飘出袅袅轻烟。木屋周围仍是草庙村废墟：断墙、倒塌木梁、荒草、碎石、碎瓦和晨雾。画面要保留“荒废村落中的一点烟火气”，不要把木屋做成精致客栈或仙门建筑。

屋檐下保留一小片浅水绿色女子裙角残片，用细绳系住，随风轻轻动。它是手掌大小的不规则破碎衣角，边缘撕裂，有细线头，薄纱或薄绸质地，旧而柔软。它可以被看见，但不要做成大旗帜、布幡、完整飘带或装饰风铃。

整体氛围是荒凉中的烟火气，是“有人在废墟中住下”的关键线索。晨光从侧后方照来，炊烟、薄雾和衣角轻动形成安静、温柔、克制的记忆感。

负面限制：不要人物，不要狗，不要猴子，不要金属风铃，不要旗子，不要布幡，不要长飘带，不要完整布条，不要大块布料，不要现代建筑，不要过度阴森，不要把木屋做成农家乐或客栈，不要文字水印。""",
}


def load_storyboard():
    spec = importlib.util.spec_from_file_location("episode1_caomiaocun_storyboard", SOURCE)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot load {SOURCE}")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return (
        mod.sections,
        mod.ASSET_PROMPTS,
        getattr(mod, "VIDEO_GROUPS", []),
        getattr(mod, "SHOT_ELEMENTS", {}),
    )


def esc(value: object) -> str:
    return html.escape("" if value is None else str(value), quote=True)


def asset_paths(asset_text: str) -> list[str]:
    if not asset_text:
        return []
    parts = []
    for raw in asset_text.replace("；", ";").split(";"):
        item = raw.strip()
        if item:
            parts.append(item)
    return parts


def asset_to_uri(asset: str) -> str:
    alias = ASSET_ALIASES.get(asset)
    if alias:
        rel = Path("assets") / alias
    else:
        path = Path(asset)
        if path.parts and path.parts[0] == PROJECT.name:
            path = Path(*path.parts[1:])
        target = PROJECT / path
        rel = os.path.relpath(target, OUT.parent)
    return quote(str(rel), safe="/")


def render_asset(asset: str) -> str:
    if not asset:
        return ""
    path = Path(asset)
    if path.parts and path.parts[0] == PROJECT.name:
        path = Path(*path.parts[1:])
    target = PROJECT / path
    if not target.is_file():
        return f'<div class="asset-missing">待补资产：<code>{esc(asset)}</code></div>'
    uri = asset_to_uri(asset)
    figure_class = "asset-figure"
    if "/道具资产/" in asset or "天琊" in asset:
        figure_class += " asset-figure-contain"
    return (
        f'<figure class="{figure_class}">'
        f'<img src="{uri}" alt="{esc(asset)}">'
        f'<figcaption>{esc(asset)}</figcaption>'
        "</figure>"
    )


def media_to_uri(asset: str) -> str:
    path = Path(asset)
    if path.parts and path.parts[0] == PROJECT.name:
        path = Path(*path.parts[1:])
    target = PROJECT / path
    rel = os.path.relpath(target, OUT.parent)
    return quote(str(rel), safe="/")


def copy_publish_assets() -> None:
    PUBLISH_ASSETS.mkdir(parents=True, exist_ok=True)
    for source_text, alias in ASSET_ALIASES.items():
        path = Path(source_text)
        if path.parts and path.parts[0] == PROJECT.name:
            path = Path(*path.parts[1:])
        source = PROJECT / path
        if source.is_file():
            shutil.copy2(source, PUBLISH_ASSETS / alias)


def render_shot_elements(elements: dict[str, str]) -> str:
    if not elements:
        return ""
    rows = "".join(
        f"<div><dt>{esc(label)}</dt><dd>{esc(value)}</dd></div>"
        for label, value in elements.items()
    )
    return f"""
        <section class="shot-elements">
          <h4>参与元素 / 参考资产</h4>
          <dl>{rows}</dl>
        </section>
    """


def asset_category(asset: str) -> str:
    if "/角色资产/" in asset:
        return "人物资产"
    if "天琊" in asset or "/道具资产/" in asset:
        return "道具资产"
    return "场景资产"


def asset_title(asset: str) -> str:
    stem = Path(asset).stem
    if stem.startswith("archive_"):
        stem = stem.replace("archive_", "", 1)
    return stem.replace("_", " ")


def fallback_asset_prompt(asset: str) -> str:
    if "/角色资产/" in asset:
        return (
            f"以该资产图作为角色一致性母版：{asset}。后续所有陆雪琪相关镜头需严格保持脸型、五官比例、发型、发饰、白色仙门服饰、"
            "清冷气质和3D国漫质感一致。该图只作为人物形象参考，不额外生成道具。"
        )
    return f"以该资产图作为场景参考母图：{asset}。后续镜头需保持空间结构、光线、色调、材质和气氛一致。"


def build_asset_prompt_entries(
    asset_prompts: dict[str, tuple[str, str]],
    video_groups: list[dict[str, object]],
) -> tuple[list[dict[str, object]], dict[str, list[dict[str, object]]]]:
    entries: list[dict[str, object]] = []
    by_asset: dict[str, dict[str, object]] = {}
    by_shot: dict[str, list[dict[str, object]]] = {}
    for shot, (asset_text, prompt) in asset_prompts.items():
        asset_text = asset_text.strip()
        prompt = prompt.strip()
        if not asset_text or not prompt:
            continue
        assets = asset_paths(asset_text)
        for asset in assets:
            final_prompt = ASSET_PROMPT_OVERRIDES.get(asset) or prompt
            if asset not in by_asset:
                entry = {
                    "id": f"asset-prompt-{len(entries) + 1:02d}",
                    "asset": asset,
                    "title": asset_title(asset),
                    "category": asset_category(asset),
                    "prompt": final_prompt,
                    "shots": [],
                    "prompt_rank": 0 if len(assets) == 1 else 1,
                }
                by_asset[asset] = entry
                entries.append(entry)
            entry = by_asset[asset]
            if ASSET_PROMPT_OVERRIDES.get(asset):
                entry["prompt"] = ASSET_PROMPT_OVERRIDES[asset]
                entry["prompt_rank"] = -1
            elif len(assets) == 1 and int(entry.get("prompt_rank", 9)) > 0:
                entry["prompt"] = prompt
                entry["prompt_rank"] = 0
            if str(shot) not in entry["shots"]:
                entry["shots"].append(str(shot))
            by_shot.setdefault(str(shot), []).append(entry)

    for group in video_groups:
        for asset in group.get("assets", []):
            asset = str(asset)
            if asset not in by_asset:
                entry = {
                    "id": f"asset-prompt-{len(entries) + 1:02d}",
                    "asset": asset,
                    "title": asset_title(asset),
                    "category": asset_category(asset),
                    "prompt": ASSET_PROMPT_OVERRIDES.get(asset) or fallback_asset_prompt(asset),
                    "shots": [],
                    "prompt_rank": 2,
                }
                by_asset[asset] = entry
                entries.append(entry)
    return entries, by_shot


def render_prompt_ref(entries: list[dict[str, object]] | None) -> str:
    if not entries:
        return '<p class="prompt-ref">参考图提示词：待整理</p>'
    links = []
    seen = set()
    for entry in entries:
        entry_id = str(entry.get("id", ""))
        if not entry_id or entry_id in seen:
            continue
        seen.add(entry_id)
        links.append(
            f'<a href="#{esc(entry_id)}">{esc(str(entry.get("id", "")).replace("asset-prompt-", "#"))} {esc(entry.get("title", ""))}</a>'
        )
    return (
        '<p class="prompt-ref">参考图提示词：'
        f'见资产提示词库 {" ".join(links)}'
        "</p>"
    )


def render_asset_prompt_library(entries: list[dict[str, object]]) -> str:
    if not entries:
        return ""
    category_order = ["人物资产", "场景资产", "道具资产"]
    grouped = {category: [] for category in category_order}
    for entry in entries:
        grouped.setdefault(str(entry.get("category", "其他资产")), []).append(entry)
    groups_html = []
    for category in [*category_order, *[key for key in grouped if key not in category_order]]:
        category_entries = grouped.get(category, [])
        cards = []
        for entry in category_entries:
            asset = str(entry.get("asset", ""))
            visuals = render_asset(asset)
            shot_tags = "".join(f"<span>镜{esc(shot)}</span>" for shot in entry.get("shots", []))
            cards.append(
                f"""
                <article class="asset-prompt-card" id="{esc(entry.get('id', ''))}">
                  <div class="asset-prompt-head">
                    <div>
                      <span>{esc(str(entry.get('id', '')).replace('asset-prompt-', '#'))}</span>
                    <h3>{esc(entry.get('title', '资产图'))}</h3>
                    </div>
                    <div class="shot-tags">{shot_tags}</div>
                  </div>
                  <div class="asset-prompt-body">
                    <div class="visuals">{visuals}</div>
                    <p>{esc(entry.get('prompt', ''))}</p>
                  </div>
                </article>
                """
            )
        if not cards:
            cards.append('<div class="asset-empty">暂无已确认资产图</div>')
        groups_html.append(
            f"""
            <section class="asset-category">
              <h3>{esc(category)}</h3>
              <div class="asset-prompt-grid">{''.join(cards)}</div>
            </section>
            """
        )
    return f"""
      <section class="asset-library" id="asset-prompt-library">
        <div class="section-title">
          <span>Asset Prompt Library</span>
          <h2>资产提示词库</h2>
        </div>
        <div class="asset-library-note">资产提示词库按“一张资产图对应一个提示词”归档；同一资产被多个镜头复用时，只保留一条资产提示词，镜头卡只放索引。</div>
        {''.join(groups_html)}
      </section>
    """


def render_group_asset(asset: str) -> str:
    return render_asset(asset)


def video_target(path_text: str) -> Path:
    path = Path(path_text)
    if path.parts and path.parts[0] == PROJECT.name:
        path = Path(*path.parts[1:])
    return PROJECT / path


def video_record_for_path(path: Path, index: int) -> dict[str, object]:
    rel = path.relative_to(PROJECT)
    stem_parts = path.stem.split("_")
    title = stem_parts[-1] if len(stem_parts) > 1 else f"候选 {index}"
    if title.startswith("候选") and len(title) > 2:
        title = f"候选 {title.replace('候选', '', 1)}"
    return {
        "title": title,
        "path": f"{PROJECT.name}/{rel.as_posix()}",
        "meta": "Seedance 2.0 / 1280x720 / 约15s",
    }


def group_video_assets(group: dict[str, object]) -> list[dict[str, object]]:
    explicit = [dict(item) for item in group.get("video_assets", [])]
    seen = {video_target(str(item.get("path", ""))).resolve() for item in explicit if item.get("path")}
    videos_dir = OUT.parent / "assets" / "videos"
    group_id = str(group.get("id", "")).strip()
    if videos_dir.is_dir() and group_id:
        for path in sorted(videos_dir.iterdir(), key=lambda item: item.name):
            if path.suffix.lower() not in VIDEO_EXTS:
                continue
            if not path.name.startswith(f"{group_id}_"):
                continue
            resolved = path.resolve()
            if resolved in seen:
                continue
            explicit.append(video_record_for_path(path, len(explicit) + 1))
            seen.add(resolved)
    return explicit


def render_video_assets(
    title: str,
    note: str,
    variant_hint: str = "版本 A",
    videos: list[dict[str, object]] | None = None,
) -> str:
    video_items = []
    for index, video in enumerate(videos or [], 1):
        path = str(video.get("path", ""))
        if not path:
            continue
        source_path = Path(path)
        if source_path.parts and source_path.parts[0] == PROJECT.name:
            source_path = Path(*source_path.parts[1:])
        target = PROJECT / source_path
        if not target.is_file():
            video_items.append(
                f"""
                <div class="video-missing">
                  <strong>{esc(video.get('title', f'候选 {index}'))}</strong>
                  <span>待补视频：<code>{esc(path)}</code></span>
                </div>
                """
            )
            continue
        video_items.append(
            f"""
            <figure class="video-candidate">
              <video controls preload="metadata" src="{media_to_uri(path)}"></video>
              <figcaption>
                <strong>{esc(video.get('title', f'候选 {index}'))}</strong>
                <span>{esc(video.get('meta', ''))}</span>
              </figcaption>
            </figure>
            """
        )
    if video_items:
        video_body = f'<div class="video-candidate-grid">{"".join(video_items)}</div>'
        variant_hint = f"{len(video_items)} 个候选"
    else:
        video_body = f"""
        <div class="video-slot">
          <div>
            <strong>{esc(note)}</strong>
            <span>16:9 视频素材占位，可追加多版本出片后人工剪辑选优</span>
          </div>
        </div>
        """
    return f"""
      <section class="video-assets">
        <div class="video-assets-head">
          <h4>{esc(title)}</h4>
          <span>{esc(variant_hint)}</span>
        </div>
        {video_body}
      </section>
    """


def build_shot_video_prompt(row: list[str]) -> str:
    shot, scene, shot_size, motion, picture, duration, sound, _note = row
    return (
        f"镜 {shot}｜{scene}｜{duration}\n"
        f"景别：{shot_size}。\n"
        f"构图：围绕本镜头核心画面组织画面层次，主体明确，环境信息保留，不要把背景完全虚化。\n"
        f"运镜手法：{motion}。镜头运动要服务情绪和叙事，节奏克制，避免无意义摇晃。\n"
        f"画面内容：{picture}\n"
        f"声音：{sound}\n"
        "整体风格：腾讯《诛仙》动画剧集 3D 国漫质感，国风仙侠电影感，清晨光线、薄雾、衣袂和环境细节保持统一。\n"
        "限制：不要新增无关人物，不要现代元素，不要字幕、水印、logo，不要过度炫光，不要改变已确认角色脸型、服装和场景结构。"
    )


def render_video_group(group: dict[str, object], shot_cards: str) -> str:
    assets = group.get("assets", [])
    pending_assets = group.get("pending_assets", [])
    visuals = "".join(render_group_asset(str(asset)) for asset in assets)
    visuals += "".join(
        f'<div class="asset-missing">{esc(asset)}</div>'
        for asset in pending_assets
    )
    shot_label = "、".join(f"镜{shot}" for shot in group.get("shots", []))
    shot_cards_html = f'<div class="shot-grid">{shot_cards}</div>' if shot_cards else ""
    videos = group_video_assets(group)
    return f"""
      <section class="video-group" id="{esc(group.get('id', ''))}">
        <div class="video-group-head">
          <div>
            <span>{esc(group.get('id', ''))}</span>
            <h3>{esc(group.get('title', ''))}</h3>
          </div>
          <div class="video-group-meta">
            <span>{esc(shot_label)}</span>
            <span>{esc(group.get('duration', ''))}</span>
            <span>{esc(group.get('strategy', ''))}</span>
          </div>
        </div>
        <div class="video-group-body">
          <section class="video-prompt video-group-prompt">
            <h4>合并视频生成提示词（可直接复制）</h4>
            <p>{esc(group.get('prompt', group.get('overview', '')))}</p>
          </section>
          <section class="reference-assets">
            <h4>参考资产</h4>
            <div class="visuals">{visuals}</div>
          </section>
          {render_video_assets("合并视频素材", str(group.get('video_asset_note', '待生成 / Seedance')), "主素材", videos)}
        </div>
        {shot_cards_html}
      </section>
    """


def render_shot(
    row: list[str],
    asset_prompt: tuple[str, str],
    elements: dict[str, str] | None = None,
    prompt_entry: dict[str, object] | None = None,
) -> str:
    shot, scene, shot_size, motion, picture, duration, sound, note = row
    asset_text, _prompt = asset_prompt
    assets = asset_paths(asset_text)
    asset_html = "".join(render_asset(asset) for asset in assets)
    video_prompt = build_shot_video_prompt(row)
    future_video_note = "待生成 / Seedance"
    if str(shot) in {"1", "2"}:
        future_video_note = "可由 VG-01 成片裁切 / 也可单独补生成。"
    dialogue = "无对白"
    elements_html = render_shot_elements(elements or {})
    prompt_ref_html = render_prompt_ref(prompt_entry)
    return f"""
      <article class="shot-card" id="shot-{esc(shot)}">
        <div class="shot-head">
          <div>
            <span class="shot-num">镜 {esc(shot)}</span>
            <h3>{esc(scene)}</h3>
          </div>
          <span class="duration">{esc(duration)}</span>
        </div>
        <section class="block video-prompt primary-video-prompt">
          <h4>视频生成提示词</h4>
          <p>{esc(video_prompt)}</p>
        </section>
        {render_video_assets("视频素材", future_video_note, f"镜 {esc(shot)}")}
        <section class="shot-description">
          <h4>镜头描述</h4>
          <p><strong>画面内容：</strong>{esc(picture)}</p>
          <p><strong>音效：</strong>{esc(sound)}</p>
          <p><strong>对白：</strong>{esc(dialogue)}</p>
          <p><strong>时长：</strong>{esc(duration)}</p>
          <p><strong>机位和运镜：</strong>{esc(shot_size)}；{esc(motion)}</p>
        </section>
        {elements_html}
        <section class="block reference-note">
          <h4>参考图备注</h4>
          <div class="visuals">{asset_html}</div>
          <p>{esc(note)}</p>
          {prompt_ref_html}
        </section>
      </article>
    """


def main() -> None:
    sections, asset_prompts, video_groups, shot_elements = load_storyboard()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    copy_publish_assets()
    asset_prompt_entries, prompt_entry_by_shot = build_asset_prompt_entries(asset_prompts, video_groups)
    total_seconds = 0
    shot_count = 0
    confirmed = 0
    body_parts = []
    nav_parts = []
    groups_by_first_shot = {
        str(group["shots"][0]): group
        for group in video_groups
        if group.get("shots")
    }
    grouped_shots = {
        str(shot)
        for group in video_groups
        for shot in group.get("shots", [])
    }
    for section_index, (title, rows) in enumerate(sections, start=1):
        nav_parts.append(f'<a href="#section-{section_index}">{esc(title.split("（")[0])}</a>')
        cards = []
        row_by_shot = {str(row[0]): row for row in rows}
        for row in rows:
            shot_count += 1
            try:
                total_seconds += int(str(row[5]).rstrip("s"))
            except ValueError:
                pass
            ap = asset_prompts.get(row[0], ("", ""))
            if ap[0]:
                confirmed += 1
            shot_id = str(row[0])
            if shot_id in groups_by_first_shot:
                group = groups_by_first_shot[shot_id]
                cards.append(render_video_group(group, ""))
            elif shot_id not in grouped_shots:
                cards.append(render_shot(row, ap, shot_elements.get(shot_id, {}), prompt_entry_by_shot.get(shot_id)))
        body_parts.append(
            f"""
            <section class="sequence" id="section-{section_index}">
              <div class="section-title">
                <span>Chapter {section_index:02d}</span>
                <h2>{esc(title)}</h2>
              </div>
              <div class="shot-grid">{''.join(cards)}</div>
            </section>
            """
        )
    nav_parts.append('<a href="#asset-prompt-library">资产提示词库</a>')
    asset_library = render_asset_prompt_library(asset_prompt_entries)
    group_count = len(video_groups)
    asset_count = len(asset_prompt_entries)
    group_seconds = 0
    for group in video_groups:
        try:
            group_seconds += int(str(group.get("duration", "0s")).rstrip("s"))
        except ValueError:
            pass

    css = """
    :root {
      --ink: #1d1d1f;
      --muted: #6e6e73;
      --paper: #f5f5f7;
      --panel: #ffffff;
      --line: #d2d2d7;
      --blue: #0071e3;
      --green: #2e7d59;
      --orange: #bf5b00;
      --shadow: rgba(0, 0, 0, 0.08);
    }
    * { box-sizing: border-box; }
    html { scroll-behavior: smooth; }
    body {
      margin: 0;
      color: var(--ink);
      background: var(--paper);
      font-family: -apple-system, BlinkMacSystemFont, "SF Pro Text", "PingFang SC", "Helvetica Neue", Arial, sans-serif;
      font-size: 14px;
    }
    .shell { width: min(1760px, calc(100vw - 28px)); margin: 0 auto; }
    header {
      padding: 18px 0 14px;
      border-bottom: 1px solid var(--line);
      position: sticky;
      top: 0;
      z-index: 10;
      background: rgba(245, 245, 247, 0.86);
      backdrop-filter: saturate(180%) blur(20px);
    }
    .brand-title {
      margin: 0;
      font-family: "Songti SC", "STSong", "Noto Serif CJK SC", "PingFang SC", serif;
      font-size: clamp(34px, 4.2vw, 58px);
      line-height: 1.05;
      letter-spacing: 0;
      font-weight: 800;
      color: #111114;
      text-shadow: 0 1px 0 #fff, 0 10px 28px rgba(0,0,0,0.10);
    }
    .brand-subtitle {
      margin-top: 4px;
      color: var(--muted); font-size: 12px;
      font-size: 14px;
      line-height: 18px;
      font-weight: 700;
      letter-spacing: 0;
    }
    h1 {
      margin: 7px 0 10px;
      font-family: -apple-system, BlinkMacSystemFont, "SF Pro Display", "PingFang SC", "Helvetica Neue", Arial, sans-serif;
      font-size: 26px;
      line-height: 28px;
      letter-spacing: 0;
      font-weight: 650;
      color: #2a2a2d;
    }
    .summary { display: flex; flex-wrap: wrap; gap: 6px; color: var(--muted); line-height: 20px; }
    .pill { border: 1px solid var(--line); border-radius: 999px; padding: 2px 8px; background: rgba(255,255,255,0.78); font-size: 12px; line-height: 18px; font-weight: 500; }
    nav { display: flex; flex-wrap: wrap; gap: 14px; margin-top: 8px; line-height: 20px; }
    nav a { color: var(--blue); text-decoration: none; padding: 0; margin: 0; font-size: 12px; line-height: 20px; font-weight: 600; }
    .shot-card {
      background: var(--panel);
      border: 1px solid rgba(210, 210, 215, 0.82);
      border-radius: 12px;
      box-shadow: 0 8px 22px var(--shadow);
      overflow: hidden;
    }
    .asset-figure img { width: 100%; height: auto; display: block; object-fit: contain; border-radius: 8px; }
    figcaption { color: var(--muted); font-size: 12px; line-height: 1.35; margin: 0; overflow-wrap: anywhere; }
    .sequence { margin: 14px 0 30px; }
    .section-title { display: flex; flex-direction: column; align-items: flex-start; gap: 5px; border-top: 1px solid var(--line); padding-top: 14px; }
    .section-title span { color: var(--blue); font-weight: 800; font-size: 16px; line-height: 20px; letter-spacing: 0.04em; }
    .section-title h2 {
      margin: 0;
      font-family: "Songti SC", "STSong", "Noto Serif CJK SC", "PingFang SC", serif;
      font-size: clamp(23px, 2.1vw, 34px);
      line-height: 1.2;
      letter-spacing: 0;
      font-weight: 800;
    }
    .shot-grid { display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 10px; margin-top: 10px; }
    .video-group {
      grid-column: 1 / -1;
      padding: 10px;
      border: 1px solid rgba(0, 113, 227, 0.22);
      border-radius: 14px;
      border-left: 4px solid var(--blue);
      background: linear-gradient(135deg, rgba(255,255,255,0.94), rgba(247,248,252,0.82));
      box-shadow: 0 10px 26px var(--shadow);
    }
    .video-group-head {
      display: flex;
      justify-content: space-between;
      align-items: flex-start;
      gap: 12px;
      padding-bottom: 8px;
      border-bottom: 1px solid var(--line);
    }
    .video-group-head span { color: #fff; background: var(--blue); font-size: 13px; line-height: 22px; font-weight: 800; letter-spacing: 0.05em; text-transform: uppercase; padding: 1px 10px; border-radius: 4px; display: inline-block; }
    .video-group-head h3 { margin: 3px 0 0; font-size: 27px; line-height: 34px; letter-spacing: 0.005em; font-family: "Songti SC", "STSong", "Noto Serif CJK SC", "PingFang SC", serif; font-weight: 700; text-shadow: 0 1px 0 rgba(255,255,255,0.9), 0 4px 14px rgba(0,0,0,0.06); }
    .video-group-meta { display: flex; flex-wrap: wrap; justify-content: flex-end; gap: 5px; max-width: 48%; }
    .video-group-meta span {
      color: var(--muted); font-size: 12px;
      border: 1px solid var(--line);
      border-radius: 999px;
      padding: 2px 7px;
      background: linear-gradient(135deg, rgba(255,255,255,0.94), rgba(247,248,252,0.82));
      white-space: nowrap;
      font-weight: 600;
    }
    .video-group-body {
      display: grid;
      grid-template-columns: minmax(0, 1fr) minmax(620px, 0.98fr);
      gap: 12px;
      margin-top: 9px;
    }
    .video-group-body section {
      border: 1px solid var(--line);
      border-radius: 10px;
      background: #fbfbfd;
      padding: 8px;
      min-width: 0;
    }
    .video-group-body h4 { margin: 0 0 6px; color: var(--blue); font-size: 14px; line-height: 18px; font-weight: 700; letter-spacing: 0.02em; }
    .video-group-body p { margin: 0; font-size: 13px; line-height: 1.55; color: #2f3033; overflow-wrap: anywhere; }
    .video-main { display: flex; flex-direction: column; gap: 8px; min-width: 0; }
    .video-group-prompt { grid-row: span 2; }
    .video-group-prompt p { white-space: pre-wrap; }
    .reference-assets { align-self: start; }
    .reference-assets .visuals { grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 12px; margin: 0; align-items: start; }
    .reference-assets .asset-figure { padding: 8px; }
    .reference-assets .asset-figure img { aspect-ratio: 16 / 9; object-fit: cover; }
    .reference-assets .asset-figure-contain img { aspect-ratio: 9 / 16; object-fit: contain; background: #eef1f5; }
    .reference-assets .asset-missing { min-height: 190px; font-size: 15px; line-height: 22px; }
    .video-group > .shot-grid { margin-top: 10px; }
    .shot-card { padding: 10px; min-width: 0; }
    .shot-head { display: flex; justify-content: space-between; gap: 8px; align-items: flex-start; border-bottom: 1px solid var(--line); padding-bottom: 7px; }
    .shot-num { color: var(--blue); font-weight: 700; font-size: 12px; }
    .shot-head h3 { margin: 2px 0 0; font-size: 17px; letter-spacing: 0.01em; font-weight: 650; }
    .duration { background: #1d1d1f; color: #fff; padding: 4px 8px; border-radius: 999px; font-size: 11px; white-space: nowrap; }
    .final-frame {
      margin: 8px 0 9px;
      padding: 8px;
      border: 1px solid rgba(0, 113, 227, 0.22);
      border-radius: 10px;
      background: linear-gradient(180deg, rgba(0,113,227,0.065), rgba(255,255,255,0.72));
    }
    .final-frame h4 { margin: 0 0 5px; color: var(--blue); font-size: 12px; line-height: 16px; }
    .final-frame p { margin: 3px 0; line-height: 1.45; color: #1d1d1f; overflow-wrap: anywhere; }
    .final-frame strong { font-weight: 700; color: #343438; }
    .final-empty { min-height: 76px; border: 1px dashed rgba(0,113,227,0.28); border-radius: 8px; background: rgba(255,255,255,0.54); }
    .shot-description {
      margin: 8px 0 9px;
      padding: 8px;
      border: 1px solid var(--line);
      border-radius: 10px;
      background: #fbfbfd;
    }
    .shot-description h4 { margin: 0 0 5px; color: #1d1d1f; font-size: 13px; line-height: 17px; }
    .shot-description p { margin: 3px 0; line-height: 1.45; color: #2f3033; overflow-wrap: anywhere; }
    .shot-description strong { font-weight: 700; color: #343438; }
    .shot-elements {
      margin: 8px 0 9px;
      padding: 8px;
      border: 1px solid rgba(0, 113, 227, 0.18);
      border-radius: 10px;
      background: rgba(0,113,227,0.045);
    }
    .shot-elements h4 { margin: 0 0 6px; color: var(--blue); font-size: 13px; line-height: 17px; }
    .shot-elements dl { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 5px; margin: 0; }
    .shot-elements div { border: 1px solid rgba(0, 113, 227, 0.14); border-radius: 8px; padding: 6px; background: rgba(255,255,255,0.72); min-width: 0; }
    .visuals { display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 6px; margin: 9px 0; }
    .asset-figure { margin: 0; border: 1px solid var(--line); border-radius: 10px; background: #fbfbfd; padding: 5px; }
    .reference-assets .asset-figure figcaption { font-size: 12px; line-height: 1.38; padding-top: 7px; }
    .asset-figure figcaption { padding: 5px 1px 0; }
    .asset-placeholder, .asset-missing { min-height: 86px; display: grid; place-items: center; color: var(--muted); border: 1px dashed var(--line); border-radius: 10px; background: #fbfbfd; padding: 10px; text-align: center; }
    .shot-meta { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 5px; margin: 0 0 8px; }
    .shot-meta div { border: 1px solid var(--line); border-radius: 8px; padding: 6px; background: #fbfbfd; min-width: 0; }
    dt { color: var(--muted); font-weight: 700; font-size: 11px; margin-bottom: 3px; }
    dd { margin: 0; color: var(--ink); line-height: 1.4; font-size: 12px; }
    .block { border-top: 1px solid var(--line); padding-top: 7px; margin-top: 7px; }
    .block h4 { margin: 0 0 4px; font-size: 13px; color: var(--blue); }
    .block p { margin: 0; line-height: 1.48; overflow-wrap: anywhere; color: #2f3033; }
    .reference-note .visuals { margin: 4px 0 7px; }
    .prompt-ref { display: flex; flex-wrap: wrap; gap: 6px; align-items: center; margin-top: 6px !important; color: var(--muted) !important; }
    .prompt-ref a { color: var(--blue); text-decoration: none; font-weight: 700; }
    .prompt-ref span { color: var(--muted); border: 1px solid var(--line); border-radius: 999px; padding: 1px 6px; background: #fff; font-size: 10px; }
    .prompt { background: rgba(0,102,204,0.055); padding: 7px; border: 1px solid rgba(0,102,204,0.18); border-radius: 10px; }
    .prompt p, .video-prompt p { white-space: pre-wrap; }
    .video-work { background: rgba(46,125,89,0.055); padding: 7px; border: 1px solid rgba(46,125,89,0.16); border-radius: 10px; }
    .video-work h4 { color: var(--green); }
    .video-prompt { background: rgba(191,91,0,0.055); padding: 7px; border: 1px solid rgba(191,91,0,0.16); border-radius: 10px; }
    .video-prompt h4 { color: var(--orange); }
    .primary-video-prompt { border-top: 0; margin-top: 8px; }
    .video-assets {
      grid-column: 1 / -1;
      margin-top: 0;
      padding: 14px;
      border: 1px solid rgba(46,125,89,0.22);
      border-radius: 14px;
      background: linear-gradient(135deg, rgba(244,252,248,0.94), rgba(255,255,255,0.86));
      box-shadow: inset 0 1px 0 rgba(255,255,255,0.8);
    }
    .video-main .video-assets { margin-top: 0; }
    .video-assets-head { display: flex; justify-content: space-between; align-items: center; gap: 10px; margin-bottom: 12px; }
    .video-assets-head h4 { margin: 0; color: var(--green); font-size: 18px; line-height: 24px; font-weight: 800; letter-spacing: 0.01em; }
    .video-assets-head span { color: var(--muted); border: 1px solid var(--line); border-radius: 999px; background: rgba(255,255,255,0.9); padding: 3px 10px; font-size: 12px; line-height: 18px; white-space: nowrap; font-weight: 700; }
    .video-slot {
      width: 100%;
      aspect-ratio: 16 / 9;
      min-height: 210px;
      border: 1px dashed rgba(46,125,89,0.34);
      border-radius: 10px;
      background:
        linear-gradient(135deg, rgba(255,255,255,0.9), rgba(245,245,247,0.82)),
        repeating-linear-gradient(45deg, rgba(46,125,89,0.05) 0, rgba(46,125,89,0.05) 8px, transparent 8px, transparent 16px);
      display: grid;
      place-items: center;
      text-align: center;
      padding: 14px;
      color: var(--muted); font-size: 12px;
    }
    .video-main .video-slot { min-height: 330px; }
    .video-slot strong { display: block; color: var(--ink); font-size: 16px; line-height: 22px; margin-bottom: 6px; letter-spacing: 0.02em; }
    .video-slot span { display: block; line-height: 1.45; }
    .video-candidate-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(min(100%, 420px), 1fr)); gap: 14px; }
    .video-candidate {
      margin: 0;
      border: 1px solid rgba(46,125,89,0.22);
      border-radius: 14px;
      background: rgba(255,255,255,0.82);
      padding: 10px;
      min-width: 0;
      box-shadow: 0 10px 24px rgba(0,0,0,0.08);
    }
    .video-candidate video {
      width: 100%;
      aspect-ratio: 16 / 9;
      display: block;
      border-radius: 11px;
      background: #111114;
    }
    .video-candidate figcaption {
      display: flex;
      flex-wrap: wrap;
      justify-content: space-between;
      gap: 6px;
      padding: 9px 2px 0;
      color: var(--muted);
      font-size: 12px;
      line-height: 1.35;
    }
    .video-candidate figcaption strong { color: var(--green); font-size: 14px; line-height: 18px; }
    .video-candidate figcaption span { overflow-wrap: anywhere; }
    .video-missing {
      border: 1px dashed rgba(46,125,89,0.34);
      border-radius: 10px;
      background: rgba(255,255,255,0.74);
      padding: 12px;
      color: var(--muted);
    }
    .video-missing strong { display: block; color: var(--green); margin-bottom: 4px; }
    .pending { color: var(--muted); }
    .asset-library { margin: 18px 0 36px; }
    .asset-library-note {
      margin-top: 8px;
      color: var(--muted); font-size: 12px;
      border: 1px solid var(--line);
      border-radius: 10px;
      background: linear-gradient(135deg, rgba(255,255,255,0.94), rgba(247,248,252,0.82));
      padding: 8px;
      line-height: 1.45;
    }
    .asset-category { margin-top: 12px; }
    .asset-category > h3 { margin: 0 0 8px; font-size: 15px; line-height: 20px; letter-spacing: 0; }
    .asset-prompt-grid { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 10px; margin-top: 10px; }
    .asset-prompt-card {
      border: 1px solid rgba(210, 210, 215, 0.82);
      border-radius: 12px;
      background: var(--panel);
      box-shadow: 0 8px 22px var(--shadow);
      padding: 10px;
      min-width: 0;
    }
    .asset-prompt-head { display: flex; justify-content: space-between; gap: 10px; align-items: flex-start; border-bottom: 1px solid var(--line); padding-bottom: 7px; }
    .asset-prompt-head span { color: var(--blue); font-size: 10px; font-weight: 700; }
    .asset-prompt-head h3 { margin: 2px 0 0; font-size: 15px; line-height: 20px; }
    .shot-tags { display: flex; flex-wrap: wrap; justify-content: flex-end; gap: 4px; }
    .shot-tags span { color: var(--muted); border: 1px solid var(--line); border-radius: 999px; padding: 1px 6px; background: #fbfbfd; white-space: nowrap; }
    .asset-prompt-body { margin-top: 8px; }
    .asset-prompt-body .visuals { grid-template-columns: repeat(auto-fit, minmax(132px, 1fr)); margin: 0 0 8px; }
    .asset-prompt-body p { margin: 0; white-space: pre-wrap; line-height: 1.5; color: #2f3033; overflow-wrap: anywhere; }
    .asset-empty { border: 1px dashed var(--line); border-radius: 12px; background: rgba(255,255,255,0.64); color: var(--muted); min-height: 76px; display: grid; place-items: center; }
    code { font-family: "SFMono-Regular", Menlo, monospace; font-size: 10px; }
    @media (max-width: 1280px) {
      .shot-grid { grid-template-columns: repeat(2, minmax(0, 1fr)); }
      .video-group-body { grid-template-columns: repeat(2, minmax(0, 1fr)); }
    }
    @media (max-width: 820px) {
      .shot-grid { grid-template-columns: 1fr; }
      .asset-prompt-grid { grid-template-columns: 1fr; }
      .shell { width: min(100% - 18px, 1760px); }
      header { position: static; }
      .shot-meta { grid-template-columns: 1fr; }
      .video-group-head { flex-direction: column; }
      .video-group-meta { justify-content: flex-start; max-width: none; }
      .video-group-body { grid-template-columns: 1fr; }
      .video-candidate-grid { grid-template-columns: 1fr; }
      .shot-elements dl { grid-template-columns: 1fr; }
    }
    """

    html_doc = f"""<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>诛仙后传·红鸾笑｜第1集草庙村制作脚本</title>
  <style>{css}</style>
</head>
<body>
  <header>
    <div class="shell">
      <div class="brand-title">诛仙后传·红鸾笑</div>
      <div class="brand-subtitle">Episode 1 Production Script</div>
      <h1>第1集「草庙村」制作脚本</h1>
      <div class="summary">
        <span class="pill">{group_count} 个视频段</span>
        <span class="pill">总时长约 {group_seconds}s</span>
        <span class="pill">已确认资产 {asset_count} 张</span>
        <span class="pill">交付格式：HTML</span>
      </div>
      <nav>{''.join(nav_parts)}</nav>
    </div>
  </header>
  <main class="shell">
    {''.join(body_parts)}
    {asset_library}
  </main>
</body>
</html>
"""
    OUT.write_text(html_doc, encoding="utf-8")
    print(OUT)

    # Also publish to docs/ for GitHub Pages
    DOCS_OUT.parent.mkdir(parents=True, exist_ok=True)
    docs_assets = DOCS_OUT.parent / "assets"
    if docs_assets.exists():
        shutil.rmtree(docs_assets)
    shutil.copytree(PUBLISH_ASSETS, docs_assets)
    DOCS_OUT.write_text(html_doc, encoding="utf-8")
    print(DOCS_OUT)


if __name__ == "__main__":
    main()
