---
title: "Post by @karpathy on X"
source: "https://x.com/karpathy/status/2039805659525644595"
author:
  - "[[@karpathy]]"
published: 2026-04-03
created: 2026-09-02
description: "ฐานความรู้ LLM สิ่งที่ฉันพบว่ามีประโยชน์มากในช่วงนี้: การใช้ LLM เพื่อสร้างฐานความรู้ส่วนตัวสำหรับหัวข้อวิจัยที่สนใจต่างๆ ในลักษณะนี้ ส่วนใ"
tags:
  - "clippings"
---
ฐานความรู้ LLM

สิ่งที่ฉันพบว่ามีประโยชน์มากในช่วงนี้: การใช้ LLM เพื่อสร้างฐานความรู้ส่วนตัวสำหรับหัวข้อวิจัยที่สนใจต่างๆ ในลักษณะนี้ ส่วนใหญ่ของโทเค็นที่ฉันใช้ในช่วงหลังๆ จะถูกนำไปใช้กับการจัดการโค้ดน้อยลง และนำไปใช้กับการจัดการความรู้มากขึ้น (ที่เก็บไว้ในรูปแบบ markdown และภาพ) LLM ล่าสุดทำได้ดีมากในเรื่องนี้ ดังนั้น:

การรับข้อมูลเข้า:

ฉันจัดทำดัชนีเอกสารต้นทาง (บทความ เอกสารวิชาการ โครงการข้อมูลชุดข้อมูล ภาพ ฯลฯ) ลงในไดเรกทอรี raw/ จากนั้นฉันใช้ LLM เพื่อ "คอมไพล์" วิกิแบบ逐步 ซึ่งก็คือชุดของไฟล์ .md ในโครงสร้างไดเรกทอรี วิกินี้รวมสรุปของข้อมูลทั้งหมดใน raw/ ลิงก์ย้อนกลับ และจากนั้นมันจะจำแนกข้อมูลเป็นแนวคิด เขียนบทความสำหรับแนวคิดเหล่านั้น และเชื่อมโยงทั้งหมดเข้าด้วยกัน เพื่อแปลงบทความเว็บเป็นไฟล์ .md ฉันชอบใช้ส่วนขยาย Obsidian Web Clipper และจากนั้นฉันยังใช้ทางลัดคีย์บอร์ดเพื่อดาวน์โหลดภาพที่เกี่ยวข้องทั้งหมดลงเครื่องจักรท้องถิ่น เพื่อให้ LLM สามารถอ้างอิงได้ง่าย

IDE:

ฉันใช้ Obsidian เป็น "frontend" ของ IDE ที่ซึ่งฉันสามารถดูข้อมูลดิบ วิกิที่คอมไพล์แล้ว และการแสดงผลที่ได้มา สิ่งสำคัญที่ต้องทราบคือ LLM เขียนและบำรุงรักษาข้อมูลทั้งหมดของวิกิ ฉันแทบไม่แตะต้องมันโดยตรง ฉันเคยลองใช้ปลั๊กอิน Obsidian บางตัวเพื่อแสดงและดูข้อมูลในรูปแบบอื่นๆ (เช่น Marp สำหรับสไลด์)

Q&A:

จุดที่น่าสนใจคือเมื่อวิกิของคุณใหญ่พอ (เช่น ของฉันเกี่ยวกับวิจัยล่าสุดมี ~100 บทความและ ~400K คำ) คุณสามารถถามตัวแทน LLM ของคุณได้ทุกคำถามซับซ้อนเกี่ยวกับวิกิ และมันจะไปค้นคว้าคำตอบ ฯลฯ ฉันคิดว่าต้องใช้ RAG แบบหรูหรา แต่ LLM ทำได้ดีในการบำรุงรักษาไฟล์ดัชนีอัตโนมัติและสรุปสั้นๆ ของเอกสารทั้งหมด และมันอ่านข้อมูลที่เกี่ยวข้องสำคัญทั้งหมดได้ค่อนข้างง่ายในระดับ ~small scale นี้

Output:

แทนที่จะได้คำตอบในรูปแบบข้อความ/เทอร์มินัล ฉันชอบให้มันแสดงไฟล์ markdown สำหรับฉัน หรือสไลด์โชว์ (รูปแบบ Marp) หรือภาพ matplotlib ซึ่งทั้งหมดนั้นฉันดูอีกครั้งใน Obsidian คุณสามารถจินตนาการถึงรูปแบบผลลัพธ์ภาพอื่นๆ มากมายขึ้นอยู่กับคำถามบ่อยครั้ง ฉันจบลงด้วยการ "ยื่น" ผลลัพธ์กลับเข้าไปในวิกิเพื่อเสริมปรุงมันสำหรับคำถามต่อไป ดังนั้นการสำรวจและคำถามของฉันเองจึง "บวกเพิ่ม" เสมอในฐานความรู้

Linting:

ฉันเคยรัน "health checks" ของ LLM บนวิกิเพื่อ เช่น ค้นหาข้อมูลที่ไม่สอดคล้องกัน สร้างข้อมูลที่ขาดหายไป (ด้วยเครื่องมือค้นหาเว็บ) ค้นหาการเชื่อมโยงที่น่าสนใจสำหรับผู้สมัครบทความใหม่ ฯลฯ เพื่อค่อยๆ ทำความสะอาดวิกิและเสริมสร้างความสมบูรณ์ของข้อมูลโดยรวม LLM ทำได้ดีมากในการแนะนำคำถามเพิ่มเติมที่จะถามและดู

