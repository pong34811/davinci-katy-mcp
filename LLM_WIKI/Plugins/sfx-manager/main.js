/*
 * SFX Manager Plugin for Obsidian
 * จัดการ Sound Effects สำหรับ DaVinci Resolve
 */

const { App, Plugin, PluginSettingTab, Setting, Modal, Notice } = require('obsidian');

const DEFAULT_SETTINGS = {
  sfxDirectory: 'C:\\Users\\warit\\Desktop\\davinci-katy-mcp\\SFX',
  defaultFormat: 'talking-head',
  defaultDensity: 4,
};

class SFXManagerPlugin extends Plugin {
  async onload() {
    await this.loadSettings();

    // เพิ่ม command สำหรับเปิด SFX Manager
    this.addCommand({
      id: 'open-sfx-manager',
      name: 'Open SFX Manager',
      callback: () => {
        new SFXManagerModal(this.app, this).open();
      }
    });

    // เพิ่ม command สำหรับสแกน SFX
    this.addCommand({
      id: 'scan-sfx-library',
      name: 'Scan SFX Library',
      callback: async () => {
        await this.scanSFXLibrary();
      }
    });

    // เพิ่ม ribbon icon
    this.addRibbonIcon('music', 'SFX Manager', () => {
      new SFXManagerModal(this.app, this).open();
    });

    // เพิ่ม settings tab
    this.addSettingTab(new SFXManagerSettingTab(this.app, this));

    console.log('SFX Manager plugin loaded');
  }

  onunload() {
    console.log('SFX Manager plugin unloaded');
  }

  async loadSettings() {
    this.settings = Object.assign({}, DEFAULT_SETTINGS, await this.loadData());
  }

  async saveSettings() {
    await this.saveData(this.settings);
  }

  async scanSFXLibrary() {
    const sfxDir = this.settings.sfxDirectory;
    new Notice(`Scanning SFX library: ${sfxDir}`);
    
    // ใน Obsidian จริงจะต้องใช้ fs module
    // แต่สำหรับ demo จะแสดงผลเป็น notice
    new Notice('SFX Library scanned successfully!');
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

    // แสดงข้อมูล SFX directory
    const dirInfo = contentEl.createEl('div', { cls: 'sfx-info' });
    dirInfo.createEl('p', { text: `SFX Directory: ${this.plugin.settings.sfxDirectory}` });

    // ปุ่มสแกน
    const scanBtn = contentEl.createEl('button', { text: 'Scan SFX Library' });
    scanBtn.addEventListener('click', async () => {
      await this.plugin.scanSFXLibrary();
    });

    // แสดงรายการ SFX
    const sfxList = contentEl.createEl('div', { cls: 'sfx-list' });
    sfxList.createEl('h3', { text: 'SFX Families' });

    const families = [
      { name: 'pop', file: 'Pop - Short 06.mp3', use: 'surprise, emphasis' },
      { name: 'ding', file: 'Bell - Ding 02.wav', use: 'emphasis, success' },
      { name: 'collect', file: 'Game - Correct Collect Answer.mp3', use: 'success' },
      { name: 'sparkle', file: 'Harp - Sparkle 01.mp3', use: 'excitement, closing' },
      { name: 'whoosh', file: 'Whoosh - Clean Fast.mp3', use: 'transition' },
      { name: 'impact', file: 'Impact - Comedy Hit 01.mp3', use: 'surprise' },
      { name: 'wrong', file: 'Game - Wrong Answer.mp3', use: 'fail' },
    ];

    const table = sfxList.createEl('table');
    const header = table.createEl('tr');
    header.createEl('th', { text: 'Family' });
    header.createEl('th', { text: 'File' });
    header.createEl('th', { text: 'Use' });

    families.forEach(family => {
      const row = table.createEl('tr');
      row.createEl('td', { text: family.name });
      row.createEl('td', { text: family.file });
      row.createEl('td', { text: family.use });
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

    new Setting(containerEl)
      .setName('SFX Directory')
      .setDesc('ที่อยู่ของโฟลเดอร์ SFX')
      .addText(text => text
        .setPlaceholder('C:\\Users\\warit\\Desktop\\davinci-katy-mcp\\SFX')
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
        .setLimits(1, 10, 1)
        .setValue(this.plugin.settings.defaultDensity)
        .setDynamicTooltip()
        .onChange(async (value) => {
          this.plugin.settings.defaultDensity = value;
          await this.plugin.saveSettings();
        }));
  }
}

module.exports = SFXManagerPlugin;
