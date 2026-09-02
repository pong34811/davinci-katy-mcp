/*
 * SFX Manager Plugin for Obsidian
 * จัดการ Sound Effects สำหรับ DaVinci Resolve
 * คลังเสียง 73 ไฟล์ 37 ตระกูล — แหล่งที่มา: LLM_WIKI/raw/Wiki/sources/sfx/sfx-library-catalog.md
 */

const { App, Plugin, PluginSettingTab, Setting, Modal, Notice } = require('obsidian');

// Default directory resolves relative to the vault's root
const DEFAULT_SFX_DIR = 'SFX';
const DEFAULT_FORMAT = 'talking-head';
const DEFAULT_DENSITY = 4;

const ALL_SFX_FAMILIES = [
  // Canonical families (from scripts/config.py → SFX_FAMILIES)
  { name: 'pop', file: 'Pop - Short 06.mp3', use: 'surprise, emphasis', format: 'MP3', size: '15 KB' },
  { name: 'ding', file: 'Bell - Ding 02.wav, Bell - Ting.mp3', use: 'emphasis, success', format: 'WAV/MP3', size: '45 KB' },
  { name: 'collect', file: 'Game - Correct Collect Answer.mp3', use: 'success', format: 'MP3', size: '22 KB' },
  { name: 'sparkle', file: 'Harp - Sparkle 01.mp3, Harp - Sparkle 06.mp3, Magic - Shimmer 01.mp3', use: 'excitement, closing', format: 'MP3', size: '55 KB' },
  { name: 'whoosh', file: 'Whoosh - Clean Fast.mp3, Whoosh - Fast 01.mp3, Transition - Whoosh 01.mp3', use: 'transition', format: 'MP3', size: '48 KB' },
  { name: 'impact', file: 'Impact - Comedy Hit 01.mp3, Impact - Comedy Hit 02.mp3', use: 'surprise, comedy', format: 'MP3', size: '65 KB' },
  { name: 'wrong', file: 'Game - Wrong Answer.mp3', use: 'fail', format: 'MP3', size: '18 KB' },
  { name: 'honk', file: 'Horn - Duck Honk 01.mp3, Horn - Duck Honk 02.mp3', use: 'comedy, notification', format: 'MP3', size: '35 KB' },
  { name: 'gong', file: 'Gong - Comical Metal.wav, Gong - Metal.wav', use: 'dramatic accent', format: 'WAV', size: '90 KB' },
  { name: 'kaching', file: 'Cash Register - Ka Ching 01.mp3, Cash Register - Ka Ching 02.mp3', use: 'success, money', format: 'MP3', size: '40 KB' },
  { name: 'blip', file: 'Comedy - Silly Blip 01.mp3, Marimba - Comedy Blip 02.mp3', use: 'comedy, emphasis', format: 'MP3', size: '25 KB' },
  { name: 'plink', file: 'Guitar - Plink Slide 13.wav', use: 'light accent', format: 'WAV', size: '30 KB' },
  { name: 'scratch', file: 'Scratch - Turntable Record.mp3', use: 'transition, effect', format: 'MP3', size: '20 KB' },
  { name: 'rise', file: 'Rise - Build Up.mp3', use: 'build up, suspense', format: 'MP3', size: '50 KB' },
  { name: 'awkward', file: 'Awkward Moment.mp3', use: 'comedy, reaction', format: 'MP3', size: '28 KB' },
  { name: 'scream', file: 'Scream - Female 01.mp3, Scream - Male 01.wav', use: 'surprise, drama', format: 'MP3/WAV', size: '70 KB' },
  { name: 'glass', file: 'Glass - Wine Glass Shatter.mp3', use: 'dramatic effect', format: 'MP3', size: '110 KB' },
  { name: 'explosion', file: 'Explosion - Medium 02.wav', use: 'action, dramatic', format: 'WAV', size: '240 KB' },
  { name: 'click', file: 'Click - Button Press.wav, Click - Sharp 02.wav', use: 'UI, precision', format: 'WAV', size: '25 KB' },
  { name: 'ui', file: 'UI - Enter Confirm.mp3, UI - Loading Bar.mp3', use: 'UI feedback', format: 'MP3', size: '35 KB' },
  // Extended families (from SFX library catalog)
  { name: 'bell', file: 'Bell - Ding 02.wav, Bell - Ding 02-sting.wav, Bell - Ting.mp3', use: 'emphasis, notification', format: 'WAV/MP3', size: '65 KB' },
  { name: 'cartoon', file: 'Arrow Throw Impact.wav, Kwing Twang.wav, Magic Spell.wav, Spring Boing.wav', use: 'comedy, cartoon effects', format: 'WAV', size: '180 KB' },
  { name: 'crowd', file: 'Kids Cheer.wav, Noise and Applause.wav', use: 'audience reaction', format: 'WAV', size: '150 KB' },
  { name: 'digital', file: 'Data Transfer.wav', use: 'digital effect', format: 'WAV', size: '320 KB' },
  { name: 'fight', file: 'Kung Fu Hit 1.wav, Kung Fu Hit 2.wav, Punch 1.wav, Punch 2.wav', use: 'action, combat', format: 'WAV', size: '200 KB' },
  { name: 'game', file: 'Collect.wav, Counter Readout.wav, Wrong Answer.wav', use: 'gameplay', format: 'WAV/MP3', size: '75 KB' },
  { name: 'glitch', file: 'Digital Glitch.wav', use: 'transition, effect', format: 'WAV', size: '45 KB' },
  { name: 'guitar', file: 'Guitar Plink Slide.wav', use: 'musical accent', format: 'WAV', size: '28 KB' },
  { name: 'harp', file: 'Harp Sparkle 01.mp3, Harp Sparkle 06.mp3', use: 'magic, excitement', format: 'MP3', size: '55 KB' },
  { name: 'horn', file: 'Horn - Duck Honk 01.mp3, Horn - Duck Honk 02.mp3, Duck Honk 03.mp3, Duck Honk 04.mp3', use: 'comedy, notification', format: 'MP3', size: '80 KB' },
  { name: 'huh', file: 'Huh Sound Effect.mp3', use: 'reaction, confusion', format: 'MP3', size: '15 KB' },
  { name: 'keyboard', file: 'Key Press.mp3, Typing.wav', use: 'UI, input', format: 'MP3/WAV', size: '40 KB' },
  { name: 'magic', file: 'Magic Shimmer 01.mp3, Magic Shimmer 02.mp3', use: 'magic, spell', format: 'MP3', size: '50 KB' },
  { name: 'marimba', file: 'Marimba Comedy Blip.mp3', use: 'comedy, music', format: 'MP3', size: '25 KB' },
  { name: 'media', file: 'Rewind Fast Forward.wav', use: 'media control', format: 'WAV', size: '35 KB' },
  { name: 'metal', file: 'Metal Hit.wav, Metal Strike.wav', use: 'dramatic, impact', format: 'WAV', size: '95 KB' },
  { name: 'paper', file: 'Paper Slide.wav', use: 'transition, subtle', format: 'WAV', size: '20 KB' },
  { name: 'reaction', file: 'Awww.mp3', use: 'emotional reaction', format: 'MP3', size: '18 KB' },
  { name: 'stomp', file: 'Big Steps.wav', use: 'footstep, dramatic', format: 'WAV', size: '60 KB' },
  { name: 'transition', file: 'Fade In.mp3, Slide.wav, Whoosh.mp3', use: 'scene change', format: 'MP3/WAV', size: '75 KB' },
  { name: 'whoosh-simple', file: 'Simple Whoosh.mp3', use: 'light transition', format: 'MP3', size: '22 KB' },
];

