# Claude Skills Pack - Phase B: Web-Testing Skill 实现计划

> **For agentic workers:** REQUIRED: Use superpowers:subagent-driven-development (if subagents available) or superpowers:executing-plans to implement this plan. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 基于 E2E 最佳实践重写 web-testing skill，整合 Playwright UI 测试和 Newman API 测试。

**Architecture:** 测试金字塔架构 - API 测试先行（Newman），UI 测试关键路径（Playwright）。包含主文档、2 个 reference 文件、5 个 template 文件。

**Tech Stack:** Playwright (TypeScript), Newman (Postman CLI), Page Object Model, Fixtures

**Spec:** `docs/superpowers/specs/2026-03-16-claude-skills-pack-design.md`
**Reference:** `E2E测试最佳实践-Playwright与Newman完整指南.md`

---

## Chunk 1: 主文档 SKILL.md

### Task 1: 创建 Web-Testing SKILL.md

**Files:**
- Create: `.claude/skills/testing/web-testing/SKILL.md`

- [ ] **Step 1: 创建目录结构**

```bash
mkdir -p /Users/Zhuanz/Desktop/onlyforskills/.claude/skills/testing/web-testing/references
mkdir -p /Users/Zhuanz/Desktop/onlyforskills/.claude/skills/testing/web-testing/templates
```

- [ ] **Step 2: 创建 SKILL.md 主文档**

```yaml
---
name: web-testing
description: |
  全栈 E2E 测试系统：Playwright (UI) + Newman (API)。
  遵循测试金字塔：API 测试先行，UI 测试关键路径。
  触发："run e2e", "playwright test", "api test", "newman", "e2e测试", "跑测试"
user-invocable: true
allowed-tools: Bash(npx playwright *), Bash(newman *), Bash(npm *), Read, Write, Edit
---

# Web Testing - 全栈 E2E 测试

全栈 E2E 测试系统，整合 **Playwright**（UI 测试）和 **Newman**（API 测试）。

## 测试策略（金字塔原则）

| 层级 | 工具 | 占比 | 速度 | 用途 |
|------|------|------|------|------|
| 单元测试 | Jest/Vitest | ~70% | 毫秒 | 业务逻辑 |
| API 测试 | Newman | ~20% | 秒 | 后端验证 |
| UI 测试 | Playwright | ~10% | 分钟 | 关键用户路径 |

**核心原则**：API 测试比 UI 快 10-100 倍。尽可能推到金字塔底层。

## 执行顺序（重要！）

```
┌─────────────────┐
│  1. API 测试    │  ← 永远先跑
│    (Newman)     │     后端挂了 → 立即发现
└────────┬────────┘
         ↓ 通过后
┌─────────────────┐
│  2. UI 测试     │  ← 再跑
│   (Playwright)  │     只验证关键路径
└─────────────────┘
```

如果后端 API 挂了，UI 测试会超时并报出令人困惑的错误。API 先行能在秒级发现后端问题。

## 快速开始

### 运行 API 测试（Newman）

```bash
# 安装 Newman（如果未安装）
npm install -g newman newman-reporter-htmlextra

# 运行测试
newman run tests/api/collections/api-tests.postman_collection.json \
  -e tests/api/environments/staging.json \
  --reporters cli,htmlextra \
  --reporter-htmlextra-export reports/newman-report.html
```

### 运行 UI 测试（Playwright）

```bash
# 安装 Playwright（如果未安装）
npm install -D @playwright/test
npx playwright install

# 运行测试
npx playwright test tests/ui/tests/ --project=chromium
```

### 运行完整 E2E 流水线

```bash
# 1. 先跑 API 测试
newman run tests/api/collections/api-tests.json -e staging.json --bail

