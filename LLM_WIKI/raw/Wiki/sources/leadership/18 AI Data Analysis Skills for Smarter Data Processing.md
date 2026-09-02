---
title: "18 AI Data Analysis Skills for Smarter Data Processing"
source: "https://www.kimi.ai/resources/data-analysis-skills-for-agents"
author:
  - "[[Kimi]]"
published: 2026-07-31
created: 2026-09-02
description: "Discover 18 AI data analysis skills professionals need to interpret data, build models, uncover patterns, and make accurate business decisions."
tags:
  - "clippings"
---
Data analysis skills are becoming increasingly important as organizations rely on data to make faster and smarter decisions. With the help of AI, many data tasks, such as cleaning datasets, identifying trends, and generating insights, can now be completed more efficiently. AI skills provide reusable workflows and methodologies that help agents perform these analysis tasks in a more structured way. This guide explores 22 data analysis skills that can streamline data workflows and turn raw data into actionable insights.

## What are AI data analysis skills?

Data analysis skills provide AI agents with structured instructions, workflows, and guidelines to handle fundamental data analysis tasks. They help agents organize data, clean datasets, identify patterns, generate charts, perform basic calculations, and summarize insights from raw information.

## 12 Kimi's built-in AI data management and analysis skills

Kimi offers a wide range of built-in AI skills that simplify data processing, analysis, and reporting. Whether you're cleaning datasets, creating visualizations, or generating insights, these tools help automate repetitive tasks and improve efficiency. Here are 12 built-in AI data management and analysis skills you can explore in Kimi.

