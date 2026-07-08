# 01 · HTML 制作脚本格式

> 基于第1集「草庙村」制作脚本 HTML 沉淀。整套结构已在 VG-01 跑通过 Seedance 2.0 试验，结构稳定。
> 每集一个 HTML，第2/3集复用同一结构，按"集 → VG → 分镜"三档组织。

---

## 一、文件位置与命名

```
制作脚本/
├── 第1集-草庙村/
│   ├── 第1集-草庙村-制作脚本.html     ← 正式交付 HTML（必备）
│   ├── 第1集-草庙村-90秒版-分镜头脚本.xlsx  ← Excel 备份（仅过渡保留）
│   └── assets/                          ← HTML 直接引用的资产副本（场景图、角色母版等）
├── 第2集-归山/
│   ├── 第2集-归山-制作脚本.html
│   └── assets/
└── 第3集-红鸾/
    ├── 第3集-红鸾-制作脚本.html
    └── assets/
```

## 二、页面整体结构

```
<header>      品牌区（剧名 / 集名 / summary pills / 章节导航）
<main>
  <section class="sequence" id="section-N">
    <div class="section-title">
      <span>Chapter NN</span>
      <h2>幕名 · （VG-范围，共秒数）</h2>
    </div>
    <div class="shot-grid">
      <article class="video-group" id="vg-NN">   ← 每个 VG 一张卡
        ...
      </article>
    </div>
  </section>
</main>
```

## 三、VG 视频段卡片（核心）

每个 VG 段是 HTML 的最小内容单位，由 **头部 + 双栏主体 + 资源区** 组成：

```html
<article class="video-group" id="vg-01">
  <div class="video-group-head">
    <div>
      <span>VG-01</span>
      <h3>小竹峰起念与出门</h3>
    </div>
    <div class="video-group-meta">
      <span>镜1、镜2</span>
      <span>14s</span>
      <span>Seedance 2.0 一次生成试验</span>
    </div>
  </div>

  <div class="video-group-body">
    <div class="video-main">
      <section class="video-assets"> ... </section>     <!-- 合并视频素材占位 -->
      <section class="video-prompt video-group-prompt"> ... </section>  <!-- 合并视频生成提示词 -->
    </div>
    <section class="reference-assets"> ... </section>     <!-- 参考资产图 -->
  </div>

  <section class="prompt-library"> ... </section>          <!-- 资产提示词库索引 -->
</article>
```

## 四、各字段规范

### 4.1 头部（`.video-group-head`）

| 元素 | 内容 | 备注 |
|------|------|------|
| `<span>` | VG 编号（VG-01） | 大写、零填充 |
| `<h3>` | VG 标题（动宾短语，如"小竹峰起念与出门"） | 简短，3-8 字 |
| `.video-group-meta` | 覆盖镜号、时长、生成方式 | pill 标签 |

### 4.2 合并视频素材占位（`.video-assets`）

固定结构：

```html
<section class="video-assets">
  <div class="video-assets-head">
    <h4>合并视频素材</h4>
    <span>主素材</span>
  </div>
  <div class="video-slot">
    <div>
      <strong>待生成 / Seedance</strong>
      <span>16:9 视频素材占位，可追加多版本出片后人工剪辑选优</span>
    </div>
  </div>
</section>
```

视频素材回填时，把 `<div class="video-slot">` 整块替换为 `<video>` 或 `<img>` 即可。

**视频候选布局标准**：所有候选视频统一用 `.video-candidate-grid` 容器，按 `repeat(2, minmax(0, 1fr))` **2 列等宽**展示，每个视频保持 16:9 比例。候选数无论 1 个、3 个、6 个均按此规则；最后一行单数时独居一行（grid 自动行为），不做跨列特例处理。这样后续 VG 段无论生成多少候选都视觉一致。

### 4.3 合并视频生成提示词（`.video-prompt`）

固定结构：

```html
<section class="video-prompt video-group-prompt">
  <h4>合并视频生成提示词（可直接复制）</h4>
  <p>【基本设定】
 人物：...
 场景：...
 声音：...

【氛围与面质】
 风格核心：...
 视觉基调：...
 色彩与影调：...

分镜一：00:00-00:04
 景别：...
 构图：...
 机位与镜头：...
 运镜手法：...
 画面内容：...
 声音：...

分镜二：00:04-00:07
 ...</p>
</section>
```

提示词内部结构详细见 `03_VG视频段提示词模板.md`。

### 4.4 参考资产（`.reference-assets`）

```html
<section class="reference-assets">
  <h4>参考资产</h4>
  <div class="visuals">
    <figure class="asset-figure">
      <img src="assets/草庙村_青云山云海御剑建立镜头.png" alt="...">
      <figcaption>红鸾笑/场景资产/草庙村_青云山云海御剑建立镜头.png</figcaption>
    </figure>
    <!-- 多个 figure 横向排列，16:9 适配 -->
  </div>
</section>
```

- 图片相对路径：`assets/<图名>`
- figcaption 必须写完整原文件路径，方便人工核对

### 4.5 资产提示词库（`.prompt-library`）

用于记录本 VG 段用到的所有资产原始提示词，便于跨段复用。结构示例：

```html
<section class="prompt-library">
  <h4>资产提示词库</h4>
  <ul>
    <li>
      <strong>陆雪琪四视图角色母版 v2</strong>
      <span>角色资产</span>
      <a href="../../角色资产/陆雪琪/角色设定.md#00">查看完整提示词 →</a>
    </li>
    <li>
      <strong>小竹峰外景（竹林溪桥仙门雅舍清晨残灯）</strong>
      <span>场景资产</span>
      <a href="../../场景资产/场景母图提示词技巧.md#小竹峰外景">查看完整提示词 →</a>
    </li>
  </ul>
</section>
```

- 用 `<a>` 锚点引用同仓库其它 md 文档，避免重复维护
- 分类标签：场景 / 角色 / 道具

## 五、命名约定

| 类型 | 命名规则 | 示例 |
|------|----------|------|
| HTML 文件 | `<集名>-制作脚本.html` | `第1集-草庙村-制作脚本.html` |
| VG 编号 | `VG-NN`（NN 为 2 位数字） | `VG-01`、`VG-09` |
| 资产文件 | `<地点/角色>_<要点>_<版本>.png/jpg` | `草庙村_青云山云海御剑建立镜头.png` |
| 归档副本 | 同名放 `assets/` 子目录 | `assets/草庙村_青云山云海御剑建立镜头.png` |

## 六、常见错误避免

- ❌ 不要在 `<p>` 内混 `<img>` —— 提示词段落必须纯文本，方便复制
- ❌ 不要把参考图绝对路径写进 HTML —— 一律相对路径
- ❌ 不要把多个 VG 写到一个卡片里 —— 一个 article 一个 VG
- ❌ 不要漏写 `id="vg-NN"` —— 顶部导航锚点依赖它
- ❌ 不要在新集里私自改字段名 —— 字段稳定是模板的核心价值

## 七、视觉规范（CSS 摘要）

字体：

```css
--ink: #1d1d1f;
--paper: #f5f5f7;
--blue: #0071e3;
--green: #2e7d59;
--orange: #bf5b00;
--line: #d2d2d7;
```

字号基准：body 14px，section h2 23-34px（clamp），VG h3 27px（衬线粗体），正文 12-13px。
卡片圆角：10-14px，阴影：`0 8px 22px rgba(0,0,0,0.08)`。

完整 CSS 模板见 `第1集-草庙村-制作脚本.html` 头部 `<style>` 块，新集直接复制后小幅调整即可。