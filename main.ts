// Deliver the rendered newspaper entry to the make.fun output directory.
// Node 22+, standard library only, no network. Copies entry.png (the 1024px
// render) from beside this program into $MAKEFUN_OUTPUT_DIR (default /output).

import { access, copyFile, mkdir } from 'node:fs/promises';
import { dirname, join, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

const here = dirname(fileURLToPath(import.meta.url));
const src = join(here, 'entry.png');
const outDir = process.env.MAKEFUN_OUTPUT_DIR ? resolve(process.env.MAKEFUN_OUTPUT_DIR) : '/output';

try {
  await access(src);
} catch {
  console.error(`entry image not found next to program: ${src}`);
  process.exit(1);
}

await mkdir(outDir, { recursive: true });
const dst = join(outDir, 'entry.png');
await copyFile(src, dst);

console.log(`copied ${src} -> ${dst}`);