<table><thead><tr><th rowspan="1" colspan="1"><strong>Skill name</strong></th><th rowspan="1" colspan="1"><strong>Description</strong></th></tr></thead><tbody><tr><td rowspan="1" colspan="1"><strong>sql-insight</strong></td><td rowspan="1" colspan="1">Translate natural language to SQL, optimize query performance, and interpret EXPLAIN plans for SQLite and PostgreSQL. Triggered when users ask to convert questions into SQL, improve slow queries, tune indexes, analyze execution plans, or mention keywords like NL2SQL, query tuning, or full table scan.</td></tr><tr><td rowspan="1" colspan="1"><strong>auto-hypothesis-test</strong></td><td rowspan="1" colspan="1">Automatically selects and runs the right statistical test for your data — the ANOVA, chi-square, Mann-Whitney, or others, and provides plain-language interpretations of the results. Triggered when you ask about group comparisons, significance, p-values, hypothesis testing, or mention specific tests like t-test, ANOVA, or chi-square.</td></tr><tr><td rowspan="1" colspan="1"><strong>correlation-auditor</strong></td><td rowspan="1" colspan="1">Analyzes correlation matrices (Pearson/Spearman), computes partial correlations to control confounding variables, and flags potential spurious correlations in your data. Triggered when users ask about relationships between variables, need correlation matrices, or mention Pearson/Spearman coefficients, partial correlation, confounding factors, or spurious correlations.</td></tr><tr><td rowspan="1" colspan="1"><strong>data-viz-renderer</strong></td><td rowspan="1" colspan="1">Generate self-contained HTML/SVG infographics from JSON data, including stat cards, bar charts, flow diagrams, and mixed dashboards. Offers 8 color palettes and built-in icons with no external dependencies. Triggered when users request data visualization, infographics, charts, or dashboards.</td></tr><tr><td rowspan="1" colspan="1"><strong>dataset-quality-audit</strong></td><td rowspan="1" colspan="1">Run comprehensive quality checks on tabular data (CSV/Excel/TSV/JSON), detecting missing values, duplicates, outliers, format issues, and type inconsistencies to produce an overall score, grade, and actionable suggestions. Triggered when users ask to check data quality, find missing or duplicate values, detect outliers, validate formats, profile data, or clean data.</td></tr><tr><td rowspan="1" colspan="1"><strong>discounted-cashflow-model</strong></td><td rowspan="1" colspan="1">Builds a discounted cash flow (DCF) valuation model, calculating enterprise value, equity value, and per-share price with a growth-rate × discount-rate sensitivity analysis matrix. Triggered by requests like 'do a DCF on \[company]', 'run a valuation', 'calculate WACC/discount rate', or mentions of free cash flow, terminal value, or sensitivity analysis.</td></tr><tr><td rowspan="1" colspan="1"><strong>financial-ratio-toolkit</strong></td><td rowspan="1" colspan="1">Analyzes company fundamentals by computing 20+ financial ratios (profitability, solvency, liquidity, efficiency, and growth) and the DuPont Analysis from user-provided financial statements. Triggered by requests for financial ratio calculation, DuPont/ROE analysis, or phrases like "analyze these financials" or "calculate solvency ratios.</td></tr><tr><td rowspan="1" colspan="1"><strong>financial-statement-analyzer</strong></td><td rowspan="1" colspan="1">Analyzes income statement, balance sheet, and cash flow statement data to generate YoY/QoQ trend analysis and flag anomalies like AR surges or cash flow divergence. Trigger when users ask to analyze financials, compare YoY/QoQ, detect red flags, or assess earnings quality.</td></tr><tr><td rowspan="1" colspan="1"><strong>quick-strategy-backtest</strong></td><td rowspan="1" colspan="1">Convert trading strategy descriptions (including event-driven studies, stock selection, and portfolio) into runnable backtest code, and output backtest results, visual dashboards, and analytical write-ups. Triggers when users describe buy/sell conditions, post-event returns, stock-pool screening backtests, and other quantitative scenarios.</td></tr><tr><td rowspan="1" colspan="1"><strong>regression-modeler</strong></td><td rowspan="1" colspan="1">Run regression analysis (OLS or logistic) on uploaded CSV/Excel data, generating coefficients, R², p-values, VIF, and plain-language interpretation. Triggered by requests for regression modeling, fitting data, testing significance, checking multicollinearity, or keywords like OLS, logit, coefficient, p-value, or R-squared.</td></tr><tr><td rowspan="1" colspan="1"><strong>stock-research-report</strong></td><td rowspan="1" colspan="1">Generate securities research reports in Guotai Haitong / Haitong International style. Use for Chinese equity research, industry tracking, investment notes, and financial research documents. Triggers on keywords: Guotai Haitong, Haitong International, industry tracking, stock research, securities research. Supports domestic and international dual templates.</td></tr><tr><td rowspan="1" colspan="1"><strong>stock-signal-analyzer</strong></td><td rowspan="1" colspan="1">Analyzes OHLCV data to compute 15+ technical indicators (including MA, MACD, RSI, Bollinger Bands, KDJ) and generates a bullish/bearish signal summary with an overall assessment. Triggered when users request technical analysis, ask to calculate indicators like MACD or RSI, mention candlestick analysis, or discuss signals from moving average crossovers, Bollinger Band breakouts, or RSI overbought/oversold levels.</td></tr><tr><td rowspan="1" colspan="1"><strong>value-investing-scorecard</strong></td><td rowspan="1" colspan="1">Buffett/Graham's value investing scorecard — evaluates a company across 20 criteria in four dimensions (moat, management, financials, valuation) for a 0-100 score. Triggered when users request a value-investing analysis, fundamental scoring, moat assessment, or ask 'is this company worth investing in', 'analyze the fundamentals of XX', or 'evaluate this using Buffett's method'.</td></tr><tr><td rowspan="1" colspan="1"><strong>weighted-scorer</strong></td><td rowspan="1" colspan="1">Builds weighted scoring decision matrices for technology selection, vendor evaluation, and multi-criteria option comparisons. Guides you through defining criteria, assigning weights, scoring options, and validating results with sensitivity analysis. Trigger when users ask about decision matrices, weighted scoring, comparing options, vendor selection, or build vs. buy choices.</td></tr><tr><td rowspan="1" colspan="1"><strong>chart-image</strong></td><td rowspan="1" colspan="1">Generate publication-quality PNG chart images from data, supporting line, bar, area, candlestick, pie, and heatmap charts. Triggers when the user asks to visualize data, create a graph, plot a time series, or generate a chart for a report, alert, or dashboard. Runs as a lightweight, headless Node.js process without a browser.</td></tr><tr><td rowspan="1" colspan="1"><strong>xlsx</strong></td><td rowspan="1" colspan="1">Specialized utility for advanced manipulation, analysis, and creation of spreadsheet files, including (but not limited to) XLSX, XLSM, and CSV formats. Core functionalities include formula deployment, complex formatting (including automatic currency formatting for financial tasks), data visualization, mandatory post-processing recalculation, and finance-focused Excel modeling workflows such as three-statement models, DCF valuation, and public comps analysis.</td></tr></tbody></table>