# 2. API 通过后，跑 UI 测试
npx playwright test
```

---

## Part A: Playwright UI 测试

详细参考：`references/playwright-best-practices.md`

### 项目结构

```
tests/ui/
├── tests/                  # 按功能域组织
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
├── data/
│   └── testData.json
└── playwright.config.ts
```

**关键规范**：
- 测试文件按**功能域**分目录（`checkout/`、`auth/`）
- 文件命名：`create-order-happy-path.spec.ts`（描述性）
- Page Object：`PascalCase`（`LoginPage.ts`）
- 工具函数：`camelCase`（`dateUtils.ts`）

### Page Object Model + Fixtures

```typescript
// pages/LoginPage.ts
import { type Page, type Locator } from '@playwright/test';

export class LoginPage {
  readonly page: Page;
  readonly emailInput: Locator;
  readonly passwordInput: Locator;
  readonly submitButton: Locator;

  constructor(page: Page) {
    this.page = page;
    // ✅ 语义化定位器优先级：getByRole > getByLabel > getByText > getByTestId
    this.emailInput = page.getByLabel('邮箱');
    this.passwordInput = page.getByLabel('密码');
    this.submitButton = page.getByRole('button', { name: '登录' });
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

### 认证状态复用（Setup Project）

Playwright 的 **Setup Project 模式** 只登录一次，将 `storageState` 保存为 JSON：

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

在 `playwright.config.ts` 中，其他 project 声明 `dependencies: ['setup']` 和 `storageState`。

⚠️ 始终将 `playwright/.auth` 加入 `.gitignore`。

### 定位器优先级

```
getByRole → getByLabel → getByPlaceholder → getByText → getByTestId
```

| 定位器 | 用途 | 示例 |
|--------|------|------|
| `getByRole` | 语义化元素 | `page.getByRole('button', { name: '提交' })` |
| `getByLabel` | 表单字段 | `page.getByLabel('邮箱')` |
| `getByPlaceholder` | 输入框 | `page.getByPlaceholder('请输入')` |
| `getByText` | 文本内容 | `page.getByText('欢迎')` |
| `getByTestId` | 最后手段 | `page.getByTestId('submit-btn')` |

⚠️ **避免使用 CSS 类选择器** — 样式变更会导致测试失败。

### 消除 Flaky 测试

| 原因 | 对策 |
|------|------|
| 竞态条件 | 使用 web-first 断言 `await expect(locator).toBeVisible()` 自动重试 |
| 硬编码等待 | ❌ 永远不用 `waitForTimeout()`，用有意义的等待条件 |
| 第三方 API 不稳定 | 用 `page.route()` Mock 外部 API 请求 |
| 状态污染 | 保证每个测试独立运行 |
| 选择器脆弱 | 使用语义化定位器 |

**配置重试**（仅 CI 环境）：
```typescript
retries: process.env.CI ? 2 : 0,
```

**提前发现 flaky 测试**：
```bash
npx playwright test --repeat-each=5  # 本地跑 5 遍
```

**失败时保留诊断证据**：
```typescript
use: {
  trace: 'on-first-retry',
  screenshot: 'only-on-failure',
  video: 'retain-on-failure',
}
```

### 视觉回归测试

```typescript
// 像素级截图比较
await expect(page).toHaveScreenshot('checkout-page.png', {
  maxDiffPixels: 50,
  animations: 'disabled',
});

// 元素级截图（更精确）
await expect(page.locator('.product-card')).toHaveScreenshot();
```

---

## Part B: Newman API 测试

详细参考：`references/newman-best-practices.md`

### Collection 组织

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

### 变量管理

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

⚠️ **关键注意**：Newman 只读取环境文件的 **initial/shared value**，不读 Postman 的 current value。

### 集合级自动刷新 JWT Token

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
      pm.collectionVariables.set("token_expiry", (Date.now() + 3500000).toString());
    }
  });
}
```

### JSON Schema 验证

```javascript
const schema = {
  type: "object",
  properties: {
    id: { type: "integer" },
    name: { type: "string", minLength: 1 },
    email: { type: "string", format: "email" }
  },
  required: ["id", "name", "email"],
  additionalProperties: false  // 严格模式
};