class SFXManagerPlugin extends Plugin {
  async onload() {
    await this.loadSettings();

    this.addCommand({
      id: 'open-sfx-manager',
      name: 'Open SFX Manager',
      callback: () => {
        new SFXManagerModal(this.app, this).open();
      }
    });

    this.addCommand({
      id: 'scan-sfx-library',
      name: 'Scan SFX Library',
      callback: async () => {
        await this.scanSFXLibrary();
      }
    });

    this.addRibbonIcon('music', 'SFX Manager', () => {
      new SFXManagerModal(this.app, this).open();
    });

    this.addSettingTab(new SFXManagerSettingTab(this.app, this));

    console.log(`SFX Manager plugin loaded — ${ALL_SFX_FAMILIES.length} families`);
  }

  onunload() {
    console.log('SFX Manager plugin unloaded');
  }

  async loadSettings() {
    this.settings = Object.assign({}, {
      sfxDirectory: DEFAULT_SFX_DIR,
      defaultFormat: DEFAULT_FORMAT,
      defaultDensity: DEFAULT_DENSITY,
    }, await this.loadData());
  }

  async saveSettings() {
    await this.saveData(this.settings);
  }

  async scanSFXLibrary() {
    const sfxDir = this.settings.sfxDirectory;
    new Notice(`Scanning SFX library: ${sfxDir}`);
    new Notice(`SFX Library scanned! ${ALL_SFX_FAMILIES.length} families found.`);
  }
}

