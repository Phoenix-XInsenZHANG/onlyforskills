# E2E 测试最佳实践：Playwright 与 Newman 完整指南

> 适用于全栈应用（含 UI 和 API 层）的现代端到端测试策略  
> 更新时间：2025–2026

---

## 目录

1. [测试策略总览](#1-测试策略总览)
2. [Playwright UI 测试最佳实践](#2-playwright-ui-测试最佳实践)
3. [Newman / Postman API 测试最佳实践](#3-newman--postman-api-测试最佳实践)
4. [两者集成与 CI/CD 流水线](#4-两者集成与-cicd-流水线)
5. [Claude AI 加速测试生成与维护](#5-claude-ai-加速测试生成与维护)
6. [项目模板使用说明](#6-项目模板使用说明)

---

## 1. 测试策略总览

### 测试金字塔

全栈应用的 E2E 测试应遵循经典的测试金字塔原则：

| 层级 | 工具 | 占比 | 运行速度 | 维护成本 |
|------|------|------|----------|----------|
| 单元测试 | Jest / Vitest | ~70% | 毫秒级 | 低 |
| API / 集成测试 | Newman (Postman CLI) | ~20% | 秒级 | 中 |
| UI / E2E 测试 | Playwright | ~10% | 分钟级 | 高 |

**核心原则**：尽可能把覆盖率推到金字塔底层。API 测试比 UI 测试快 10–100 倍，UI 测试只用来验证"非用真实浏览器不可"的关键用户路径。

### 执行顺序

**永远先跑 API 测试，再跑 UI 测试。** 如果后端 API 挂了，UI 测试会超时并报出令人困惑的错误。API 先行能在秒级发现后端问题，节省大量 CI 时间。

---

## 2. Playwright UI 测试最佳实践

### 2.1 项目结构

```
tests/ui/
├── tests/                  # 按功能域组织测试文件
│   ├── auth/
│   │   └── auth.setup.ts   # 认证 setup project
│   ├── checkout/
│   │   └── checkout.spec.ts
│   └── dashboard/
│       └── dashboard.spec.ts
├── pages/                  # Page Object Model
│   ├── BasePage.ts
│   ├── LoginPage.ts
│   └── CheckoutPage.ts
├── fixtures/
│   └── fixtures.ts         # 自定义 fixtures
├── utils/
│   └── helpers.ts
├── data/
│   └── testData.json
└── playwright.config.ts
```

**关键规范**：
- 测试文件按**功能域**分目录（`checkout/`、`auth/`），不按测试人员或迭代分
- 文件命名：`create-order-happy-path.spec.ts`（描述性）
- Page Object：`PascalCase`（`LoginPage.ts`）
- 工具函数：`camelCase`（`dateUtils.ts`）

### 2.2 Page Object Model + Fixtures 集成

现代 Playwright 的 POM 通过 `test.extend()` 注入到 fixture 系统中，测试代码读起来就像用户故事：

```typescript
// pages/LoginPage.ts
import { type Page, type Locator } from '@playwright/test';

export class LoginPage {
  readonly page: Page;
  readonly emailInput: Locator;
  readonly passwordInput: Locator;
  readonly submitButton: Locator;
  readonly errorMessage: Locator;

  constructor(page: Page) {
    this.page = page;
    // ✅ 使用语义化定位器，优先级：getByRole > getByLabel > getByText > getByTestId
    this.emailInput = page.getByLabel('邮箱');
    this.passwordInput = page.getByLabel('密码');
    this.submitButton = page.getByRole('button', { name: '登录' });
    this.errorMessage = page.getByRole('alert');
  }

  async goto() {
    await this.page.goto('/login');
  }

  async login(email: string, password: string) {
    await this.emailInput.fill(email);
    await this.passwordInput.fill(password);
    await this.submitButton.click();
  }
}
```

```typescript
// fixtures/fixtures.ts
import { test as base, expect } from '@playwright/test';
import { LoginPage } from '../pages/LoginPage';
import { CheckoutPage } from '../pages/CheckoutPage';

type MyFixtures = {
  loginPage: LoginPage;
  checkoutPage: CheckoutPage;
};

export const test = base.extend<MyFixtures>({
  loginPage: async ({ page }, use) => {
    await use(new LoginPage(page));
  },
  checkoutPage: async ({ page }, use) => {
    await use(new CheckoutPage(page));
  },
});
export { expect };
```

```typescript
// tests/checkout/checkout.spec.ts
import { test, expect } from '../../fixtures/fixtures';

test('用户可以成功完成结账', async ({ checkoutPage }) => {
  await checkoutPage.goto();
  await checkoutPage.addItem('商品A');
  await checkoutPage.fillShippingInfo({ name: '张三', address: '北京市朝阳区' });
  await checkoutPage.submitOrder();
  await expect(checkoutPage.successMessage).toBeVisible();
});
```

**定位器优先级（官方推荐）**：`getByRole` → `getByLabel` → `getByPlaceholder` → `getByText` → `getByTestId`

⚠️ **避免使用 CSS 类选择器**——样式变更时会导致测试大面积失败。断言（assertions）应放在测试代码中，不要放在 Page Object 里。

### 2.3 认证状态复用（Setup Project）

Playwright 的 **Setup Project 模式** 只登录一次，将 `storageState` 保存为 JSON，后续所有测试复用该会话——每个测试可节省 5–15 秒的登录时间。

```typescript
// tests/auth/auth.setup.ts
import { test as setup } from '@playwright/test';

const authFile = 'playwright/.auth/user.json';

setup('认证', async ({ page }) => {
  await page.goto('/login');
  await page.getByLabel('邮箱').fill('test@example.com');
  await page.getByLabel('密码').fill('password123');
  await page.getByRole('button', { name: '登录' }).click();
  await page.waitForURL('/dashboard');
  await page.context().storageState({ path: authFile });
});
```

在 `playwright.config.ts` 中，其他 project 声明 `dependencies: ['setup']` 和 `storageState` 即可。

**多角色场景**：为不同角色创建独立的认证文件（`admin.json`、`user.json`），在 fixtures 中为每个角色启动独立的浏览器上下文。

⚠️ 始终将 `playwright/.auth` 加入 `.gitignore`。

### 2.4 测试隔离、并行与分片

Playwright 为每个测试创建独立的浏览器上下文（cookies、localStorage、session 完全隔离）。

```typescript
// playwright.config.ts 关键配置
fullyParallel: true,        // 所有文件的所有测试并行执行
workers: process.env.CI ? 2 : undefined,  // CI 限制 worker 数，本地用满 CPU
```

**CI 分片（跨机器分布）**：
```bash
npx playwright test --shard=1/4   # 机器 1
npx playwright test --shard=2/4   # 机器 2
npx playwright test --shard=3/4   # 机器 3
npx playwright test --shard=4/4   # 机器 4
```

**隔离原则**：
- 绝不通过全局变量共享状态
- 使用 `testInfo.workerIndex` 或 Faker.js 生成唯一测试数据
- 除非测试真的有顺序依赖，否则不要使用 `test.describe.configure({ mode: 'serial' })`

### 2.5 消除 Flaky 测试

**配置重试**（仅 CI 环境）：
```typescript
retries: process.env.CI ? 2 : 0,
```

**Flaky 测试的常见原因与对策**：

| 原因 | 对策 |
|------|------|
| 竞态条件 | 使用 web-first 断言 `await expect(locator).toBeVisible()` 自动重试 |
| 硬编码等待 | ❌ 永远不用 `waitForTimeout()`，用有意义的等待条件 |
| 第三方 API 不稳定 | 用 `page.route()` Mock 外部 API 请求 |
| 状态污染 | 保证每个测试独立运行，不依赖其他测试的副作用 |
| 选择器脆弱 | 使用语义化定位器而非 CSS class |

**提前发现 flaky 测试**：
```bash
npx playwright test --repeat-each=5  # 合并前本地跑 5 遍
```

**失败时保留诊断证据**：
```typescript
use: {
  trace: 'on-first-retry',          // 首次重试时记录完整 trace
  screenshot: 'only-on-failure',     // 失败时截图
  video: 'retain-on-failure',        // 失败时保留视频
}
```

用 `@flaky` 标签将不稳定测试隔离到非阻塞 CI 任务中。团队目标：flaky 率低于 2%。

### 2.6 视觉回归测试

```typescript
// 像素级截图比较
await expect(page).toHaveScreenshot('checkout-page.png', {
  maxDiffPixels: 50,
  animations: 'disabled',  // 禁用动画确保稳定性
});

// 元素级截图（更精确）
await expect(page.locator('.product-card')).toHaveScreenshot();
```

**最佳实践**：
- 在 CI 中使用 Playwright Docker 镜像生成基线（保证渲染一致性）
- 遮蔽动态内容（时间戳、广告位）
- 元素级截图比全页面截图更精确、更少误报

### 2.7 跨浏览器与报告

```typescript
// playwright.config.ts 项目配置
projects: [
  { name: 'setup', testMatch: /.*\.setup\.ts/ },
  {
    name: 'chromium',
    use: { ...devices['Desktop Chrome'], storageState: 'playwright/.auth/user.json' },
    dependencies: ['setup'],
  },
  {
    name: 'firefox',
    use: { ...devices['Desktop Firefox'], storageState: 'playwright/.auth/user.json' },
    dependencies: ['setup'],
  },
  {
    name: 'webkit',
    use: { ...devices['Desktop Safari'], storageState: 'playwright/.auth/user.json' },
    dependencies: ['setup'],
  },
  // 移动端视口
  {
    name: 'mobile-chrome',
    use: { ...devices['Pixel 5'], storageState: 'playwright/.auth/user.json' },
    dependencies: ['setup'],
  },
]
```

**报告策略**：
- **HTML Reporter**：主要调试工具，本地开发用
- **GitHub Annotations**：PR 反馈集成
- **JUnit XML**：CI 集成的通用格式
- **Trace Viewer**：在 `trace.playwright.dev` 打开（本地运行，不上传数据）

### 2.8 完整的 playwright.config.ts

见项目模板中的 `tests/ui/playwright.config.ts` 文件——包含生产就绪的完整配置。

---

## 3. Newman / Postman API 测试最佳实践

### 3.1 Collection 组织结构

按**域/资源**组织 Postman Collection，嵌套文件夹反映 API 层级：

```
Collection: MyApp API Tests
├── 🔐 Authentication
│   ├── POST Login
│   ├── POST Register
│   └── POST Refresh Token
├── 👤 Users
│   ├── GET List Users
│   ├── GET User By ID
│   ├── POST Create User
│   ├── PUT Update User
│   └── DELETE User
├── 🛒 Orders
│   ├── GET List Orders
│   ├── POST Create Order
│   └── PATCH Update Order Status
└── 🔧 Health Check
    └── GET Health
```

**命名规范**：`HTTP方法 资源 - 动作描述`，如 `POST User - Create New`。

### 3.2 变量管理

Postman 变量优先级（从高到低）：`local` → `data` → `environment` → `collection` → `global`

| 变量类型 | 用途 | 示例 |
|----------|------|------|
| Environment | 环境间变化的值 | `base_url`, `auth_token` |
| Collection | 集合内的常量 | `api_version`, `timeout` |
| Global | 跨集合共享 | `common_headers` |
| Data | 数据驱动测试 | CSV/JSON 文件中的行 |

**Newman 变量传递**：
```bash
newman run collection.json \
  -e staging.json \
  --env-var "base_url=https://api.staging.com" \
  --env-var "api_key=secret123"
```

⚠️ **关键注意**：Newman 只读取环境文件的 **initial/shared value**，不读 Postman 的 current value。始终使用 shared value 或 `--env-var` 覆盖。

### 3.3 脚本执行流程与模式

执行顺序：`Collection Pre-request` → `Folder Pre-request` → `Request Pre-request` → **请求发送** → `Collection Tests` → `Folder Tests` → `Request Tests`

**集合级自动刷新 JWT Token**：

```javascript
// Collection-level pre-request script
const tokenExpiry = pm.collectionVariables.get("token_expiry");
if (!tokenExpiry || Date.now() > parseInt(tokenExpiry)) {
  pm.sendRequest({
    url: pm.environment.get("base_url") + "/auth/login",
    method: 'POST',
    header: { 'Content-Type': 'application/json' },
    body: {
      mode: 'raw',
      raw: JSON.stringify({
        email: pm.environment.get("auth_email"),
        password: pm.environment.get("auth_password")
      })
    }
  }, (err, response) => {
    if (!err) {
      const json = response.json();
      pm.collectionVariables.set("auth_token", json.token);
      pm.collectionVariables.set("token_expiry",
        (Date.now() + 3500000).toString()); // ~58 分钟
    }
  });
}
```

**集合级通用断言（DRY 模式）**：
```javascript
// Collection-level test script — 对所有请求自动执行
pm.test("响应是有效 JSON", () => { pm.response.json(); });
pm.test("无服务器错误", () => { pm.expect(pm.response.code).to.be.below(500); });
pm.test("响应时间 < 5s", () => { pm.expect(pm.response.responseTime).to.be.below(5000); });
```

### 3.4 请求链接与数据驱动测试

**请求链接**：从响应中提取数据并传递给下一个请求：

```javascript
// POST Create User 的 test script
const response = pm.response.json();
pm.collectionVariables.set("created_user_id", response.id);
// 后续 GET User By ID 使用 {{created_user_id}}
```

**流程控制**：
```javascript
postman.setNextRequest("Request Name"); // 跳转到指定请求
postman.setNextRequest(null);            // 终止执行（防止死循环！）
```

**数据驱动测试**：
```bash
# test-data.csv
email,password,expected_status
valid@test.com,pass123,200
invalid@test.com,wrong,401
,pass123,400

newman run collection.json -d test-data.csv -n 3 --delay-request 200
```

在脚本中通过 `pm.iterationData.get('email')` 访问每行数据。

### 3.5 JSON Schema 验证

使用 **Ajv**（不要用已废弃的 tv4）做契约验证：

```javascript
const schema = {
  type: "object",
  properties: {
    id: { type: "integer" },
    name: { type: "string", minLength: 1 },
    email: { type: "string", format: "email" },
    roles: {
      type: "array",
      items: { type: "string" },
      minItems: 1
    }
  },
  required: ["id", "name", "email"],
  additionalProperties: false  // ⚠️ 严格模式：拒绝未知字段
};

pm.test("响应匹配 JSON Schema", () => {
  pm.response.to.have.jsonSchema(schema);
});
```

### 3.6 Newman CLI 完整命令

```bash
newman run collection.json \
  -e production.json \           # 环境文件
  -g globals.json \              # 全局变量
  -d testdata.csv \              # 数据驱动文件
  -n 3 \                         # 迭代次数
  --delay-request 500 \          # 请求间延迟（ms）
  --timeout-request 30000 \      # 单请求超时（ms）
  --bail \                       # 首次失败即停止
  --reporters cli,htmlextra,junit \
  --reporter-htmlextra-export reports/newman-report.html \
  --reporter-junit-export reports/newman-junit.xml
```

**HTMLExtra Reporter**（最流行的第三方报告器）：提供交互式仪表盘、暗色主题、分页和失败过滤。

**Newman 编程接口（Node.js）**：
```javascript
const newman = require('newman');

newman.run({
  collection: require('./collection.json'),
  environment: require('./staging.json'),
  reporters: ['cli', 'htmlextra'],
}, (err, summary) => {
  if (summary.run.failures.length) {
    console.error('测试失败:', summary.run.failures.length);
    process.exit(1);
  }
});
```

### 3.7 Newman 的局限性

- **无原生 OAuth 2.0**：需在 pre-request 脚本中手动获取 token
- **无 Postman 包库**：不能使用 Postman 的共享库功能
- **串行执行**：请求只能顺序执行，不支持并行
- **负载测试有限**：并发量大时（1000+ 用户），应使用 k6 或 JMeter

### 3.8 2025 年 Postman 更新

- `pm.require('npm:package@version')` 支持在脚本中引入外部 npm 包
- `pm.execution.runRequest()` 支持可复用的请求调用
- Postman Agent Mode 提供 AI 驱动的测试自动生成
- Newman 持续维护（~7.2k GitHub Stars），但 Postman CLI 是云端连接的推荐替代

---

## 4. 两者集成与 CI/CD 流水线

### 4.1 统一项目结构

```
project-root/
├── tests/
│   ├── api/                        # Newman/Postman 测试
│   │   ├── collections/            # .postman_collection.json
│   │   ├── environments/           # .postman_environment.json
│   │   └── data/                   # 数据驱动 CSV/JSON
│   ├── ui/                         # Playwright 测试
│   │   ├── tests/
│   │   ├── pages/
│   │   ├── fixtures/
│   │   └── playwright.config.ts
│   └── shared/
│       ├── test-config.json        # 单一事实来源
│       └── generate-newman-env.js  # 共享配置 → Newman 环境
├── scripts/
│   └── merge-reports.js            # 合并 JUnit 报告
├── .github/workflows/
│   └── e2e-tests.yml
└── package.json
```

共享 `test-config.json` 存放所有环境的 baseURL、API URL 和凭证占位符。`generate-newman-env.js` 在运行时将共享配置转换为 Newman 兼容的环境 JSON，消除配置漂移。

### 4.2 分层执行策略

| 触发时机 | 执行范围 | 预计耗时 |
|----------|----------|----------|
| Pull Request | Lint + 单元测试 + API Smoke (`--folder Smoke`) | < 5 分钟 |
| 合并到 main | 完整 API → UI Smoke (`--grep @smoke`) | < 15 分钟 |
| 每日定时（Nightly） | 完整 API → 完整 UI（全浏览器） | < 60 分钟 |
| 发版前 | 完整 API → 完整 UI → 性能 → 安全 | < 2 小时 |

### 4.3 GitHub Actions 完整流水线

```yaml
name: E2E Tests
on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

env:
  TEST_ENV: staging

jobs:
  # ========== 第一阶段：API 测试 ==========
  api-tests:
    name: API Tests (Newman)
    runs-on: ubuntu-latest
    timeout-minutes: 15
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: 20
          cache: 'npm'
      - run: npm ci
      - run: npm install -g newman newman-reporter-htmlextra
      - run: node tests/shared/generate-newman-env.js
      - name: 运行 API 测试
        run: |
          newman run tests/api/collections/api-tests.postman_collection.json \
            -e tests/api/environments/staging.generated.json \
            --reporters cli,junit,htmlextra \
            --reporter-junit-export reports/newman-junit.xml \
            --reporter-htmlextra-export reports/newman-report.html \
            --bail
      - uses: actions/upload-artifact@v4
        if: ${{ !cancelled() }}
        with:
          name: api-test-results
          path: reports/

  # ========== 第二阶段：UI 测试（依赖 API 测试通过）==========
  ui-tests:
    name: UI Tests (Playwright)
    needs: api-tests
    runs-on: ubuntu-latest
    timeout-minutes: 30
    strategy:
      fail-fast: false
      matrix:
        shard: [1/3, 2/3, 3/3]
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: 20
          cache: 'npm'
      - run: npm ci
      - run: npx playwright install --with-deps
      - name: 运行 Playwright 测试
        run: npx playwright test --shard=${{ matrix.shard }}
        env:
          CI: true
      - uses: actions/upload-artifact@v4
        if: ${{ !cancelled() }}
        with:
          name: playwright-report-${{ strategy.job-index }}
          path: playwright-report/

  # ========== 第三阶段：合并报告 ==========
  merge-reports:
    name: 合并测试报告
    needs: [api-tests, ui-tests]
    if: ${{ !cancelled() }}
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/download-artifact@v4
        with:
          path: all-results/
      - run: npm install -g junit-report-merger
      - run: jrm combined-results.xml "all-results/**/*.xml"
      - uses: actions/upload-artifact@v4
        with:
          name: combined-report
          path: combined-results.xml
```

`needs: api-tests` 确保 UI 测试在 API 测试通过后才执行。**分片策略**（`matrix.shard`）将 UI 测试分布到 3 台并行机器上。

### 4.4 报告合并

两个工具都输出 **JUnit XML**——CI 集成的通用格式。使用 `junit-report-merger` 合并：

```bash
npm install -g junit-report-merger
jrm combined.xml "reports/**/*.xml"
```

如需统一的交互式仪表盘，**Allure Report** 是最佳选择——原生支持 Playwright（通过 `allure-playwright`），也可导入 Newman 的 JUnit XML。

---

## 5. Claude AI 加速测试生成与维护

### 5.1 Playwright MCP：让 AI 看到真实页面

传统方式让 AI 写测试最大的问题是**幻觉**——AI 会编造不存在的选择器和页面结构。**Playwright MCP**（Model Context Protocol）给 Claude 一个可控制和观察的真实浏览器，解决了这个问题。

```json
// .mcp.json — 让 Claude Code 控制真实浏览器
{
  "mcpServers": {
    "playwright": {
      "type": "stdio",
      "command": "npx",
      "args": ["@playwright/mcp@latest"]
    }
  }
}
```

Playwright v1.56+ 提供三个**专用 Agent**给 Claude Code：

| Agent | 功能 |
|-------|------|
| **Planner** | 探索应用，生成 Markdown 测试计划 |
| **Generator** | 将计划转化为 Playwright 测试代码（使用语义化定位器） |
| **Healer** | 重放失败测试，检查当前 UI，建议修复，并重新运行 |

初始化：`npx playwright init-agents --loop=claude`

### 5.2 CLAUDE.md：编码团队测试标准

在仓库根目录放置 `CLAUDE.md` 文件，为 Claude 提供持久的项目上下文：

```markdown
# 测试规范

## Playwright E2E 测试
- 使用 Page Object Model（页面对象在 /tests/ui/pages/）
- 使用语义化定位器：getByRole、getByLabel、getByText
- 禁止使用硬编码超时（waitForTimeout）
- 每个测试必须独立可运行
- 测试命名："should [行为] when [条件]"
- 使用 fixtures 注入 Page Object

## Newman API 测试
- Collection 按域组织
- 使用集合级 pre-request 脚本做认证
- 所有响应必须验证 JSON Schema
- 使用环境变量管理不同环境配置
```

### 5.3 自定义 Slash 命令

创建 `.claude/commands/write-e2e-test.md`：

```markdown
根据以下功能描述，生成符合团队规范的 Playwright E2E 测试：

1. 使用 Page Object Model 模式
2. 包含 happy path 和 error path
3. 使用 web-first 断言
4. 从 fixtures/fixtures.ts 导入 test 和 expect
5. 遵循项目的定位器优先级

功能描述：$ARGUMENTS
```

使用：`/write-e2e-test 用户密码重置流程`

### 5.4 高效提示模板

```xml
<instructions>为以下功能编写 Playwright E2E 测试</instructions>
<context>
  React SPA + REST API 全栈应用
  认证方式：JWT 存储在 localStorage
  Page Objects 位于 /tests/ui/pages/
  使用 TypeScript
</context>
<task>测试密码重置流程：请求重置 → 检查邮箱链接 → 设置新密码 → 用新密码登录</task>
<output_format>TypeScript .spec.ts，使用 POM 模式，包含 happy path 和 error path</output_format>
```

### 5.5 AI 辅助修复 Flaky 测试

研究表明 LLM 可以修复 **47–83% 的 flaky 测试**。Playwright 的 Healer Agent 能：
1. 重放失败的测试步骤
2. 检查当前 accessibility tree
3. 修补定位器或等待条件
4. 重新运行验证

手动调试时，将以下信息提供给 Claude：错误信息、失败率、Playwright trace、截图——让它先分类 flakiness 类型（时序、状态、资源竞争），再建议修复方案。修复后用 `--repeat-each=50` 验证稳定性。

### 5.6 Postman MCP：AI 生成 API 测试集

Postman 也提供了 MCP Server，可以让 Claude：
- 从 OpenAPI Spec 自动生成 Postman Collection
- 创建/更新 Collection 中的请求和测试脚本
- 运行测试并获取结果

thoughtbot 还发布了开源的 Claude Skill，能扫描后端控制器并自动生成带测试脚本的 Postman Collection。

---

## 6. 项目模板使用说明

随本报告附带的 `e2e-testing-template/` 目录是一个可直接使用的项目脚手架，包含：

```
e2e-testing-template/
├── package.json                    # 依赖和脚本命令
├── tests/
│   ├── api/
│   │   ├── collections/            # 示例 Postman Collection
│   │   ├── environments/           # 示例环境文件
│   │   └── data/                   # 数据驱动测试数据
│   ├── ui/
│   │   ├── tests/                  # 按功能域组织的测试
│   │   ├── pages/                  # Page Object Model
│   │   ├── fixtures/               # 自定义 fixtures
│   │   └── playwright.config.ts    # 生产就绪配置
│   └── shared/
│       ├── test-config.json        # 共享配置
│       └── generate-newman-env.js  # 环境生成器
├── scripts/
│   └── run-all-tests.sh            # 一键运行全部测试
├── .github/workflows/
│   └── e2e-tests.yml               # GitHub Actions 流水线
├── .claude/commands/
│   └── write-e2e-test.md           # Claude 自定义命令
├── CLAUDE.md                       # Claude 项目上下文
└── README.md                       # 快速开始指南
```

### 快速开始

```bash
# 1. 安装依赖
npm install

# 2. 安装 Playwright 浏览器
npx playwright install --with-deps

# 3. 运行 API 测试
npm run test:api

# 4. 运行 UI 测试
npm run test:ui

# 5. 运行全部 E2E 测试
npm run test:e2e
```

---

## 总结

Playwright + Newman 的组合为全栈应用提供了完整的测试栈。**Newman API 测试形成快速、稳定的中间层**，在秒级捕获后端回归；**Playwright UI 测试验证关键用户旅程**，支持跨浏览器并提供丰富的 Trace Viewer 调试。

最关键的集成点：
1. **共享配置层** 消除环境漂移
2. **CI/CD 流水线** 强制 API 先行的执行顺序
3. **JUnit 报告合并** 通过 Allure 等工具统一呈现
4. **Claude AI + MCP** 生成基于真实 DOM 的测试代码，而非幻觉选择器

将团队测试标准编码到 `CLAUDE.md` 和自定义 Skills 中，AI 生成的测试质量会显著提升——但人工审查始终不可缺少。测试金字塔恒久有效：尽可能将覆盖率推到 API 层，UI 测试只保留给真实浏览器才能验证的关键流程。