pm.test("响应匹配 JSON Schema", () => {
  pm.response.to.have.jsonSchema(schema);
});
```

### Newman CLI 完整命令

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

---

## Part C: 测试隔离与并行

### Playwright 并行

Playwright 为每个测试创建独立的浏览器上下文（cookies、localStorage 完全隔离）。

```typescript
// playwright.config.ts 关键配置
fullyParallel: true,        // 所有文件的所有测试并行执行
workers: process.env.CI ? 2 : undefined,  // CI 限制 worker 数
```

**CI 分片（跨机器分布）**：
```bash
npx playwright test --shard=1/4   # 机器 1
npx playwright test --shard=2/4   # 机器 2
```

### Newman 串行执行

Newman 请求只能顺序执行，不支持并行。如需高并发负载测试，使用 k6 或 JMeter。

---

## 诊断命令

```bash
# Playwright
npx playwright test --repeat-each=5      # 检测 flaky
npx playwright test --shard=1/4          # CI 分片
npx playwright show-report               # 查看报告
npx playwright test --ui                 # UI 模式调试

# Newman
newman run collection.json --bail        # 首次失败停止
newman run collection.json -n 3          # 跑 3 遍
newman run collection.json --delay-request 500  # 请求间延迟
```

---

## 模板文件

使用以下模板快速开始：

| 模板 | 用途 |
|------|------|
| `templates/playwright.config.ts` | Playwright 配置 |
| `templates/base-page.ts` | Page Object 基类 |
| `templates/auth.setup.ts` | 认证 setup |
| `templates/fixtures.ts` | Fixtures 模板 |
| `templates/newman-collection.json` | Newman collection |

---

## 相关 Skills

- **api-testing** — 简化版 Newman 测试
- **tdd** — 测试驱动开发
- **debugging** — 调试失败的测试
```

Run: `cat /Users/Zhuanz/Desktop/onlyforskills/.claude/skills/testing/web-testing/SKILL.md | head -30`
Expected: 显示 SKILL.md 开头内容

---

## Chunk 2: Playwright Best Practices Reference

### Task 2: 创建 Playwright 参考文档

**Files:**
- Create: `.claude/skills/testing/web-testing/references/playwright-best-practices.md`

- [ ] **Step 1: 创建 playwright-best-practices.md`

从 E2E 最佳实践文档提取 Playwright 相关内容。

```markdown
# Playwright UI 测试最佳实践

> 适用于全栈应用的现代端到端测试策略

---

## 1. 项目结构

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
- 测试文件按**功能域**分目录
- 文件命名：`create-order-happy-path.spec.ts`（描述性）
- Page Object：`PascalCase`（`LoginPage.ts`）
- 工具函数：`camelCase`（`dateUtils.ts`）

---

## 2. Page Object Model + Fixtures

### 2.1 Page Object 类

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
    // ✅ 语义化定位器优先级
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

### 2.2 Fixtures 集成

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

### 2.3 测试使用

```typescript
// tests/checkout/checkout.spec.ts
import { test, expect } from '../../fixtures/fixtures';

test('用户可以成功完成结账', async ({ checkoutPage }) => {
  await checkoutPage.goto();
  await checkoutPage.addItem('商品A');
  await checkoutPage.fillShippingInfo({ name: '张三', address: '北京市' });
  await checkoutPage.submitOrder();
  await expect(checkoutPage.successMessage).toBeVisible();
});
```

---

## 3. 认证状态复用

### 3.1 Setup Project

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

### 3.2 多角色场景

为不同角色创建独立的认证文件：

```typescript
// admin.setup.ts
const adminAuthFile = 'playwright/.auth/admin.json';

// user.setup.ts
const userAuthFile = 'playwright/.auth/user.json';
```

⚠️ 始终将 `playwright/.auth` 加入 `.gitignore`。

---

## 4. 定位器优先级

```
getByRole → getByLabel → getByPlaceholder → getByText → getByTestId
```