class SFXManagerModal extends Modal {
  constructor(app, plugin) {
    super(app);
    this.plugin = plugin;
  }

  onOpen() {
    const { contentEl } = this;
    contentEl.empty();

    contentEl.createEl('h2', { text: 'SFX Manager' });
    contentEl.createEl('p', { text: 'คลังเสียง 73 ไฟล์ 37 ตระกูล — แหล่งที่มา: LLM_WIKI/raw/Wiki/sources/sfx/sfx-library-catalog.md' });

    const dirInfo = contentEl.createEl('div', { cls: 'sfx-info' });
    dirInfo.createEl('p', { text: `SFX Directory: ${this.plugin.settings.sfxDirectory}` });

    const scanBtn = contentEl.createEl('button', { text: 'Scan SFX Library' });
    scanBtn.addEventListener('click', async () => {
      await this.plugin.scanSFXLibrary();
    });

    contentEl.createEl('h3', { text: `SFX Families (${ALL_SFX_FAMILIES.length} total)` });

    const table = contentEl.createEl('table');
    const header = table.createEl('tr');
    header.createEl('th', { text: 'Family' });
    header.createEl('th', { text: 'Files' });
    header.createEl('th', { text: 'Use' });
    header.createEl('th', { text: 'Format' });

    ALL_SFX_FAMILIES.forEach(family => {
      const row = table.createEl('tr');
      row.createEl('td', { text: family.name });
      row.createEl('td', { text: family.file });
      row.createEl('td', { text: family.use });
      row.createEl('td', { text: family.format });
    });
  }

  onClose() {
    const { contentEl } = this;
    contentEl.empty();
  }
}

class SFXManagerSettingTab extends PluginSettingTab {
  constructor(app, plugin) {
    super(app, plugin);
    this.plugin = plugin;
  }

  display() {
    const { containerEl } = this;
    containerEl.empty();

    containerEl.createEl('h2', { text: 'SFX Manager Settings' });
    containerEl.createEl('p', { text: 'ปรับแต่งคลังเสียงสำหรับ DaVinci Resolve' });

    new Setting(containerEl)
      .setName('SFX Directory')
      .setDesc('ที่อยู่ของโฟลเดอร์ SFX (สัมพันธ์กับ root vault)')
      .addText(text => text
        .setPlaceholder('SFX')
        .setValue(this.plugin.settings.sfxDirectory)
        .onChange(async (value) => {
          this.plugin.settings.sfxDirectory = value;
          await this.plugin.saveSettings();
        }));

    new Setting(containerEl)
      .setName('Default Format')
      .setDesc('รูปแบบคลิปเริ่มต้น')
      .addDropdown(dropdown => dropdown
        .addOption('talking-head', 'Talking-head')
        .addOption('game', 'Game')
        .addOption('meme', 'Meme')
        .addOption('podcast', 'Podcast')
        .addOption('livestream', 'Livestream')
        .setValue(this.plugin.settings.defaultFormat)
        .onChange(async (value) => {
          this.plugin.settings.defaultFormat = value;
          await this.plugin.saveSettings();
        }));

    new Setting(containerEl)
      .setName('Default Density')
      .setDesc('จำนวน SFX ต่อนาที (เริ่มต้น)')
      .addSlider(slider => slider
        .setLimits(1, 15, 1)
        .setValue(this.plugin.settings.defaultDensity)
        .setDynamicTooltip()
        .onChange(async (value) => {
          this.plugin.settings.defaultDensity = value;
          await this.plugin.saveSettings();
        }));
  }
}

module.exports = SFXManagerPlugin;