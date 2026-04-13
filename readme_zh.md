# 智能教育及行业发展研究

> 研究生课程仓库 · 2026 年春季 · 人机协同学习研究组

---

## 📋 课程概览

本仓库服务于研究生课程 **《智能教育及行业发展研究》**。它提供了一个结构化工作空间，用于管理课程资源、小组讨论、阶段作业，以及贯穿学期的智能教育系统开发项目。

本小组的研究重点为：**中国高等教育场景下教育技术中的人机协同学习范式**。

---

## 👥 团队成员

| 姓名 | 角色 | 职责 |
|------|------|------|
| 成员 1 | 项目负责人 | 架构设计、项目协调 |
| 成员 2 | 研究负责人 | 文献综述、理论框架 |
| 成员 3 | 开发负责人 | 系统开发、代码评审 |
| 成员 4 | 文档负责人 | 文档维护、讨论组织 |

> _请将此表更新为真实姓名和 GitHub 账号。_

---

## 🗂️ 仓库结构

```text
Research-on-Intelligent-Education-and-Industry-Development/
│
├── README.md                          # 仓库总览（英文）
├── readme_zh.md                       # 仓库总览（中文）
├── .gitignore                         # 全局忽略规则
│
├── resources/                         # 课程学习资源
│   ├── README.md                      # 资源管理规则与命名规范
│   ├── module-01-intro-to-intelligent-education/
│   ├── module-02-ai-in-education-systems/
│   ├── module-03-human-computer-collaborative-learning/
│   ├── module-04-educational-data-governance/
│   └── module-05-industry-development-and-applications/
│
├── discussion/                        # 小组讨论区
│   ├── README.md                      # 讨论规则与导出流程
│   ├── main-discussion.md             # 主讨论线程索引
│   ├── export_discussion.py           # 讨论内容导出为格式化 .md 的脚本
│   ├── topic-01-human-computer-collaborative-learning/
│   ├── topic-02-educational-data-governance/
│   ├── topic-03-ai-tools-in-higher-education/
│   └── topic-04-industry-development-trends/
│
├── assignments/                       # 课程作业
│   ├── README.md                      # 提交要求与评审流程
│   ├── phase-1-literature-review/
│   ├── phase-2-research-proposal/
│   └── phase-3-final-report/
│
└── project/                           # 智能教育系统项目
    ├── PROJECT_README.md              # 项目概览与快速开始
    ├── roadmap.md                     # 项目路线图与里程碑
    ├── CONTRIBUTING.md                # 贡献指南
    ├── CODE_OF_CONDUCT.md             # 行为准则
    ├── requirements.txt               # Python 依赖
    ├── setup.py                       # 包安装配置
    ├── .gitignore                     # 项目级忽略规则
    ├── src/                           # 源代码
    │   ├── collaborative_learning/    # 人机协同学习模块
    │   ├── knowledge_graph/           # 知识图谱模块
    │   ├── recommendation/            # 自适应推荐模块
    │   └── utils/                     # 通用工具
    ├── docs/                          # 技术文档
    ├── tests/                         # 单元测试
    ├── data/                          # 示例数据集（不含敏感数据）
    └── models/                        # 预训练模型配置（不含权重）
```

---

## 🚀 快速开始

### 克隆仓库

```bash
git clone https://github.com/chaogao512/Research-on-Intelligent-Education-and-Industry-Development.git
cd Research-on-Intelligent-Education-and-Industry-Development
```

### 配置项目环境

```bash
cd project
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 运行项目

```bash
python -m src.main
```

---

## 📚 区域说明

| 区域 | 说明 | 链接 |
|------|------|------|
| 课程资源 | 按模块组织的课件、论文与笔记 | [resources/README.md](resources/README.md) |
| 小组讨论 | 异步讨论线程与导出工具 | [discussion/README.md](discussion/README.md) |
| 作业管理 | 提交模板与评审流程 | [assignments/README.md](assignments/README.md) |
| 项目开发 | 智能教育系统开发内容 | [project/PROJECT_README.md](project/PROJECT_README.md) |

---

## 🤝 协作规范

1. **分支命名**：`feature/<area>-<short-description>`（例如：`feature/project-add-recommender`）
2. **提交信息**：采用 [Conventional Commits](https://www.conventionalcommits.org/) 规范
   - `feat:`, `fix:`, `docs:`, `refactor:`, `test:`, `chore:`
3. **Pull Request**：所有变更合并到 `main` 前至少需要 1 位同伴评审
4. **文件命名**：使用小写加连字符（例如：`research-proposal-v1.md`）
5. **大文件限制**：不提交大于 50 MB 的文件；请使用 Git LFS 或外部存储
6. **敏感信息**：严禁提交 API Key、密码或个人隐私数据

详细规范见 [project/CONTRIBUTING.md](project/CONTRIBUTING.md)。

---

## 📄 许可说明

本仓库仅用于学术课程。所有课程资料的知识产权归各作者与授课教师所有。`project` 目录下开发的代码，除另有说明外，采用 MIT License。

---

_最后更新：2026 年 4 月_