| 定位器 | 用途 | 示例 |
|--------|------|------|
| `getByRole` | 语义化元素 | `page.getByRole('button', { name: '提交' })` |
| `getByLabel` | 表单字段 | `page.getByLabel('邮箱')` |
| `getByPlaceholder` | 输入框 | `page.getByPlaceholder('请输入')` |
| `getByText` | 文本内容 | `page.getByText('欢迎')` |
| `getByTestId` | 最后手段 | `page.getByTestId('submit-btn')` |

⚠️ **避免使用 CSS 类选择器** — 样式变更会导致测试失败。

---

## 5. 消除 Flaky 测试

### 5.1 配置重试

```typescript
// playwright.config.ts
retries: process.env.CI ? 2 : 0,
```

### 5.2 Flaky 测试原因与对策

| 原因 | 对策 |
|------|------|
| 竞态条件 | 使用 web-first 断言自动重试 |
| 硬编码等待 | ❌ 永远不用 `waitForTimeout()` |
| 第三方 API 不稳定 | 用 `page.route()` Mock |
| 状态污染 | 保证每个测试独立运行 |
| 选择器脆弱 | 使用语义化定位器 |

### 5.3 Web-first 断言

```typescript
// ✅ 正确：自动重试
await expect(locator).toBeVisible();
await expect(locator).toHaveText('成功');

// ❌ 错误：不重试
const isVisible = await locator.isVisible();
expect(isVisible).toBe(true);
```

### 5.4 提前发现 Flaky

```bash
npx playwright test --repeat-each=5  # 本地跑 5 遍
```

### 5.5 诊断证据

```typescript
use: {
  trace: 'on-first-retry',
  screenshot: 'only-on-failure',
  video: 'retain-on-failure',
}
```

---

## 6. 视觉回归测试

### 6.1 页面截图

```typescript
await expect(page).toHaveScreenshot('checkout-page.png', {
  maxDiffPixels: 50,
  animations: 'disabled',
});
```

### 6.2 元素截图

```typescript
await expect(page.locator('.product-card')).toHaveScreenshot();
```

### 6.3 最佳实践

- 在 CI 中使用 Playwright Docker 镜像（保证渲染一致性）
- 遮蔽动态内容（时间戳、广告位）
- 元素级截图比全页面截图更精确

---

## 7. 跨浏览器测试

```typescript
// playwright.config.ts
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
  {
    name: 'mobile-chrome',
    use: { ...devices['Pixel 5'], storageState: 'playwright/.auth/user.json' },
    dependencies: ['setup'],
  },
]
```

---

## 8. 测试隔离与并行

### 8.1 自动隔离

Playwright 为每个测试创建独立的浏览器上下文（cookies、localStorage 完全隔离）。

### 8.2 并行配置

```typescript
fullyParallel: true,
workers: process.env.CI ? 2 : undefined,
```

### 8.3 CI 分片

```bash
npx playwright test --shard=1/4
npx playwright test --shard=2/4
npx playwright test --shard=3/4
npx playwright test --shard=4/4
```

### 8.4 隔离原则

- 绝不通过全局变量共享状态
- 使用 `testInfo.workerIndex` 或 Faker.js 生成唯一测试数据
- 除非必要，不使用 `test.describe.configure({ mode: 'serial' })`

---

## 9. 报告策略

| 报告类型 | 用途 |
|----------|------|
| HTML Reporter | 本地调试 |
| GitHub Annotations | PR 反馈 |
| JUnit XML | CI 集成 |
| Trace Viewer | 深度调试（`trace.playwright.dev`） |

---

## 10. 完整配置示例

```typescript
// playwright.config.ts
import { defineConfig, devices } from '@playwright/test';

export default defineConfig({
  testDir: './tests',
  fullyParallel: true,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 2 : 0,
  workers: process.env.CI ? 2 : undefined,
  reporter: 'html',
  use: {
    baseURL: 'http://localhost:3000',
    trace: 'on-first-retry',
    screenshot: 'only-on-failure',
    video: 'retain-on-failure',
  },
  projects: [
    { name: 'setup', testMatch: /.*\.setup\.ts/ },
    {
      name: 'chromium',
      use: { ...devices['Desktop Chrome'], storageState: 'playwright/.auth/user.json' },
      dependencies: ['setup'],
    },
  ],
});
```
```

---

## Chunk 3: Newman Best Practices Reference

### Task 3: 创建 Newman 参考文档

**Files:**
- Create: `.claude/skills/testing/web-testing/references/newman-best-practices.md`

- [ ] **Step 1: 创建 newman-best-practices.md`

