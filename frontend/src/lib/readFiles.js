// Liest den Text von Anhaengen. Einfache Textdateien werden direkt im Browser
// gelesen, docx und pdf liest das Backend aus (derselbe Leser wie bei der Wissensbasis).
import { postFile } from "./apiClient.js";

const TEXT = /\.(txt|md|csv|json)$/i;
const SERVER = /\.(docx|pdf)$/i;

export async function readFiles(files) {
  return Promise.all(files.map(async (f) => {
    if (TEXT.test(f.name)) return { name: f.name, text: await f.text() };
    if (SERVER.test(f.name)) {
      const r = await postFile("/api/knowledge/extract", f);
      return { name: f.name, text: r.text };
    }
    return { name: f.name, text: "" };
  }));
}