เครื่องมือพิเศษ:

ฉันพบว่าตัวเองพัฒนาเครื่องมือเพิ่มเติมเพื่อประมวลผลข้อมูล เช่น ฉันเขียนโค้ดแบบ vibe 一个小และเรียบง่ายเครื่องมือค้นหาบนวิกิ ซึ่งฉันใช้โดยตรง (ใน web ui) แต่บ่อยครั้งกว่าฉันต้องการส่งต่อให้ LLM ผ่าน CLI เป็นเครื่องมือสำหรับคำถามใหญ่กว่า

การสำรวจเพิ่มเติม:

เมื่อ repo เติบโต ความปรารถนาธรรมชาติคือคิดถึงการสร้างข้อมูลสังเคราะห์ + finetuning เพื่อให้ LLM ของคุณ "รู้" ข้อมูลในน้ำหนักของมันแทนที่จะเป็นแค่ context windows

TLDR: ข้อมูลดิบจากแหล่งที่มามากมายถูกรวบรวม จากนั้นคอมไพล์โดย LLM เป็นวิกิ .md จากนั้นดำเนินการโดย CLI ต่างๆ โดย LLM เพื่อทำ Q&A และเสริมปรุงวิกิแบบ逐步 และทั้งหมดดูได้ใน Obsidian คุณแทบไม่เคยเขียนหรือแก้ไขวิกิด้วยมือ มันเป็นโดเมนของ LLM ฉันคิดว่ามีที่ว่างที่นี่สำหรับผลิตภัณฑ์ใหม่ที่ยอดเยี่ยมแทนที่จะเป็นชุดสคริปต์แบบ hacky

---

## Comments

> **Goss Gowtham 𝕏 @Goss\_Gowtham** · [2026-04-02](https://x.com/Goss_Gowtham/status/2039830480829456596)
> 
> Can you make a video of how you work with md files, agentic IDEs?
> 
> Your earlier explanations of using LLMs were really helpful.
> 
> > **Andrej Karpathy @karpathy** · [2026-04-02](https://x.com/karpathy/status/2039832291464417746)
> > 
> > I was just thinking the same thing

> **Gavriel Cohen @Gavriel\_Cohen** · [2026-04-02](https://x.com/Gavriel_Cohen/status/2039810935452225959)
> 
> Can you share more on the incremental compilation?
> 
> I've found that if processing one by one, they don't have enough context to understand how to divide to directories.
> 
> Is there an optimal batch size? Multiple stages?
> 
> > **Andrej Karpathy @karpathy** · [2026-04-02](https://x.com/karpathy/status/2039812403962253744)
> > 
> > Atm it's not a fully autonomous process, I add every source manually, one by one and I am in the loop, especially in early stages. After a while, the LLMs "gets" the pattern and the marginal document is a lot easier, I just say "file this new doc to our wiki: (path)".

> **jiahao @\_endif\_** · [2026-04-02](https://x.com/_endif_/status/2039810651120705569)
> 
> you are like Linus to Linux now, the meta vibe coder, I wonder how many projects will be created overnight because of your tweet
> 
> > **Andrej Karpathy @karpathy** · [2026-04-02](https://x.com/karpathy/status/2039816150062948769)
> > 
> > Haha I vibe code products with twitter :D

> **Krishna Tammireddy @tammireddy** · [2026-04-02](https://x.com/tammireddy/status/2039814328229204201)
> 
> Every business has a raw/ directory.
> 
> Nobody's ever compiled it.
> 
> That's the product.
> 
> > **Andrej Karpathy @karpathy** · [2026-04-02](https://x.com/karpathy/status/2039814446479192187)
> > 
> > Might be an LLM reply I don't know, but yes exactly.

> **CBir @c\_\_bir** · [2026-04-02](https://x.com/c__bir/status/2039812841750839506)
> 
> are you useing obsidian cli?
> 
> > **Andrej Karpathy @karpathy** · [2026-04-02](https://x.com/karpathy/status/2039814066575917263)
> > 
> > Currently no because I'm trying to keep it super simple and flat, it's just a nested directory of .md files and .png files and a few .csv and .py, and the schema is kept up to date in AGENTS.md . The LLMs get this very easily. Any custom functions are easy to vibe code tools for.

> **Lex Fridman @lexfridman** · [2026-04-02](https://x.com/lexfridman/status/2039841897066414291)
> 
> Same, I have a similar setup. A mix of Obsidian, Cursor (for md), and vibe-coded web terminals as front-end.
> 
> Since I do a podcast, the number/diversity of research interests is very large. But the knowledge-base approach has been working great.
> 
> For answers, I often have it

> **0xSero @0xSero** · [2026-04-02](https://x.com/0xSero/status/2039813228352717201)
> 
> One thing I've done this year is:
> 
> \- Download all my X data from settings/account
> 
> \- Download all my youtube, gmaps, gmail, google from takout google com
> 
> \- Download all my personal data from Claude, ChatGPT
> 
> \- Export a copy of every AI session on Cursor Claude Code, Codex, Droid,

> **Robert Scoble @Scobleizer** · [2026-04-02](https://x.com/Scobleizer/status/2039806272867029069)
> 
> I did even more.
> 
> Ingested everything on X about AI and had it build this: https://alignednews.com/ai
> 
> Has a feed for your AI to hit too.
> 
> Includes papers, models, news, events, and much more.
> 
> Updated three times a day. Reads EVERYONE in AI on X and 8,300 AI companies too.
> 
> [https://t.co/kiuZ7QXLzb](https://t.co/kiuZ7QXLzb)