```markdown
# Newman / Postman API 测试最佳实践

> 适用于全栈应用的 API 层测试策略

---

## 1. Collection 组织结构

按**域/资源**组织 Postman Collection：

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

---

## 2. 变量管理

### 2.1 变量优先级

从高到低：`local` → `data` → `environment` → `collection` → `global`

| 变量类型 | 用途 | 示例 |
|----------|------|------|
| Environment | 环境间变化的值 | `base_url`, `auth_token` |
| Collection | 集合内的常量 | `api_version`, `timeout` |
| Global | 跨集合共享 | `common_headers` |
| Data | 数据驱动测试 | CSV/JSON 文件中的行 |

### 2.2 Newman 变量传递

```bash
newman run collection.json \
  -e staging.json \
  --env-var "base_url=https://api.staging.com" \
  --env-var "api_key=secret123"
```

⚠️ **关键注意**：Newman 只读取环境文件的 **initial/shared value**，不读 Postman 的 current value。始终使用 shared value 或 `--env-var` 覆盖。

---

## 3. 脚本执行流程

### 3.1 执行顺序

```
Collection Pre-request
    ↓
Folder Pre-request
    ↓
Request Pre-request
    ↓
【发送请求】
    ↓
Collection Tests
    ↓
Folder Tests
    ↓
Request Tests
```

### 3.2 集合级自动刷新 JWT Token

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
      pm.collectionVariables.set("token_expiry", (Date.now() + 3500000).toString());
    }
  });
}
```

### 3.3 集合级通用断言（DRY 模式）

```javascript
// Collection-level test script — 对所有请求自动执行
pm.test("响应是有效 JSON", () => { pm.response.json(); });
pm.test("无服务器错误", () => { pm.expect(pm.response.code).to.be.below(500); });
pm.test("响应时间 < 5s", () => { pm.expect(pm.response.responseTime).to.be.below(5000); });
```

---

## 4. 请求链接与数据驱动

### 4.1 请求链接

从响应中提取数据并传递给下一个请求：

```javascript
// POST Create User 的 test script
const response = pm.response.json();
pm.collectionVariables.set("created_user_id", response.id);
// 后续 GET User By ID 使用 {{created_user_id}}
```

### 4.2 流程控制

```javascript
postman.setNextRequest("Request Name"); // 跳转到指定请求
postman.setNextRequest(null);           // 终止执行
```

### 4.3 数据驱动测试

```csv
# test-data.csv
email,password,expected_status
valid@test.com,pass123,200
invalid@test.com,wrong,401
,pass123,400
```

```bash
newman run collection.json -d test-data.csv -n 3 --delay-request 200
```

在脚本中通过 `pm.iterationData.get('email')` 访问每行数据。

---

## 5. JSON Schema 验证

使用 **Ajv**（不要用已废弃的 tv4）：

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
  additionalProperties: false  // ⚠️ 严格模式
};

