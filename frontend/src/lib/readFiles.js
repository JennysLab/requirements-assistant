// Liest den Text von Anhaengen (nur einfache Textdateien). Andere Dateitypen
// werden nur mit Namen weitergegeben. TODO: docx/pdf serverseitig auslesen.
const TEXT = /\.(txt|md|csv|json)$/i;
export async function readFiles(files) {
  return Promise.all(files.map(async (f) => ({ name: f.name, text: TEXT.test(f.name) ? await f.text() : "" })));
}