### Use Kimi's built-in AI data analysis skills

Follow these simple steps to use Kimi's built-in AI skills for faster data analysis, financial calculations, and automated reporting.

**Step 1: Input a skill command**

Type the command `/financial-ratio-toolkit` in the input box to activate Kimi's financial data analysis skill.

![Input a skill command](https://kimi-file.kimi.ai/prod-chat-kimi/kfs/4/2/2026-07-30/1d9lk9e9l51jas5ce4eo0?x-tos-process=image%2Fauto-orient%2C1%2Fstrip%2Fignore-error%2C1)

Input a skill command

**Step 2: Start your research task**

Describe the dataset or financial analysis you want Kimi to perform after activating the skill.

**Example prompt:**

/financial-ratio-toolkit Analyze the uploaded financial statements and calculate key financial ratios, including liquidity, profitability, leverage, and efficiency ratios. Summarize the company's financial performance, identify strengths and potential risks, compare important metrics, and present the findings in a clear report with tables and charts.

![Start your research task](https://kimi-file.kimi.ai/prod-chat-kimi/kfs/4/2/2026-07-30/1d9lk9ehl51jas5ce4eq0?x-tos-process=image%2Fauto-orient%2C1%2Fstrip%2Fignore-error%2C1)

Start your research task

Then Kimi automatically analyzes the data, performs the required calculations, and generates a structured report with key insights to support faster decision-making.

![Start your research task](https://kimi-file.kimi.ai/prod-chat-kimi/kfs/4/2/2026-07-30/1d9lk9et3v89kken77brg?x-tos-process=image%2Fauto-orient%2C1%2Fstrip%2Fignore-error%2C1)

Start your research task

**Step 3: Review and download your document**

Review the generated report, make any necessary edits, and download the final document for further analysis, sharing, or presentation.

![Review and download your document](https://kimi-file.kimi.ai/prod-chat-kimi/kfs/4/2/2026-07-30/1d9lk9f2av1fc646chgng?x-tos-process=image%2Fauto-orient%2C1%2Fstrip%2Fignore-error%2C1)

Review and download your document

## Unlock 6 more open-source data analysis skills

Open-source skills provide AI agents with specialized workflows for different data analysis tasks. By installing these skills in Kimi, you can automate data processing, perform deeper analysis, and build more efficient workflows for handling complex datasets. Here are 6 open-source data analysis skills worth exploring.

<table><thead><tr><th rowspan="1" colspan="1"><strong>Skill name</strong></th><th rowspan="1" colspan="1"><strong>Description</strong></th><th rowspan="1" colspan="1"><strong>URL</strong></th></tr></thead><tbody><tr><td rowspan="1" colspan="1"><strong>data-analytics-skills</strong></td><td rowspan="1" colspan="1">A collection of 31 portable AI-powered skills covering the analyst workflow, including data quality checks, deep analysis, documentation, dashboard creation, and stakeholder communication.</td><td rowspan="1" colspan="1"><a href="https://github.com/nimrodfisher/data-analytics-skills">https://github.com/nimrodfisher/data-analytics-skills</a></td></tr><tr><td rowspan="1" colspan="1"><strong>d3-visualization-skill</strong></td><td rowspan="1" colspan="1">Comprehensive D3.js skill that helps agents create complex interactive data visualizations, including bar charts, line charts, force graphs, sankey diagrams, treemaps, sunbursts, and choropleth maps for dashboards and reports.</td><td rowspan="1" colspan="1"><a href="https://github.com/nexu-io/open-design/blob/main/skills/d3-visualization/SKILL.md">https://github.com/nexu-io/open-design/blob/main/skills/d3-visualization/SKILL.md</a></td></tr><tr><td rowspan="1" colspan="1"><strong>tufte-data-viz-skill</strong></td><td rowspan="1" colspan="1">Applies Edward Tufte's data visualization principles, including high data-ink ratio, minimal chart clutter, direct labels, small multiples, and sparklines, to create clean and accessible charts across visualization libraries.</td><td rowspan="1" colspan="1"><a href="https://github.com/caylent/tufte-data-viz">https://github.com/caylent/tufte-data-viz</a></td></tr><tr><td rowspan="1" colspan="1"><strong>mckinsey-style-visualization-skill</strong></td><td rowspan="1" colspan="1">Helps transform raw business notes into executive-ready consulting visuals with insight-driven headlines, visual hierarchy, reusable slide specifications, and quality evaluation frameworks.</td><td rowspan="1" colspan="1"><a href="https://github.com/kgraph57/mckinsey-style-visualization-skill">https://github.com/kgraph57/mckinsey-style-visualization-skill</a></td></tr><tr><td rowspan="1" colspan="1"><strong>data-visualization-report-skill</strong></td><td rowspan="1" colspan="1">Converts CSV, Excel, or JSON data into polished visual reports with KPI cards, Chart.js charts, and data tables. Supports template-based report generation for business and finance scenarios.</td><td rowspan="1" colspan="1"><a href="https://github.com/nexu-io/open-design/blob/main/skills/data-report/SKILL.md">https://github.com/nexu-io/open-design/blob/main/skills/data-report/SKILL.md</a></td></tr><tr><td rowspan="1" colspan="1"><strong>analytics-tracking-measurement-strategy</strong></td><td rowspan="1" colspan="1">Helps design, audit, and improve analytics tracking systems through measurement strategies, event taxonomies, data quality reviews, and tracking implementation workflows.</td><td rowspan="1" colspan="1"><a href="https://github.com/diegosouzapw/awesome-omni-skills/blob/main/skills/analytics-tracking/SKILL.md">https://github.com/diegosouzapw/awesome-omni-skills/blob/main/skills/analytics-tracking/SKILL.md</a></td></tr></tbody></table>

### Use open-source data analysis skills with Kimi

Follow these simple steps to install an open-source AI skill in Kimi and use it for advanced data analysis and reporting tasks.

**Step 1: Enter a prompt**

Open Kimi Chat and provide a prompt with the GitHub URL of the open-source data analysis skill you want to install.

**Example prompt:**

Install the data analytics skill from the GitHub repository below and make it available in my Kimi workspace. \[https://github.com/borghei/Claude-Skills/blob/main/data-analytics/analytics-engineer/SKILL.md\](https://github.com/borghei/Claude-Skills/blob/main/data-analytics/analytics-engineer/SKILL.md)

![Enter a prompt](https://kimi-file.kimi.ai/prod-chat-kimi/kfs/4/2/2026-07-30/1d9lk9faav1fc646chgp0?x-tos-process=image%2Fauto-orient%2C1%2Fstrip%2Fignore-error%2C1)

Enter a prompt

**Step 2: Let AI install the skill automatically**

Kimi automatically downloads, configures, and prepares the skill based on the provided GitHub URL. Once the installation is complete, the skill becomes available in your workspace.

![Let AI install the skill automatically](https://kimi-file.kimi.ai/prod-chat-kimi/kfs/4/2/2026-07-30/1d9lk9fiav1fc646chgqg?x-tos-process=image%2Fauto-orient%2C1%2Fstrip%2Fignore-error%2C1)

Let AI install the skill automatically

**Step 3: Use the skill**

Click "Add to my skills" to add the installed skill to Kimi, then select "Try it" to activate it. Once enabled, upload your dataset or describe your analysis task, and the skill will help clean data, perform calculations, generate insights, and create structured reports more efficiently.

![Use the skill](https://kimi-file.kimi.ai/prod-chat-kimi/kfs/4/2/2026-07-30/1d9lk9fqav1fc646chgsg?x-tos-process=image%2Fauto-orient%2C1%2Fstrip%2Fignore-error%2C1)

Use the skill

## Take data analysis further with custom AI skills

Follow these simple steps to build a custom AI skill that automates your data analysis workflows and makes recurring tasks more efficient.

**Step 1: Access the "Document to skills" tool**

Open Kimi Skills and click "Document to skills." This feature allows you to convert your data analysis documents into reusable AI skills.

![Access the document to the skills tool](https://kimi-file.kimi.ai/prod-chat-kimi/kfs/4/2/2026-07-30/1d9lk9fqav1fc646chgtg?x-tos-process=image%2Fauto-orient%2C1%2Fstrip%2Fignore-error%2C1)

Access the document to the skills tool

**Step 2: Upload the files**

Upload spreadsheets, CSV files, reports, SQL documentation, analysis guides, or workflow documents containing the knowledge you want to automate. Kimi extracts key information and builds a structured AI skill.

![Upload the files](https://kimi-file.kimi.ai/prod-chat-kimi/kfs/4/2/2026-07-30/1d9lk9g2av1fc646chgug?x-tos-process=image%2Fauto-orient%2C1%2Fstrip%2Fignore-error%2C1)

Upload the files

**Step 3: Create and use your skills**

Review the generated AI skill, refine its instructions if needed, and save it to your workspace. You can then use custom skills to automate data processing, generate reports, and streamline future analysis tasks.

![Create and use your skills](https://kimi-file.kimi.ai/prod-chat-kimi/kfs/4/2/2026-07-30/1d9lk9gn6rtp4tq89ucq0?x-tos-process=image%2Fauto-orient%2C1%2Fstrip%2Fignore-error%2C1)

Create and use your skills

You can edit it anytime or export it as an.md file for sharing and use in other projects.

![Create and use your skills](https://kimi-file.kimi.ai/prod-chat-kimi/kfs/4/2/2026-07-30/1d9lk9gn6rtp4tq89ucrg?x-tos-process=image%2Fauto-orient%2C1%2Fstrip%2Fignore-error%2C1)

Create and use your skills

## Tips for using AI data analysis skills

Using AI effectively starts with providing the right data and clear instructions. Follow these best practices to improve the accuracy of your data analysis skills and generate more meaningful insights.

- **Define clear analysis goals first**

Provide AI agents with specific questions, objectives, and expected outputs to help them focus on relevant data and generate more useful insights.

- **Prepare and validate your data before analysis**

Ensure datasets are complete, properly formatted, and free from obvious errors. Clean data helps AI agents produce more accurate analysis results.

- **Choose skills based on your analysis needs**

Use different skills for different tasks, such as data cleaning, visualization, reporting, forecasting, or dashboard creation.

- **Provide context and business background**

Include information about the dataset, industry, target audience, and decision goals so AI agents can interpret results more effectively.

- **Review and refine AI-generated insights**

Check analysis results, validate important findings, and adjust instructions when needed to improve the accuracy and consistency of future outputs.

## Conclusion

Whether you're developing basic data analysis skills or automating complex workflows, AI can save time while improving accuracy. Strong data analysis skills help you process information more efficiently and make better data-driven decisions. With Kimi, you can leverage built-in, open-source, and custom AI skills to simplify data analysis and turn raw data into actionable insights.

![AI Coding Skills: Build Faster with AI Workflows](https://kimi-file.kimi.ai/prod-chat-kimi/kfs/4/2/2026-07-30/1d9lk9pl3v89kken77cp0?x-tos-process=image%2Fauto-orient%2C1%2Fstrip%2Fignore-error%2C1) ![12 UI/UX Design Skills to Build Modern Interfaces](https://kimi-file.kimi.ai/prod-chat-kimi/kfs/4/2/2026-07-27/1d9jke72av1fc6469803g?x-tos-process=image%2Fauto-orient%2C1%2Fstrip%2Fignore-error%2C1) ![Kimi Agent Skills Examples for Smarter AI Workflows](https://kimi-file.kimi.ai/prod-chat-kimi/kfs/4/2/2026-08-24/1da5v67t3v89kkenq6cj0?x-tos-process=image%2Fauto-orient%2C1%2Fstrip%2Fignore-error%2C1) ![Useful Spreadsheet Skills to Automate Data Tasks](https://kimi-file.kimi.ai/prod-chat-kimi/kfs/4/2/2026-08-06/1d9q6gsqav1fc646ileg0?x-tos-process=image%2Fauto-orient%2C1%2Fstrip%2Fignore-error%2C1) ![13 Translation Skills: Automate Smarter Multilingual Tasks](https://kimi-file.kimi.ai/prod-chat-kimi/kfs/4/2/2026-08-03/1d9o19jiav1fc646fjjj0?x-tos-process=image%2Fauto-orient%2C1%2Fstrip%2Fignore-error%2C1)