pm.test("响应匹配 JSON Schema", () => {
  pm.response.to.have.jsonSchema(schema);
});
```

---

## 6. Newman CLI 完整命令

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

### 6.1 HTMLExtra Reporter

最流行的第三方报告器，提供：
- 交互式仪表盘
- 暗色主题
- 分页和失败过滤

### 6.2 Newman 编程接口

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

---

## 7. Newman 的局限性

| 局限 | 替代方案 |
|------|----------|
| 无原生 OAuth 2.0 | pre-request 脚本手动获取 token |
| 无 Postman 包库 | — |
| 串行执行 | — |
| 负载测试有限 | k6 或 JMeter |

---

## 8. 分层执行策略

| 触发时机 | 执行范围 | 预计耗时 |
|----------|----------|----------|
| Pull Request | API Smoke (`--folder Smoke`) | < 5 分钟 |
| 合并到 main | 完整 API 测试 | < 15 分钟 |
| 每日定时 | 完整 API + UI | < 60 分钟 |
| 发版前 | 完整 API + UI + 性能 + 安全 | < 2 小时 |

---

## 9. 常见问题

### 9.1 变量不生效

确保使用 **shared value** 而非 current value，或使用 `--env-var` 覆盖。

### 9.2 Token 过期

使用集合级 pre-request 脚本自动刷新。

### 9.3 请求顺序依赖

使用 `postman.setNextRequest()` 控制流程。

### 9.4 测试数据隔离

使用数据驱动测试（CSV/JSON）和 `pm.iterationData.get()`。
```

---

## Chunk 4: Template Files

### Task 4: 创建模板文件

**Files:**
- Create: `.claude/skills/testing/web-testing/templates/playwright.config.ts`
- Create: `.claude/skills/testing/web-testing/templates/base-page.ts`
- Create: `.claude/skills/testing/web-testing/templates/auth.setup.ts`
- Create: `.claude/skills/testing/web-testing/templates/fixtures.ts`
- Create: `.claude/skills/testing/web-testing/templates/newman-collection.json`

- [ ] **Step 1: 创建 playwright.config.ts 模板**

```typescript
// templates/playwright.config.ts
import { defineConfig, devices } from '@playwright/test';

/**
 * Playwright 配置模板
 * 复制到项目根目录并根据需要修改
 */
export default defineConfig({
  testDir: './tests/ui/tests',
  fullyParallel: true,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 2 : 0,
  workers: process.env.CI ? 2 : undefined,
  reporter: [
    ['html', { open: 'never' }],
    ['list']
  ],

  use: {
    baseURL: process.env.BASE_URL || 'http://localhost:3000',
    trace: 'on-first-retry',
    screenshot: 'only-on-failure',
    video: 'retain-on-failure',
  },

  projects: [
    // Setup project - 认证状态
    {
      name: 'setup',
      testMatch: /.*\.setup\.ts/,
    },
    // Chromium
    {
      name: 'chromium',
      use: {
        ...devices['Desktop Chrome'],
        storageState: 'playwright/.auth/user.json',
      },
      dependencies: ['setup'],
    },
    // Firefox (可选)
    // {
    //   name: 'firefox',
    //   use: { ...devices['Desktop Firefox'], storageState: 'playwright/.auth/user.json' },
    //   dependencies: ['setup'],
    // },
    // Mobile (可选)
    // {
    //   name: 'mobile-chrome',
    //   use: { ...devices['Pixel 5'], storageState: 'playwright/.auth/user.json' },
    //   dependencies: ['setup'],
    // },
  ],

  // Web Server (可选 - 自动启动开发服务器)
  // webServer: {
  //   command: 'npm run dev',
  //   url: 'http://localhost:3000',
  //   reuseExistingServer: !process.env.CI,
  // },
});
```

- [ ] **Step 2: 创建 base-page.ts 模板**

```typescript
// templates/base-page.ts
import { type Page, type Locator, expect } from '@playwright/test';

/**
 * Page Object 基类
 * 所有 Page Object 应继承此类
 */
export abstract class BasePage {
  readonly page: Page;

  constructor(page: Page) {
    this.page = page;
  }

  /**
   * 导航到指定路径
   */
  async goto(path: string = '/') {
    await this.page.goto(path);
  }

  /**
   * 等待页面加载完成
   */
  async waitForLoad() {
    await this.page.waitForLoadState('networkidle');
  }

  /**
   * 获取当前 URL
   */
  getCurrentUrl(): string {
    return this.page.url();
  }

  /**
   * 断言当前路径
   */
  async assertPath(expectedPath: string) {
    await expect(this.page).toHaveURL(new RegExp(expectedPath));
  }

  /**
   * 截图
   */
  async screenshot(name: string) {
    await this.page.screenshot({ path: `screenshots/${name}.png` });
  }

  /**
   * 等待元素可见
   */
  async waitForVisible(locator: Locator) {
    await expect(locator).toBeVisible();
  }

  /**
   * 点击并等待导航
   */
  async clickAndWait(locator: Locator, waitForPath?: string) {
    await locator.click();
    if (waitForPath) {
      await this.page.waitForURL(new RegExp(waitForPath));
    }
  }
}
```

