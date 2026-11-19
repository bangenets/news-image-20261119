// Entry program for news-image-20261119 (Node 22, standard library only).
//
// The image this entry submits is the entry.png beside this file. The
// program copies it to the output directory the grader provides
// ($MAKEFUN_OUTPUT_DIR outside the grader container, /output inside it),
// so the judge sees exactly those bytes.
//
// Run it locally with:  mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync } from "node:fs";
import { join } from "node:path";

const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
copyFileSync(new URL("./entry.png", import.meta.url), join(outDir, "entry.png"));