- [ ] **Step 3: 创建 auth.setup.ts 模板**

```typescript
// templates/auth.setup.ts
import { test as setup, expect } from '@playwright/test';

const authFile = 'playwright/.auth/user.json';

setup('认证', async ({ page }) => {
  // 1. 导航到登录页
  await page.goto('/login');

  // 2. 填写登录表单
  await page.getByLabel(/邮箱|email/i).fill(process.env.TEST_EMAIL || 'test@example.com');
  await page.getByLabel(/密码|password/i).fill(process.env.TEST_PASSWORD || 'password123');

  // 3. 点击登录
  await page.getByRole('button', { name: /登录|login/i }).click();

  // 4. 等待导航到仪表盘
  await page.waitForURL(/dashboard|home/i);

  // 5. 保存认证状态
  await page.context().storageState({ path: authFile });
});
```

- [ ] **Step 4: 创建 fixtures.ts 模板**

```typescript
// templates/fixtures.ts
import { test as base, expect } from '@playwright/test';

/**
 * 自定义 Fixtures 类型定义
 * 在这里添加你的 Page Object
 */
type MyFixtures = {
  // 示例：添加 LoginPage
  // loginPage: LoginPage;
};

/**
 * 扩展的 test 对象
 * 使用这个 test 而不是 @playwright/test 的 test
 */
export const test = base.extend<MyFixtures>({
  // 示例：注入 LoginPage
  // loginPage: async ({ page }, use) => {
  //   await use(new LoginPage(page));
  // },
});

/**
 * 重新导出 expect
 */
export { expect };

/**
 * 使用示例：
 *
 * ```typescript
 * import { test, expect } from '../fixtures';
 *
 * test('登录测试', async ({ loginPage }) => {
 *   await loginPage.goto();
 *   await loginPage.login('user@example.com', 'password');
 *   await expect(page).toHaveURL(/dashboard/);
 * });
 * ```
 */
```

- [ ] **Step 5: 创建 newman-collection.json 模板**

```json
{
  "info": {
    "name": "API Tests Template",
    "description": "Newman/Postman Collection 模板",
    "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json"
  },
  "variable": [
    {
      "key": "api_version",
      "value": "v1"
    },
    {
      "key": "auth_token",
      "value": ""
    },
    {
      "key": "token_expiry",
      "value": ""
    }
  ],
  "event": [
    {
      "listen": "prerequest",
      "script": {
        "type": "text/javascript",
        "exec": [
          "// 集合级 pre-request 脚本",
          "// 自动刷新 JWT Token",
          "const tokenExpiry = pm.collectionVariables.get('token_expiry');",
          "if (!tokenExpiry || Date.now() > parseInt(tokenExpiry)) {",
          "  // Token 过期或不存在，需要刷新",
          "  // 在这里添加刷新逻辑",
          "}"
        ]
      }
    },
    {
      "listen": "test",
      "script": {
        "type": "text/javascript",
        "exec": [
          "// 集合级通用断言",
          "pm.test('响应是有效 JSON', () => { pm.response.json(); });",
          "pm.test('无服务器错误', () => { pm.expect(pm.response.code).to.be.below(500); });",
          "pm.test('响应时间 < 5s', () => { pm.expect(pm.response.responseTime).to.be.below(5000); });"
        ]
      }
    }
  ],
  "item": [
    {
      "name": "Health Check",
      "item": [
        {
          "name": "GET Health",
          "request": {
            "method": "GET",
            "header": [],
            "url": {
              "raw": "{{base_url}}/health",
              "host": ["{{base_url}}"],
              "path": ["health"]
            }
          },
          "response": []
        }
      ]
    },
    {
      "name": "Authentication",
      "item": [
        {
          "name": "POST Login",
          "request": {
            "method": "POST",
            "header": [
              {
                "key": "Content-Type",
                "value": "application/json"
              }
            ],
            "body": {
              "mode": "raw",
              "raw": "{\n  \"email\": \"{{auth_email}}\",\n  \"password\": \"{{auth_password}}\"\n}"
            },
            "url": {
              "raw": "{{base_url}}/auth/login",
              "host": ["{{base_url}}"],
              "path": ["auth", "login"]
            }
          },
          "response": []
        }
      ]
    }
  ]
}
```

---

## Chunk 5: 更新 SKILL-CATALOG.md

### Task 5: 更新技能索引

**Files:**
- Modify: `.claude/skills/SKILL-CATALOG.md`

- [ ] **Step 1: 在 SKILL-CATALOG.md 中添加 web-testing 详情**

找到测试层部分，更新 web-testing 条目：

```markdown
## 测试层 (Testing)

| Skill | 触发词 | 用途 |
|-------|--------|------|
| `web-testing` | /e2e, playwright, newman, 测试 | **全栈 E2E 测试**（Playwright UI + Newman API） |
| `api-testing` | /api-test, newman | Newman/Postman API 测试（简化版） |

### web-testing 子模块

| 文件 | 用途 |
|------|------|
| `SKILL.md` | 主文档 |
| `references/playwright-best-practices.md` | Playwright 最佳实践 |
| `references/newman-best-practices.md` | Newman 最佳实践 |
| `templates/playwright.config.ts` | Playwright 配置模板 |
| `templates/base-page.ts` | Page Object 基类模板 |
| `templates/auth.setup.ts` | 认证 setup 模板 |
| `templates/fixtures.ts` | Fixtures 模板 |
| `templates/newman-collection.json` | Newman collection 模板 |
```

---

## Chunk 6: 验证与提交

### Task 6: 验证完整性

- [ ] **Step 1: 验证目录结构**

```bash
tree /Users/Zhuanz/Desktop/onlyforskills/.claude/skills/testing/
```

Expected:
```
testing/
└── web-testing/
    ├── SKILL.md
    ├── references/
    │   ├── playwright-best-practices.md
    │   └── newman-best-practices.md
    └── templates/
        ├── playwright.config.ts
        ├── base-page.ts
        ├── auth.setup.ts
        ├── fixtures.ts
        └── newman-collection.json
```

- [ ] **Step 2: 验证文件数量**

```bash
find /Users/Zhuanz/Desktop/onlyforskills/.claude/skills/testing/ -type f | wc -l
```

Expected: 8 个文件

- [ ] **Step 3: 提交 Phase B 完成**

```bash
cd /Users/Zhuanz/Desktop/onlyforskills
git add .claude/skills/testing/
git add .claude/skills/SKILL-CATALOG.md
git commit -m "feat(skills): add web-testing skill with Playwright + Newman

- Add comprehensive web-testing SKILL.md
- Add playwright-best-practices.md reference
- Add newman-best-practices.md reference
- Add 5 template files (config, page, auth, fixtures, collection)
- Update SKILL-CATALOG.md with testing layer

Phase B of Claude Skills Pack implementation."
```

---

## 完成检查

- [ ] web-testing/SKILL.md 包含完整的 E2E 测试指南
- [ ] references/ 包含 Playwright 和 Newman 最佳实践
- [ ] templates/ 包含 5 个模板文件
- [ ] SKILL-CATALOG.md 已更新测试层
- [ ] Git 提交完成

---

## 下一步

Phase B 完成后，继续执行：
- **Phase C**: Skills 整合（从插件复制 33 个 skills）
- **Phase D**: 分发包（README + 清理）
